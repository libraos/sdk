# LibraOS SDK — worked examples

Each example is a runnable script. Set `LIBRAOS_BASE_URL` and `LIBRAOS_API_KEY`
env vars first.

```bash
pip install libraos-sdk
export LIBRAOS_BASE_URL=https://libraos.partner.com
export LIBRAOS_API_KEY=msk_live_...

python examples/00_quickstart.py
```

## How the SDK is shaped

Two objects get you to a working agent: an **employee** (`employees.create`) owns one or more agents and their model routing, and an **agent** (`agents.create`) is the runnable behaviour bound to it. There is no separate session or environment object: memory is keyed on the `(API key, end_user, agent)` triple (pass `X-End-User` for per-end-user isolation), and a per-tenant filesystem is an opt-in agent flag (`filesystem.enabled: true`). To steer a run, send another `messages.create()` to the same agent.

Total to go from zero to a working digital agent: **3 SDK calls** (`00_quickstart.py`).

## Example index

| File | Surface |
|---|---|
| `00_quickstart.py` | **Start here.** Fastest path from zero to a digital agent — 3 SDK calls: employee, agent, message |
| `01_basic_chat.py` | Hello world — one `c.messages.create()` to an existing agent, no agent setup |
| `02_create_employee_and_agent.py` | Full lifecycle: employee → owned agent → first chat → cleanup |
| `03_upload_knowledge.py` | `c.knowledge` — ingest a document then search it back |
| `04_custom_tool_inline.py` | Mode A (SSE inline) — partner intercepts `custom_tool_use` mid-stream |
| `05_custom_tool_webhook.py` | Mode B (webhook) — partner exposes a FastAPI endpoint |
| `06_multi_model_fallback.py` | Per-employee `model_config` cascade, observe fallback fields |
| `07_bundle_export_import.py` | Tenant onboarding via `.nova-bundle.zip` round-trip |
| `08_async_job_long_running.py` | Submit async job, poll status, receive final result |
| `09_streaming_messages.py` | `c.messages.stream(...)` minimum-lines example — token-on-the-wire latency for chat UIs |
| `10_idempotency.py` | `idempotency_key=` on `create()` — safely retry across network failures, no duplicates |
| `11_pagination.py` | `async for x in c.agents.list()` auto-pagination — page boundaries invisible to partner code |
| `12_documents_upload.py` | `c.documents` — multipart upload, list, delete; auto-indexed on upload |
| `13_hooks_subscribe.py` | `c.hooks` — register lifecycle-event subscriptions (9 canonical events) |
| `14_filesystem_seed.py` | `c.filesystem` — seed an agent's per-tenant workspace before its first turn |
| `15_users_settings_admin.py` | `c.users` + `c.settings` — partner-admin onboarding flow |
| `16_sessions_explicit.py` | `c.sessions` — explicit session lifecycle (per-ticket / per-batch isolation, session-default model override) |
| `17_personas_discovery.py` | `c.personas` — boot-time persona-manifest discovery with ETag/If-None-Match cache validation |
| `19_durable_run.py` | Native background jobs — submit once, replay progress after disconnect, inspect the persisted outcome |

## Native background jobs

`19_durable_run.py` is a standalone Python 3.10+ example with no extra packages.
Unlike the managed-jobs example, it uses the native server contract at
`/agents/v1/{agent}/jobs`, where successful completion is `done`. Set
`LIBRA_OS_URL` and `LIBRA_OS_TOKEN` to your deployment and bearer token:

```bash
python examples/19_durable_run.py --agent my-agent --prompt "Summarize the approved documents."
```

Save the returned job ID. To reconnect to existing work without submitting again:

```bash
python examples/19_durable_run.py --agent my-agent --job-id "$JOB_ID" --after 42
```

The example retries observation only, never submission. A timed-out POST can
already have created work; do not automatically submit another job. The CLI's
cursor is not durable application storage, and an invocation finishing does
not establish that a separately queued approval action executed.

Restart-safe event numbering and atomic terminal receipts require the
durable-runs server update, which is not yet released. General agent recovery
is not enabled by this example. See the [background tasks guide](https://libraos.com/docs/durable-runs/)
for permissions, retention, and recovery limits.

Run the offline example tests from the SDK repository root:

```bash
python3 -B -m unittest discover -s python/tests -p 'test_durable_run_example.py' -v
```

For full end-to-end vertical integrations (legaltech contract review,
healthcare clinical-note triage, finance 10-K diff) see [`../../examples/`](../../examples/).
