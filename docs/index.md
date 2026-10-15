---
title: LibraOS SDK Documentation
---

# LibraOS SDK Documentation

Partner integration docs for [LibraOS](https://github.com/libraos/sdk) — the agentic operating system that lets you build vertical AI products on a multi-model, multi-tenant runtime.

> ⚠️ **License Notice**
>
> The **LibraOS server** is provided for **evaluation and development use** under the Business Source License. Production deployments require a commercial license — contact support@libraos.com for pricing.
>
> The **SDK** (Python, CLI, OpenAPI) is **MIT-licensed** and free to use commercially.

## Start here

| Doc | What it covers |
|---|---|
| [Getting Started](getting-started.md) | Front-door table, 5-minute first call, scenario matrix |
| [Desk Chat and Conversation API](desk-chat-api.md) | Conversation CRUD, persisted messages, AG-UI streaming, citations, scope isolation, recovery |
| [Multi-Model Routing](multi-model.md) | Three slots (answer / planner / skill), five-level cascade, fallback semantics |
| [Web Search Backends](web-search.md) | Five pluggable backends, cost-quality table, fallback chains, reformulator, recency intent |
| [Comparing Search Backends](comparing-search-backends.md) | Side-by-side pricing / latency / features for each backend |
| [Custom Tools](custom-tools.md) | Mode A (SSE inline) + Mode B (webhook) end-to-end, HMAC signing, idempotency |
| [Deployment](deployment.md) | Self-hosted vs cloud, three deploy shapes, reverse-proxy templates, observability |
| [Scenarios](scenarios.md) | 10 lifecycle workflows traced end-to-end with wire-level detail |

## SDK reference

| Surface | Doc |
|---|---|
| Python SDK | [`python/README.md`](https://github.com/libraos/sdk/blob/main/python/README.md) |
| CLI | [`cli/README.md`](https://github.com/libraos/sdk/blob/main/cli/README.md) |
| OpenAPI spec | [`openapi/libra-os-partner.v1.yaml`](https://github.com/libraos/sdk/blob/main/openapi/libra-os-partner.v1.yaml) |
| Worked examples | [`python/examples/`](https://github.com/libraos/sdk/tree/main/python/examples) — 18 numbered examples covering every public surface |

## Server-side

For partners who need to operate LibraOS themselves:

| Doc | Where |
|---|---|
| Install LibraOS | [libraos.com/docs](https://libraos.com/docs/) |
| Releases / cadence | [libraos.com/docs](https://libraos.com/docs/) |
| Pre-built deploy stack | [`libraos/stack`](https://github.com/libraos/stack) — compose manifests + 8 companion apps |

## Status

**Python SDK 2.0.0** — Removes the Anthropic-compatibility client and renames every Nova-era name to LibraOS; see [`python/CHANGELOG.md`](https://github.com/libraos/sdk/blob/main/python/CHANGELOG.md). PyPI: `pip install libraos-sdk`.

**CLI 1.0.0** — Multi-arch binaries (`linux/darwin/windows × amd64/arm64`), cosign-signed, Docker image at `ghcr.io/libraos/libraos-cli`.

**OpenAPI alpha.7** — Partner-facing API surface continuing to grow toward the v1 freeze. The Python SDK \`__version__\` is 2.0.0; \`OPENAPI_VERSION\` tracks the spec separately.

**Server image** — `ghcr.io/libraos/libraos:v0.2.1` (and `:latest`).

See [libraos.com/docs](https://libraos.com/docs/) for the cadence.

## Contributing

Issues and PRs welcome on the SDK side at [`libraos/sdk`](https://github.com/libraos/sdk). The LibraOS server itself is in a separate repository under a different license — see the notice above.

## Contact

- General SDK questions: open an issue on [`libraos/sdk/issues`](https://github.com/libraos/sdk/issues)
- Server-side issues: the LibraOS server repository is private; file at the SDK level if you don't have access
- Commercial licensing: support@libraos.com
