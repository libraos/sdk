# LibraOS SDK

Partner integration SDK for **LibraOS** — the agentic operating system that lets you build vertical AI products on a multi-model, multi-tenant runtime.

> **New to LibraOS?** Start with the [Create your first agent](https://libraos.com/docs/creating-an-agent/) tutorial — three SDK calls from zero to a working agent, then come back here for the full surface.

This repo ships:

- **OpenAPI spec** (`openapi/libra-os-partner.v1.yaml`) — source of truth for the partner-facing API surface.
- **CLI** (`cli/`) — single static Go binary for sync, validate, test-callback, export/import.
- **Python SDK** (`python/`) — reference client library, published to PyPI as `libraos-sdk`.
- **Docs** (`docs/`) — getting started, Desk chat, multi-model, web-search, custom tools.
- **Examples** (`examples/`) — worked partner integrations (legaltech, healthcare, finance).

Official docs: [libraos.com/docs](https://libraos.com/docs/) — including [Create your first agent](https://libraos.com/docs/creating-an-agent/) and [Model settings & token plans](https://libraos.com/docs/model-settings/).

## Install

| Surface | Command |
|---|---|
| Python SDK | `pip install libraos-sdk` |
| CLI binary | `curl -L $(release_url)/libraos-cli_linux_amd64.tar.gz \| tar -xz` |
| CLI Docker | `docker pull ghcr.io/libraos/libraos-cli:latest` |

See `python/README.md` and `cli/README.md` for usage details.

Building a web or mobile Desk client? Start with the
[Desk chat and conversation API](docs/desk-chat-api.md).

## Self-hosting the LibraOS server

The SDK targets a running LibraOS server. To stand one up yourself:

| Resource | What it is |
|---|---|
| [`ghcr.io/libraos/libraos`](https://github.com/orgs/libraos/packages/container/package/libraos) | Public, multi-arch Docker image of the server. `docker pull ghcr.io/libraos/libraos:v0.2.1`. |
| [`libraos/stack`](https://github.com/libraos/stack) | Reference docker-compose manifests — core (LibraOS + Postgres + SurrealDB) plus 8 optional companion apps (LibreChat chat UI, SearXNG, crawl4ai, Firecrawl, Docling, FlashRank, Phoenix, Hermes). |
| [docs.libraos.com/install](https://docs.libraos.com/install) | Step-by-step install guide: prerequisites, env vars, smoke tests, reverse-proxy templates. |
| [docs.libraos.com/releases](https://docs.libraos.com/releases) | Release notes + migration notes for each server version. |

### Minimal local evaluation

Smallest practical local instance — LibraOS plus a disposable Postgres. **Not for production**:

```bash
docker network create libraos-eval
docker run --rm -d --name libraos-pg --network libraos-eval \
  -e POSTGRES_USER=libraos \
  -e POSTGRES_PASSWORD=libraos \
  -e POSTGRES_DB=libraos \
  postgres:16
docker run --rm --network libraos-eval -p 8900:8900 \
  -e LIBRA_OS_PUBLIC_URL=http://localhost:8900 \
  -e LIBRA_OS_JWT_SECRET=$(openssl rand -hex 32) \
  -e LIBRA_OS_ADMIN_EMAIL=admin@example.com \
  -e LIBRA_OS_ADMIN_PASSWORD=$(openssl rand -hex 16) \
  -e LIBRA_OS_DATABASE_URL='postgres://libraos:libraos@libraos-pg:5432/libraos?sslmode=disable' \
  -e OPENAI_API_BASE=http://your-vllm-host:8000/v1 \
  -e OPENAI_API_KEY=local \
  ghcr.io/libraos/libraos:v0.2.1
```

The server runs against **any OpenAI-compatible endpoint** — a local vLLM/Ollama
for a fully self-hosted, air-gapped deployment (shown above), or a hosted
provider. Set `OPENAI_API_BASE`, `OPENAI_API_KEY` and, optionally,
`OPENAI_MODEL` to match.

Then point the SDK at it:

```python
import asyncio
from libraos import Client

async def main() -> None:
    async with Client(base_url="http://localhost:8900", api_key="msk_eval_...") as client:
        msg = await client.messages.create(
            "default",
            [{"role": "user", "content": "Hello, LibraOS!"}],
            max_tokens=256,
        )
        print(msg.text)

asyncio.run(main())
```

For anything beyond evaluation (real Postgres, companion apps, TLS, OIDC) use the [`libraos/stack`](https://github.com/libraos/stack) manifests linked above and follow [docs.libraos.com/install](https://docs.libraos.com/install).

If you only need to call a hosted LibraOS that someone else operates, skip this section — the SDK works against any reachable LibraOS endpoint.

## Python SDK

The native client (`from libraos import Client`) covers the whole partner surface: chat over `/v1/messages`, the multi-model `model_config` cascade at employee and agent level, structured-output `output_type` validation, custom-tool webhooks, portable employee bundles and async jobs. See [`python/examples/00_quickstart.py`](python/examples/00_quickstart.py).

Python SDK 2.0 removes the Anthropic-compatibility client; see [`python/CHANGELOG.md`](python/CHANGELOG.md).

## Status

**Python SDK: v2.0.0** — published to PyPI as [`libraos-sdk`](https://pypi.org/project/libraos-sdk/). 2.0.0 is a clean break: the Anthropic-compatibility client is gone and every Nova-era name is now LibraOS. See [`python/CHANGELOG.md`](python/CHANGELOG.md).

**OpenAPI spec: v1.0.0-alpha.7** — still advancing ahead of the SDK to declare new server endpoints as they land.

## License

> ⚠️ **License Notice**
>
> The **LibraOS server** is provided for **evaluation and development use** under the Business Source License. Production deployments require a commercial license — contact support@libraos.com for pricing.
>
> The **SDK in this repository** (Python, CLI, OpenAPI) is **MIT-licensed** and free to use commercially.
