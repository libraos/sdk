# Getting Started

The front door for partners adopting LibraOS. Use the table below to jump to the doc that matches what you're trying to do — most adoption paths are 5-15 minutes.

> ⚠️ **License Notice**
>
> The **LibraOS server** is provided for **evaluation and development use** under the Business Source License. Production deployments require a commercial license — contact support@libraos.com for pricing.
>
> The **SDK in this repository** (Python, CLI, OpenAPI) is **MIT-licensed** and free to use commercially.

## I want to…

| Goal | Path | Doc |
|---|---|---|
| **Run a LibraOS server locally** | Pull the public Docker image, set three env vars, smoke-test `/api/health` | [libraos.com/docs](https://libraos.com/docs/) |
| **Use the LibraOS native SDK** | `pip install libraos-sdk`; `from libraos import Client` | [`python/examples/00_quickstart.py`](../python/examples/00_quickstart.py) |
| **Manage employees / agents from the terminal** | Install `libraos-cli`, set a profile, run `employees list` | [`cli/README.md`](../cli/README.md) |
| **Validate a folder of agent/employee definitions before deploy** | `libraos-cli validate ./data/` — offline CI gate | [`cli/README.md` → validate](../cli/README.md#validate-offline-ci-gate) |
| **Sync a local folder of definitions to a server** | `libraos-cli sync ./data/` (one-shot or `--watch`) | [`cli/README.md` → sync](../cli/README.md#sync-folder--server) |
| **Use multi-model fallbacks** | Per-call / per-skill / per-agent / per-employee / server-default cascade | [`multi-model.md`](multi-model.md) |
| **Add a custom tool with HTTP webhook fan-out** | Mode A (SSE inline) or Mode B (webhook) | [`custom-tools.md`](custom-tools.md) |
| **Bring my own search backend** | Tavily, Brave, Exa, SearXNG, MegaNova with fallback chains | [`web-search.md`](web-search.md) |
| **Compare search backends** | Pricing, latency, features for each option | [`comparing-search-backends.md`](comparing-search-backends.md) |
| **Deploy to production** | Reverse proxy, TLS, Postgres, scaling notes | [`deployment.md`](deployment.md) |
| **Pin a specific server version** | Track release tags + image digests | [libraos.com/docs](https://libraos.com/docs/) |

## 5-minute first call

The fastest path from zero to "I have a working LibraOS instance answering chat requests." Assumes Docker is installed.

### 1. Stand up the server

```bash
docker run -d --name libraos -p 8900:8900 \
  -e LIBRA_OS_DATABASE_URL="postgres://libraos:secret@host.docker.internal:5432/libraos" \
  -e LIBRA_OS_JWT_SECRET="$(openssl rand -hex 32)" \
  -e LIBRA_OS_ADMIN_EMAIL="admin@example.com" \
  -e LIBRA_OS_ADMIN_PASSWORD="changeme-please-12chars" \
  -e OPENAI_API_KEY="msk_..." \
  ghcr.io/libraos/libraos:v0.2.1
```

Defaults that "just work" against the MegaNova gateway: `OPENAI_API_BASE=https://api.meganova.ai`, `OPENAI_MODEL=gemini/gemini-2.5-flash`. Override either to use OpenAI direct or pick a different model.

`v0.2.1` and `:latest` track each other. For partner-validation builds, use the `-week-YYYY-MM-DD` weekly tags. See the [docs](https://libraos.com/docs/) for the release cadence.

### 2. Verify health

```bash
curl http://localhost:8900/api/health
# {"status":"ok","agents_available":67,"agents_registered":67,"circuit_breakers_open":0}
```

### 3. First chat

**Python SDK:**

```python
import asyncio
from libraos import Client

async def main() -> None:
    async with Client(base_url="http://localhost:8900", api_key="msk_...") as c:
        msg = await c.messages.create(
            "legal-assistant",
            [{"role": "user", "content": "What is contract clause 7.3 about?"}],
            max_tokens=256,
        )
        print(msg.text)

asyncio.run(main())
```

**CLI:**

```bash
libraos-cli config set local --url http://localhost:8900 --api-key-env LIBRA_OS_API_KEY
libraos-cli config default local
export LIBRA_OS_API_KEY=msk_...

libraos-cli messages send legal-assistant "What is contract clause 7.3 about?"
```

## Scenario matrix

End-to-end paths for the most common partner tasks. Each row points at a worked example.

| Scenario | What it shows | Worked example |
|---|---|---|
| Hello-world chat | `c.messages.create` round-trip | [`python/examples/01_basic_chat.py`](../python/examples/01_basic_chat.py) |
| Create an employee + agent from scratch | Define employee, attach agents, set model_config | [`python/examples/02_create_employee_and_agent.py`](../python/examples/02_create_employee_and_agent.py) |
| Upload knowledge to a collection | Ingest + verify retrieval at chat time | [`python/examples/03_upload_knowledge.py`](../python/examples/03_upload_knowledge.py) |
| Mode A custom tool (SSE inline) | Stream + `submit_tool_result` round-trip | [`python/examples/04_custom_tool_inline.py`](../python/examples/04_custom_tool_inline.py) |
| Mode B custom tool (webhook) | HMAC-signed webhook + idempotency dedup | [`python/examples/05_custom_tool_webhook.py`](../python/examples/05_custom_tool_webhook.py) |
| Multi-model with fallback | Per-call model override + cascade resolution | [`python/examples/06_multi_model_fallback.py`](../python/examples/06_multi_model_fallback.py) |
| Bundle export / import | `.nova-bundle.zip` across instances | [`python/examples/07_bundle_export_import.py`](../python/examples/07_bundle_export_import.py) |
| Async long-running job | Job submit + polling | [`python/examples/08_async_job_long_running.py`](../python/examples/08_async_job_long_running.py) |
| Streaming chat | SSE event parsing | [`python/examples/09_streaming_messages.py`](../python/examples/09_streaming_messages.py) |
| Idempotency | `Idempotency-Key` retry-safe POSTs | [`python/examples/10_idempotency.py`](../python/examples/10_idempotency.py) |
| Auto-paginating list | Walk every record without offset bookkeeping | [`python/examples/11_pagination.py`](../python/examples/11_pagination.py) |
| Documents upload | `c.documents` partner-prefix CRUD | [`python/examples/12_documents_upload.py`](../python/examples/12_documents_upload.py) |
| Lifecycle hooks | `c.hooks` subscribe to canonical agent-loop events | [`python/examples/13_hooks_subscribe.py`](../python/examples/13_hooks_subscribe.py) |
| Per-tenant filesystem | `c.filesystem` seed + read | [`python/examples/14_filesystem_seed.py`](../python/examples/14_filesystem_seed.py) |
| Admin: users + settings | `c.users` + `c.settings` partner-prefix admin | [`python/examples/15_users_settings_admin.py`](../python/examples/15_users_settings_admin.py) |
| Explicit sessions | `c.sessions` create + get for resumed conversations | [`python/examples/16_sessions_explicit.py`](../python/examples/16_sessions_explicit.py) |
| Persona discovery (boot-time) | `c.personas.list()` with `If-None-Match` ETag | [`python/examples/17_personas_discovery.py`](../python/examples/17_personas_discovery.py) |
| Folder-to-server sync | `libraos-cli sync ./data/` | [`cli/README.md` → sync](../cli/README.md#sync-folder--server) |
| Webhook smoke test | Forge a LibraOS-shaped signed POST to your handler | [`cli/README.md` → test-callback](../cli/README.md#test-callback-mode-b-webhook-smoke) |

## Auth resolution

For every CLI command and SDK call, credentials resolve in this order:

1. Explicit constructor args (`Client(base_url=..., api_key=...)`) or CLI flags (`--url`, `--api-key`)
2. Environment variables (`LIBRA_OS_URL`, `LIBRA_OS_API_KEY`)
3. Profile in `~/.libraos/config.yaml` selected by `--profile` / `LIBRA_OS_PROFILE`, falling back to `default:`

A partner running multiple environments (dev / staging / prod) keeps one profile per environment in `config.yaml` and switches via `--profile prod`.

## Next steps

- **Working in production?** [`deployment.md`](deployment.md) covers reverse-proxy templates, TLS, Postgres sizing, multi-replica deploys, and the SSE flag that's load-bearing for Cloudflare-fronted streaming.
- **Building a vertical product?** The [`libraos/cookbook`](https://github.com/libraos/cookbook) holds end-to-end recipes — its `legaltech/` recipe is the canonical reference integration (EqualDocs's `legal-assistant` shape, validated end-to-end at 7/7 against the latest server build).
- **Running into an issue?** Open one at [`libraos/sdk/issues`](https://github.com/libraos/sdk/issues). It is also the place for server-side issues if you don't have access to the LibraOS server repository.
