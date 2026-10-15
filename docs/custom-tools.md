# Custom Tools

Partner-implemented tools run over **webhooks** ("Mode B"): LibraOS POSTs an HMAC-SHA256-signed JSON payload to a partner endpoint per tool call, and the partner returns the result in the HTTP response. Calls are idempotent via `tool_use_id` dedup. Declare tools per agent in `custom_tools[]`, each with a `callback`.

> Answering tool calls over the open message stream ("Mode A", `submit_tool_result`) is not supported and has been removed from the SDK. Use webhooks.

## Webhooks

LibraOS POSTs a signed JSON payload to a partner-registered URL whenever the agent calls a custom tool. Partner runs the tool and returns the result in the HTTP response.

Webhooks suit any HTTP-server-shaped partner (FastAPI / Flask / Lambda / Cloudflare Workers), long-running tools (no connection is held while the tool runs), fire-and-forget tools (run async, ack the webhook fast), and tools that live in different services (each callback URL can point at its own service).

### Webhook payload

```json
POST https://partner.example.com/libraos/cb/tools/fetch_invoice

Headers:
  Content-Type: application/json
  X-LibraOS-Signature: t=1714867200,v1=<hex(hmac_sha256(secret, ts + "." + tool_use_id + "." + body))>
  X-LibraOS-Idempotency-Key: toolu_abc123

Body:
{
  "tool_use_id": "toolu_abc123",
  "name": "fetch_invoice",
  "input": {"invoice_id": "INV-2026-042"},
  "agent_id": "invoice-bot",
  "employee_id": "legal-team",
  "session_id": "sess_xyz",
  "ts": 1714867200
}
```

**Header names during the transition.** Receivers get both the new headers above and the older `X-Nova-Signature` / `X-Nova-Idempotency-Key`, with the same values; older servers send only the `X-Nova-*` ones. Read the `X-LibraOS-*` header and fall back to the `X-Nova-*` one. `WebhookRouter` does this for you, and `libraos-cli test-callback` sends both.

### Expected response

```json
HTTP/1.1 200 OK
Content-Type: application/json

{"output": "Invoice INV-2026-042: status=paid", "is_error": false}
```

Or for errors:

```json
{"output": "rate limited by ERP", "is_error": true}
```

### Worked example (FastAPI)

```python
import os
from fastapi import FastAPI
from libraos.callbacks import WebhookRouter

router = WebhookRouter(secret=os.environ["LIBRA_OS_CB_SECRET"])


@router.tool("fetch_invoice")
async def fetch_invoice(input: dict, ctx: dict) -> str:
    invoice_id = input.get("invoice_id", "UNKNOWN")
    agent_id = ctx.get("agent_id", "?")
    # In production: query your DB / ERP.
    return f"Invoice {invoice_id}: status=paid"


@router.tool("check_eligibility")
async def check_eligibility(input: dict, ctx: dict) -> dict:
    client_id = input.get("client_id")
    return {"eligible": True, "reason": "All criteria met", "client_id": client_id}


app = FastAPI()
app.include_router(router.fastapi_router(), prefix="/libraos/cb")
```

`WebhookRouter` handles:
- HMAC-SHA256 signature verification (rejects with 401 on mismatch)
- Idempotency dedup by `tool_use_id` (skips duplicate deliveries — LibraOS retries on transient failures)
- Replay-window enforcement (5min default — rejects requests with `t` outside the window)
- Auto-serialisation of dict / str / list returns to JSON

Full example: [`python/examples/05_custom_tool_webhook.py`](../python/examples/05_custom_tool_webhook.py).

### Signature scheme

```
t=<unix_ts>,v1=<hex(hmac_sha256(secret, ts + "." + tool_use_id + "." + body))>
```

Three components separated by `.`:

1. **Timestamp** (`ts`) — Unix seconds. LibraOS rejects deliveries with `|now - ts| > 300s` (5min replay window). Partners must verify the same window.
2. **`tool_use_id`** — pins the signature to a specific tool invocation. Replaying the body alone won't pass verification for a different `tool_use_id`.
3. **Body** — the raw JSON body bytes (no whitespace normalization).

### Idempotency dedup

LibraOS may retry webhook deliveries on transient network failures. The same `tool_use_id` may arrive 1-3 times. Partners should dedup:

```python
# WebhookRouter does this for you:
@router.tool("fetch_invoice")
async def fetch_invoice(input, ctx):
    # Already deduped by tool_use_id before reaching this fn.
    ...
```

Or manually (DIY router):

```python
seen_ids = set()
async def handle(req):
    # the tool_use_id; older servers send only X-Nova-Idempotency-Key
    tool_use_id = req.headers.get("X-LibraOS-Idempotency-Key") or req.headers["X-Nova-Idempotency-Key"]
    if tool_use_id in seen_ids:
        return {"output": cached_result_for(tool_use_id), "is_error": False}
    seen_ids.add(tool_use_id)
    ...
```

In production, use Redis / your DB / a TTL cache — in-process sets don't survive restarts.

### Smoke test

Forge a LibraOS-shaped signed POST to your handler before exposing it to live traffic:

```bash
export LIBRA_OS_CB_SECRET=your-shared-hmac-secret
libraos-cli test-callback \
  --target https://partner.example.com/libraos/cb \
  --tool fetch_invoice \
  --input '{"invoice_id":"INV-9912"}'
```

Test idempotency dedup with `--repeat 3 --tool-use-id toolu_dedupe_test` — your handler should run exactly once.

## Tool definition (server-side)

A custom tool is declared on the agent with its `callback`:

```python
await c.agents.create(
    id="invoice-bot",
    type="conversational",
    custom_tools=[
        {
            "name": "fetch_invoice",
            "description": "Fetch invoice details by ID.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "invoice_id": {"type": "string", "description": "Invoice identifier"},
                },
                "required": ["invoice_id"],
            },
            # The webhook LibraOS calls for this tool.
            "callback": {
                "url": "https://partner.example.com/libraos/cb/tools/fetch_invoice",
                "auth": {"type": "hmac_sha256", "secret_ref": "partner_webhook_secret"},
                "timeout_sec": 30,
                "retry": {"max_attempts": 3, "backoff": "exponential"},
            },
        },
    ],
)
```

### Input schema gotcha (Vertex AI)

If you declare `type: array` in the schema **without** `items`, LibraOS validation rejects the agent on save. This catches a class of failure where Vertex AI strictly enforces JSON Schema and returns 400 at chat time:

```python
# ✗ Rejected at validation:
"input_schema": {"type": "object", "properties": {"ids": {"type": "array"}}}

# ✓ Accepted:
"input_schema": {"type": "object", "properties": {"ids": {"type": "array", "items": {"type": "string"}}}}

# ✓ Also accepted (catch-all):
"input_schema": {"type": "object", "properties": {"ids": {"type": "array", "items": {}}}}
```

The CLI's `libraos-cli validate ./data/` runs this rule offline, before deploy.

## Retries + dispatch

When LibraOS POSTs to a partner endpoint and gets a non-2xx response or timeout:

| Response | Action |
|---|---|
| `200 OK` with `is_error: false` | Use result, continue agent loop |
| `200 OK` with `is_error: true` | Surface to agent as recoverable error |
| `4xx` (4xx body) | Surface to agent as fatal error — don't retry (it'd fail the same way) |
| `5xx` or network timeout | Retry with exponential backoff (max 3 by default) |
| Final retry failed | Surface to agent as upstream-error |

Configure per-tool via the `retry` block on the callback:

```python
"callback": {
    "url": "...",
    "auth": {...},
    "retry": {
        "max_attempts": 5,
        "backoff": "exponential",
    },
}
```

## See also

- [`getting-started.md`](getting-started.md) — front-door + scenario matrix
- [`python/examples/05_custom_tool_webhook.py`](../python/examples/05_custom_tool_webhook.py) — webhook worked example
- [`cli/README.md` → test-callback](../cli/README.md#test-callback-mode-b-webhook-smoke) — webhook smoke-test flow
