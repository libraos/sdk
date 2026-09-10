"""Offline tests for the native durable-jobs example (standard library)."""

import contextlib
import importlib.util
import io
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import threading
import unittest
from unittest.mock import patch


spec = importlib.util.spec_from_file_location(
    "durable_run", Path(__file__).resolve().parents[1] / "examples/19_durable_run.py"
)
example = importlib.util.module_from_spec(spec)
spec.loader.exec_module(example)


class ExampleTests(unittest.TestCase):
    def test_sse_handles_multiline_and_discards_incomplete_frame(self):
        raw = b': heartbeat\n\nid: 42\nevent: progress\ndata: {"a":\ndata: 1}\n\nid: 43\ndata: {"partial":true}\n'
        self.assertEqual(list(example.events(io.BytesIO(raw))), [(42, "progress", {"a": 1})])

    def run_example(self, *, existing=False, bad_submission=False, final_status="done"):
        state = {"posts": 0, "streams": 0, "cursors": [], "auth": []}

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *_):
                pass

            def reply(self, body, kind="application/json"):
                self.send_response(200)
                self.send_header("Content-Type", kind)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def do_POST(self):
                state["posts"] += 1
                state["auth"].append(self.headers.get("Authorization"))
                self.rfile.read(int(self.headers.get("Content-Length", 0)))
                body = {} if bad_submission else {"job_id": "job_saved", "status": "queued"}
                self.reply(json.dumps(body).encode())

            def do_GET(self):
                state["auth"].append(self.headers.get("Authorization"))
                if self.path.endswith("/stream"):
                    state["streams"] += 1
                    state["cursors"].append(self.headers.get("Last-Event-ID"))
                    if state["streams"] == 1:
                        # Lose connection during event 2. Only complete event 1
                        # may be acknowledged before reconnecting.
                        body = b'id: 1\nevent: progress\ndata: {"type":"progress"}\n\nid: 2\ndata: {"partial":'
                    else:
                        body = b'id: 2\nevent: done\ndata: {"type":"done"}\n\n'
                    self.reply(body, "text/event-stream")
                else:
                    status = final_status if state["streams"] >= 2 else "running"
                    self.reply(json.dumps({"job_id": "job_saved", "status": status}).encode())

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        output, errors = io.StringIO(), io.StringIO()
        args = ["--url", f"http://127.0.0.1:{server.server_port}", "--agent", "test-agent"]
        args += ["--job-id", "job_saved"] if existing else ["--prompt", "test task"]
        try:
            with patch.dict("os.environ", {"LIBRA_OS_TOKEN": "test-only"}), patch.object(example.time, "sleep"), contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
                code = example.main(args)
        finally:
            server.shutdown()
            server.server_close()
            thread.join()
        self.assertTrue(all(token == "Bearer test-only" for token in state["auth"]))
        return code, state, output.getvalue(), errors.getvalue()

    def test_reconnects_to_same_job_without_resubmitting(self):
        code, state, output, _ = self.run_example()
        self.assertEqual(code, 0)
        self.assertEqual(state["posts"], 1)
        self.assertEqual(state["cursors"], ["0", "1"])
        self.assertIn('"status": "done"', output)

    def test_existing_job_never_posts(self):
        code, state, _, _ = self.run_example(existing=True)
        self.assertEqual(code, 0)
        self.assertEqual(state["posts"], 0)

    def test_unknown_submission_outcome_is_not_retried(self):
        code, state, _, errors = self.run_example(bad_submission=True)
        self.assertEqual(code, 2)
        self.assertEqual(state["posts"], 1)
        self.assertEqual(state["streams"], 0)
        self.assertIn("Do not resubmit", errors)

    def test_done_event_does_not_override_failed_job_status(self):
        code, _, _, _ = self.run_example(final_status="failed")
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
