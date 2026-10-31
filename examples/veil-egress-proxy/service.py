"""A small HTTP service: mask a conversation, send it to a model, restore the answer.

    python service.py --backend echo                         # no key: shows what would leave
    python service.py --backend libraos                      # a LibraOS agent, through libraos-sdk
    python service.py --backend openai --base-url URL/v1     # any OpenAI-compatible endpoint

    POST /v1/ask      {"messages": [{"role": "user", "content": "..."}], "system": "...", "model": "...", "max_tokens": 2000}
                   -> {"text": restored answer, "masked": mentions replaced}
    POST /v1/preview  the same request -> {"would_send": {"system", "messages"}, "masked": n}; sends nothing

It fails closed: fields it has not masked are refused, not passed on, and an answer holding a placeholder the mapping
does not cover is not returned. The mapping lives for one request and is never logged or sent.
"""
from __future__ import annotations

import argparse, asyncio, json, os, sys, threading, urllib.error, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from veil_mask import Detector, Mapping, mask, restore

REQUEST_FIELDS = {"messages", "system", "model", "max_tokens"}
MAX_BYTES = 4 * 1024 * 1024


class Refused(Exception):
    def __init__(self, status: int, error: str, **detail):
        self.status, self.body = status, dict(error=error, **detail)


# ------------------------------------------------------------------ where the masked text goes
def libraos_backend():
    """A LibraOS agent. LIBRA_OS_URL, LIBRA_OS_API_KEY, LIBRA_OS_AGENT_ID (default: "default")."""
    from libraos import Client

    url, key, agent = os.environ["LIBRA_OS_URL"], os.environ["LIBRA_OS_API_KEY"], os.environ.get("LIBRA_OS_AGENT_ID", "default")

    async def call(messages, system, model, max_tokens):
        async with Client(base_url=url, api_key=key) as c:
            msg = await c.messages.create(agent, messages=messages, system=system, model=model, max_tokens=max_tokens)
        return msg.text

    return lambda *a: asyncio.run(call(*a))


def openai_backend(base_url: str):
    """Any OpenAI-compatible endpoint. The key, if it needs one, is OPENAI_API_KEY."""
    key = os.environ.get("OPENAI_API_KEY")

    def call(messages, system, model, max_tokens):
        body = {"model": model, "max_tokens": max_tokens, "messages": ([{"role": "system", "content": system}] if system else []) + messages}
        headers = {"Content-Type": "application/json"} | ({"Authorization": f"Bearer {key}"} if key else {})
        req = urllib.request.Request(base_url.rstrip("/") + "/chat/completions", json.dumps(body, ensure_ascii=False).encode(), headers)
        with urllib.request.urlopen(req, timeout=300) as r:
            return json.loads(r.read())["choices"][0]["message"].get("content") or ""

    return call


def echo_backend():
    """No model at all: prints what would have left, and quotes it back, the way a model reuses the names it was given."""

    def call(messages, system, model, max_tokens):
        print("--- the outside model would receive ---\n" + json.dumps({"system": system, "messages": messages}, ensure_ascii=False, indent=1), file=sys.stderr)
        return "Noted: " + messages[-1]["content"]

    return call


# ------------------------------------------------------------------ the round trip
def parse(request: dict) -> tuple[list[dict], str | None]:
    unknown = set(request) - REQUEST_FIELDS
    if unknown:
        raise Refused(400, "field_not_masked", fields=sorted(unknown))
    messages = request.get("messages")
    if not messages:
        raise Refused(400, "no_messages")
    for i, m in enumerate(messages):
        if set(m) != {"role", "content"} or m["role"] not in ("user", "assistant") or not isinstance(m["content"], str):
            raise Refused(400, "message_not_masked", index=i)
    system = request.get("system")
    if system is not None and not isinstance(system, str):
        raise Refused(400, "system_not_masked")
    return messages, system


def mask_request(request: dict, detect) -> tuple[list[dict], str | None, Mapping]:
    messages, system = parse(request)
    mapping = Mapping()
    try:
        masked_system = mask(system, detect, mapping) if system else None
        masked = [{"role": m["role"], "content": mask(m["content"], detect, mapping)} for m in messages]
    except Exception as e:  # nothing is sent if the masking did not finish
        raise Refused(503, "masking_failed", kind=type(e).__name__)
    return masked, masked_system, mapping


def ask(request: dict, detect, send) -> dict:
    masked, system, mapping = mask_request(request, detect)
    try:
        answer = send(masked, system, request.get("model"), request.get("max_tokens") or 2000)
    except urllib.error.HTTPError as e:
        # An error's text is dropped: it can quote the request, and nothing restores it.
        raise Refused(502, "model_error", upstream_status=e.code)
    except Exception as e:
        raise Refused(502, "model_error", kind=type(e).__name__)
    if not answer:
        raise Refused(502, "empty_answer", hint="a reasoning model can spend a small max_tokens before it answers")
    text, unresolved = restore(answer, mapping)
    if unresolved:
        raise Refused(502, "unresolved_placeholder", count=len(unresolved))
    return {"text": text, "masked": len(mapping.originals)}


def make_handler(detect, send):
    lock = threading.Lock()  # one forward pass at a time

    def locked_detect(text):
        with lock:
            return detect(text)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):  # method, path and status only, never a body
            sys.stderr.write("%s %s %s\n" % (self.command, self.path, args[1] if len(args) > 1 else ""))

        def reply(self, status, obj):
            body = json.dumps(obj, ensure_ascii=False).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_POST(self):
            if self.path not in ("/v1/ask", "/v1/preview"):
                return self.reply(404, {"error": "not_found"})
            n = int(self.headers.get("Content-Length") or 0)
            if n > MAX_BYTES:
                return self.reply(413, {"error": "too_large", "max_bytes": MAX_BYTES})
            try:
                request = json.loads(self.rfile.read(n))
                if self.path == "/v1/preview":
                    messages, system, mapping = mask_request(request, locked_detect)
                    return self.reply(200, {"would_send": {"system": system, "messages": messages}, "masked": len(mapping.originals)})
                self.reply(200, ask(request, locked_detect, send))
            except Refused as e:
                self.reply(e.status, e.body)
            except (ValueError, KeyError, AttributeError, TypeError):
                self.reply(400, {"error": "bad_request"})

    return Handler


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--backend", choices=["echo", "libraos", "openai"], default="echo")
    ap.add_argument("--base-url", help="for --backend openai, ending in /v1")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8931)
    ap.add_argument("--device", default="cpu")
    a = ap.parse_args()
    if a.backend == "openai" and not a.base_url:
        ap.error("--backend openai needs --base-url")
    send = {"echo": echo_backend, "libraos": libraos_backend, "openai": lambda: openai_backend(a.base_url)}[a.backend]()
    detect = Detector(device=a.device)
    print(f"masking service on http://{a.host}:{a.port}/v1, backend {a.backend}", file=sys.stderr)
    ThreadingHTTPServer((a.host, a.port), make_handler(detect, send)).serve_forever()


if __name__ == "__main__":
    main()
