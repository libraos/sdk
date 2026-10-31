"""No model download and no API key: the detector is a stand-in, and LibraOS is a local stub behind the real SDK client.

    pip install pytest libraos-sdk
    pytest test_egress.py
"""
import json, os, sys, threading, urllib.error, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from service import libraos_backend, make_handler
from veil_mask import Mapping, find_spans, mask, restore

NAMES = {"Anna Berg": "person", "Northwind Ltd": "organization", "12 Baker Street": "location", "Paris": "location", "Employee": "person",
         "14 March 1979": "date", "1 March 2027": "date"}


def detect(text):
    """What the model would tag, for the names above."""
    out = []
    for name, label in NAMES.items():
        i = text.find(name)
        if i >= 0:
            out.append({"start": i, "end": i + len(name), "label": label})
    return out


def test_round_trip_puts_every_value_back():
    text = ("Anna Berg (born 14 March 1979, the Employee) of Northwind Ltd, 12 Baker Street: anna.berg@example.org, +1 415 555 0173, "
            "card 4111 1111 1111 1111, IBAN GB82 WEST 1234 5698 7654 32, token sk-demo-Zk3vQ9bLm2Xc7TtYw1RnH8sPd4Fg, host 10.0.0.7. "
            "Refund $40 by 1 March 2027 in Paris.")
    mapping = Mapping()
    masked = mask(text, detect, mapping)
    for value in ("Anna", "14 March 1979", "Northwind", "Baker", "anna.berg", "415", "4111", "GB82", "sk-demo", "10.0.0.7"):
        assert value not in masked, value
    for value in ("$40", "1 March 2027", "Paris", "Employee"):  # what the model needs to reason stays
        assert value in masked, value
    assert restore(masked, mapping) == (text, [])


def test_one_person_keeps_one_placeholder_across_messages_and_mentions():
    mapping = Mapping()
    first = mask("Anna Berg called. Later Anna Berg wrote.", detect, mapping)
    second = mask("Reply to Anna Berg.", detect, mapping)
    assert first == "[PERSON_1] called. Later [PERSON_1] wrote."
    assert second == "Reply to [PERSON_1]."


def test_a_name_the_model_only_sees_once_the_address_is_gone_does_not_leave():
    def distracted(text):  # what the real model does: it tags the name only when the address does not repeat it
        i = text.find("Anna Berg")
        return [] if "anna.berg@" in text or i < 0 else [{"start": i, "end": i + 9, "label": "person"}]

    mapping = Mapping()
    text = "Anna Berg wrote from anna.berg@example.org."
    masked = mask(text, distracted, mapping)
    assert masked == "[PERSON_1] wrote from [EMAIL_1]."
    assert restore(masked, mapping) == (text, [])


def test_a_surname_alone_is_the_same_person_and_does_not_leave():
    mapping = Mapping()
    masked = mask("Ms. Berg paid. Anna Berg signed.", detect, mapping)
    assert masked == "Ms. [PERSON_1] paid. [PERSON_1] signed."
    assert restore("Ms. [PERSON_1] paid.", mapping) == ("Ms. Anna Berg paid.", [])


def test_a_surname_two_people_share_stays_apart():
    names = ("Anna Berg", "Omar Berg", "Berg")

    def tag(text):
        out, pos = [], 0
        for name in names:
            i = text.find(name, pos)
            out.append({"start": i, "end": i + len(name), "label": "person"})
            pos = i + len(name)
        return out

    mapping = Mapping()
    masked = mask("Anna Berg, Omar Berg. Then Berg left.", tag, mapping)
    assert masked == "[PERSON_1], [PERSON_2]. Then [PERSON_3] left."
    assert restore(masked, mapping)[0] == "Anna Berg, Omar Berg. Then Berg left."


def test_a_name_or_address_tagged_in_pieces_gets_one_placeholder():
    def pieces(text):
        return [{"start": text.find(p), "end": text.find(p) + len(p), "label": label}
                for p, label in (("Anna", "person"), ("Berg", "person"), ("48 Elm Grove", "location"), ("Leeds", "location"))]

    mapping = Mapping()
    text = "Anna Berg, 48 Elm Grove, Leeds LS6 2AB"
    masked = mask(text, pieces, mapping)
    assert masked == "[PERSON_1], [ADDRESS_1]"
    assert restore(masked, mapping) == (text, [])


def test_restore_accepts_what_models_do_to_a_placeholder():
    mapping = Mapping()
    mask("Anna Berg", detect, mapping)
    assert restore("[person_1], [PERSON 1], PERSON_1.", mapping) == ("Anna Berg, Anna Berg, Anna Berg.", [])


def test_a_made_up_placeholder_is_reported():
    mapping = Mapping()
    mask("Anna Berg", detect, mapping)
    assert restore("Ask [PERSON_2]; see [Step 1].", mapping) == ("Ask [PERSON_2]; see [Step 1].", ["[PERSON_2]"])


def test_a_placeholder_already_in_the_text_is_left_alone():
    mapping = Mapping()
    masked = mask("The form says [PERSON_1]; the signer is Anna Berg.", detect, mapping)
    assert masked == "The form says [PERSON_1]; the signer is [PERSON_2]."
    assert restore(masked, mapping) == ("The form says [PERSON_1]; the signer is Anna Berg.", [])


@pytest.mark.parametrize("text", [
    'User: "Wait." user: hello. login: required',
    "password = auth[0]; password=self.secret; ${DB_PASS}; Password: required",
    '/home/ubuntu/app, /usr/local/bin, user="root"',
    'MARKER = ("-----BEGIN PRIVATE KEY-----", "-----END PRIVATE KEY-----")',
    "task-force, sk-learn, hf_transfer, version 2.4.1, ISO 9001, order 20231105",
])
def test_ordinary_text_and_code_are_not_identifiers(text):
    assert find_spans(text, lambda t: []) == []


@pytest.mark.parametrize("text, secret", [
    ("DB postgres://svc:Tr0ub4dor9@db.example:5432/x.", "Tr0ub4dor9"),
    ('File "/home/tomasz.w/app.py"', "tomasz.w"),
    ('connect(user="t.w")', "t.w"),
    ("Leeds LS6 2AB", "LS6 2AB"),
    ('password = "correcthorse"', "correcthorse"),
    ("-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASC", "MIIEvQ"),
])
def test_values_with_a_fixed_shape_do_not_leave(text, secret):
    assert secret not in mask(text, lambda t: [], Mapping())


# ------------------------------------------------------------------ the service
def serve(handler):
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{server.server_address[1]}"


def post(url, body):
    req = urllib.request.Request(url, json.dumps(body).encode(), {"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


class Model:
    """A backend that records what it received."""

    def __init__(self, answer=None, error=None):
        self.received, self.answer, self.error = [], answer, error

    def __call__(self, messages, system, model, max_tokens):
        self.received.append({"messages": messages, "system": system})
        if self.error:
            raise self.error
        return self.answer if self.answer is not None else "Noted: " + messages[-1]["content"]


def ask(model, **extra):
    url = serve(make_handler(detect, model))
    return post(url + "/v1/ask", {"messages": [{"role": "user", "content": "Write to Anna Berg, anna@example.org."}]} | extra)


def test_the_model_sees_placeholders_and_the_caller_sees_names():
    model = Model()
    status, body = ask(model, system="The agent works for Northwind Ltd.")
    assert status == 200
    assert "Anna" not in json.dumps(model.received) and "Northwind" not in json.dumps(model.received)
    assert body == {"text": "Noted: Write to Anna Berg, anna@example.org.", "masked": 3}


@pytest.mark.parametrize("extra, error", [
    ({"stream": True}, "field_not_masked"),
    ({"tools": [{"name": "f", "description": "Anna Berg"}]}, "field_not_masked"),
    ({"metadata": {"who": "Anna Berg"}}, "field_not_masked"),
    ({"messages": [{"role": "user", "content": [{"type": "image", "source": "..."}]}]}, "message_not_masked"),
    ({"messages": [{"role": "tool", "content": "Anna Berg"}]}, "message_not_masked"),
    ({"system": ["Anna Berg"]}, "system_not_masked"),
])
def test_what_has_not_been_masked_is_refused_and_not_sent(extra, error):
    model = Model()
    status, body = ask(model, **extra)
    assert (status, body["error"]) == (400, error)
    assert model.received == []


def test_nothing_is_sent_if_masking_fails():
    def broken(text):
        raise RuntimeError("out of memory")

    model = Model()
    url = serve(make_handler(broken, model))
    status, body = post(url + "/v1/ask", {"messages": [{"role": "user", "content": "Anna Berg"}]})
    assert (status, body["error"]) == (503, "masking_failed")
    assert model.received == []


def test_an_answer_with_a_made_up_placeholder_is_not_returned():
    status, body = ask(Model(answer="Ask [PERSON_7]."))
    assert (status, body["error"], body["count"]) == (502, "unresolved_placeholder", 1)
    assert "PERSON_7" not in json.dumps(body)


def test_a_model_error_is_not_passed_on():
    status, body = ask(Model(error=RuntimeError("bad request: Write to [PERSON_1]")))
    assert (status, body) == (502, {"error": "model_error", "kind": "RuntimeError"})


def test_an_empty_answer_says_so():
    assert ask(Model(answer=""))[1]["error"] == "empty_answer"


def test_preview_sends_nothing():
    model = Model()
    url = serve(make_handler(detect, model))
    status, body = post(url + "/v1/preview", {"messages": [{"role": "user", "content": "Anna Berg"}]})
    assert (status, body["would_send"]["messages"][0]["content"]) == (200, "[PERSON_1]")
    assert model.received == [] and "mapping" not in body


def test_through_the_real_libraos_sdk(monkeypatch):
    pytest.importorskip("libraos")
    received = []

    class LibraOS(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_POST(self):
            request = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            received.append((self.path, self.headers["Authorization"], request))
            text = "Noted: " + request["messages"][-1]["content"]
            body = json.dumps({"id": "msg_1", "type": "message", "role": "assistant", "model": request["model"], "stop_reason": "end_turn",
                               "content": [{"type": "text", "text": text}]}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    monkeypatch.setenv("LIBRA_OS_URL", serve(LibraOS))
    monkeypatch.setenv("LIBRA_OS_API_KEY", "msk_test_stub")
    monkeypatch.setenv("LIBRA_OS_AGENT_ID", "support")
    status, body = ask(libraos_backend(), system="The agent works for Northwind Ltd.")
    assert (status, body["text"]) == (200, "Noted: Write to Anna Berg, anna@example.org.")
    path, auth, sent = received[0]
    assert path == "/v1/messages" and "msk_test_stub" in auth and sent["metadata"]["agent_id"] == "support"
    assert "Anna" not in json.dumps(sent) and "Northwind" not in json.dumps(sent)
