#!/usr/bin/env python3
"""Native Libra OS jobs: submit once, observe and reconnect. Python 3.10+.

Set LIBRA_OS_URL and LIBRA_OS_TOKEN. This standalone example uses the native
/agents/v1/{agent}/jobs contract, not the separate managed-jobs SDK helpers.
"""

import argparse
import http.client
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request


TERMINAL = {"done", "failed", "cancelled"}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # A configured server must not redirect bearer credentials elsewhere.
        raise urllib.error.HTTPError(req.full_url, code, "Redirect refused", headers, fp)


def events(lines):
    """Parse complete SSE frames, including multiline data and heartbeat comments."""
    event_id, event_type, data = None, "message", []
    for raw in lines:
        line = raw.decode("utf-8").rstrip("\r\n")
        if not line:
            if data:
                yield event_id, event_type, json.loads("\n".join(data))
            event_id, event_type, data = None, "message", []
            continue
        if line.startswith(":"):
            continue
        field, _, value = line.partition(":")
        if value.startswith(" "):
            value = value[1:]
        if field == "id":
            event_id = int(value)
        elif field == "event":
            event_type = value
        elif field == "data":
            data.append(value)
    # An incomplete final frame is intentionally not acknowledged; reconnect
    # from the preceding ID so that frame can be replayed in full.


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=os.environ.get("LIBRA_OS_URL", "http://127.0.0.1:8900"))
    parser.add_argument("--agent", required=True, help="An installed agent's route ID")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--prompt", help="Submit NEW work exactly once")
    mode.add_argument("--job-id", help="Observe existing work; never submit a replacement")
    parser.add_argument("--after", type=int, default=0, help="Last successfully processed event ID")
    args = parser.parse_args(argv)
    if args.after < 0:
        parser.error("--after must be non-negative")
    if args.prompt is not None and args.after:
        parser.error("--after is only valid with --job-id")
    token = os.environ.get("LIBRA_OS_TOKEN")
    if not token:
        parser.error("set LIBRA_OS_TOKEN to your bearer token")
    parsed = urllib.parse.urlsplit(args.url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc or parsed.username or parsed.query or parsed.fragment:
        parser.error("--url must be an HTTP(S) server URL without credentials, query or fragment")
    base = args.url.rstrip("/") + "/agents/v1/" + urllib.parse.quote(args.agent, safe="") + "/jobs"
    headers = {"Authorization": "Bearer " + token}
    opener = urllib.request.build_opener(NoRedirect())

    def request(method, url, body=None, extra_headers=None):
        hs = {**headers, **(extra_headers or {})}
        raw = None
        if body is not None:
            hs["Content-Type"] = "application/json"
            raw = json.dumps(body).encode()
        return opener.open(urllib.request.Request(url, data=raw, headers=hs, method=method), timeout=30)

    job_id = args.job_id
    if job_id is None:
        # Do not retry POST, even on a timeout: the server may have accepted it.
        try:
            with request("POST", base, {"message": args.prompt}) as response:
                job_id = json.load(response)["job_id"]
        except (OSError, http.client.HTTPException, ValueError, KeyError) as exc:
            print("Submission did not return a usable job ID; it may have been accepted. "
                  "Do not resubmit automatically. Ask the operator to check the original request. "
                  f"Error: {type(exc).__name__}", file=sys.stderr)
            return 2
        print(json.dumps({"job_id": job_id}), flush=True)

    job_url = base + "/" + urllib.parse.quote(job_id, safe="")
    after = args.after
    for attempt in range(5):
        try:
            with request("GET", job_url + "/stream", extra_headers={
                "Accept": "text/event-stream", "Last-Event-ID": str(after),
            }) as response:
                for event_id, event_type, payload in events(response):
                    if event_id is None or event_id <= after:
                        continue
                    print(json.dumps({"id": event_id, "event": event_type, "data": payload}), flush=True)
                    # In an app, advance this cursor only after processing and
                    # durably storing the event. Event delivery can repeat.
                    after = event_id
            with request("GET", job_url) as response:
                job = json.load(response)
            if job["status"] in TERMINAL:
                print(json.dumps(job), flush=True)
                return 0 if job["status"] == "done" else 1
        except urllib.error.HTTPError as exc:
            if exc.code not in {429, 502, 503, 504}:
                print(f"Observation failed: HTTP {exc.code}. No new work was submitted.", file=sys.stderr)
                return 2
        except (OSError, http.client.HTTPException):
            pass  # Retry observation only, using the same job and cursor.
        except (ValueError, KeyError) as exc:
            print(f"Unexpected response ({type(exc).__name__}); no new work was submitted.", file=sys.stderr)
            break
        if attempt < 4:
            time.sleep(min(2 ** attempt, 8))
    print(f"Observation stopped. Job {job_id} may still be running. "
          f"Reconnect with --job-id {job_id} --after {after}; keep the same --agent.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
