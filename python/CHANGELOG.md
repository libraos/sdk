# Changelog

All notable changes to `libraos-sdk` (Python) will be documented in this file.

## [2.0.0] — 2026-10-16

**Breaking.** The SDK drops Anthropic SDK compatibility and takes the LibraOS name everywhere it
owns one. There are no aliases or deprecation shims: update imports and environment variables
before upgrading.

### Added

- **Per-end-user memory: `end_user=` on `messages.create()` and `messages.stream()`.** Pass your
  end user's id and the SDK sends it as the `X-End-User` header, so the server keeps memory per end
  user: one agent serving many customers keeps each one's memory apart. Omitted, no header is sent.

### Removed

- **`AnthropicCompatClient`.** LibraOS no longer promises to be a drop-in for the Anthropic Python
  SDK or the Claude Agent SDK. Use `libraos.Client`: `await c.messages.create(agent_id, messages,
  model=..., max_tokens=...)` returns a `Message`, and `msg.text` joins its text blocks. The
  `01b_claude_agent_sdk_drop_in.py` example and the compat tests are gone, and `01_basic_chat.py`
  now uses `libraos.Client`.
- **The `anthropic` package** is no longer in the `dev` extra.
- **Mode A custom tools: `MessageStream.submit_tool_result()`** and the `message_id=` argument of
  `c.messages.stream(...)`, which existed only for it. Answering a tool call over the open stream
  never worked end to end on the server. Run custom tools over webhooks ("Mode B": declare the tool
  with a `callback` and serve it with `WebhookRouter`); see `docs/custom-tools.md`. The
  `04_custom_tool_inline.py` example is gone.

### Changed

- **`NovaOSError` is now `LibraOSError`.** Every SDK error still subclasses it.
- **Example and test environment variables** use the `LIBRA_OS_` prefix, the same as the
  server's settings (`LIBRA_OS_URL`, `LIBRA_OS_API_KEY`, `LIBRA_OS_AGENT_ID`, …).
- **The simulator's harness agent id** is `libraos-simulator-harness` (was
  `nova-os-simulator-harness`). A deployment that provisioned the old id falls back to a transient
  agent until it provisions the new one.
- **`WebhookRouter.flask_blueprint()`** names its blueprint `libraos_callbacks` by default (was
  `nova_callbacks`). Pass `name=` to keep the old name.
- **LibraOS wire names.** The client sends `X-LibraOS-SDK-Version` and `X-LibraOS-OpenAPI-Hash`
  (was `X-Nova-SDK-Version` / `X-Nova-OpenAPI-Hash`). `WebhookRouter` and its FastAPI, Flask and
  Lambda mounts verify `X-LibraOS-Signature` / `X-LibraOS-Idempotency-Key`, falling back to
  `X-Nova-Signature` / `X-Nova-Idempotency-Key` when the new headers are absent, so receivers work
  against both new and older servers. Bundles are named `.libraos-bundle.zip` in the docs and
  examples; import accepts any file name.

### Breaking changes — migrating from 1.x

1. **Anthropic compatibility is removed.** Replace `AnthropicCompatClient` with `libraos.Client`
   and call `await c.messages.create(agent_id, messages, ...)`; read the reply with `msg.text`.
   If you use the `anthropic` package directly, install it yourself — the `dev` extra no longer
   pulls it in.
2. **Renamed names.** `NovaOSError` → `LibraOSError`; `NOVA_OS_*` example/test environment
   variables → `LIBRA_OS_*`; simulator harness agent `nova-os-simulator-harness` →
   `libraos-simulator-harness`; Flask blueprint `nova_callbacks` → `libraos_callbacks`. There are
   no aliases.
3. **Mode A custom tools are removed.** `MessageStream.submit_tool_result()` and
   `messages.stream(..., message_id=...)` are gone. Declare each custom tool with a `callback` and
   serve it with `WebhookRouter` (Mode B).
4. **Wire names, with fallback.** The client now sends `X-LibraOS-SDK-Version` /
   `X-LibraOS-OpenAPI-Hash`. Webhook receivers verify `X-LibraOS-Signature` /
   `X-LibraOS-Idempotency-Key` and fall back to the `X-Nova-*` headers, so they keep working
   against older servers — no change needed unless you verify signatures yourself, in which case
   read the new header first and fall back to the old one.
5. **`end_user=` is additive.** Nothing to change; pass it on `messages.create()` /
   `messages.stream()` when one agent serves many end users and their memory must stay apart.

| 1.x | 2.0.0 |
|---|---|
| `from libraos import AnthropicCompatClient` | `from libraos import Client` — `await c.messages.create(agent_id, messages, ...)` |
| `NovaOSError` | `LibraOSError` |
| `NOVA_OS_URL` | `LIBRA_OS_URL` |
| `NOVA_OS_API_KEY` | `LIBRA_OS_API_KEY` |
| `pip install "libraos-sdk[dev]"` installs `anthropic` | no longer installed; install it yourself if you use it directly |
| `stream.submit_tool_result(...)` (Mode A) | a webhook per tool: `callback` on the tool + `WebhookRouter` |

## [1.2.0] — 2026-10-12

### Added

- **Persona-drift metric for the simulator** ([`libraos-sdk#29`](https://github.com/libraos/sdk/issues/29)),
  productizing Kenneth Li's methodology ([ArXiv 2402.10962](https://arxiv.org/html/2402.10962v1)).
  `SimulationResult.drift` is populated on every `simulate()` call, `client.measure_drift(transcript,
  archetype)` scores any transcript shape, and a `drift_alert` stream event fires when the score
  crosses the threshold mid-loop. New exports: `DriftMetric`, `DriftTurn`, `DriftOptions`,
  `measure_drift`. Archetypes gain an optional `drift_alert_threshold` (default `0.15`).

  **What it measures.** The archetype constrains the SIMULATOR, not the target agent, so drift
  scores the synthetic customer's turns. It answers "was this run still testing the persona you
  authored?" — it is a validity check on the evaluation, **not** a quality score for the agent under
  test. Reading it as the latter would be a confident misuse.

  **What it does not measure**, because using it without knowing this will mislead you: semantic
  drift that preserves register — a persona still sounding like a customer while contradicting its
  own biography — is undetected and needs a model-based judge. Also paraphrased leakage, tone and
  emotional-stance drift, non-English transcripts (marker sets are English-only, so a
  Punjabi-register archetype under-scores on its Punjabi turns), and persona turns the probe cadence
  did not sample (at the default `probe_every=2`, half of them). A model-graded method can register
  under a new `method=` identifier without changing a signature.

  A run too short to measure reports `measured == False` with a reason rather than `0.0` — "perfect
  retention" and "not measured" are different claims, and conflating them would drag any corpus
  average toward zero.

- **OpenAPI spec `1.0.0-alpha.8`** — the partner spec catches up with the server through the
  v0.2.1 weeklies; `libraos._generated` (and the Go and TypeScript clients) are regenerated from it.
  No hand-written wrappers were added; call the new endpoints through `libraos._generated`.
  - New endpoints: the Agent Skills catalog (`/v1/skills*`), scheduled runs
    (`/v1/managed/schedules*`), decision probes (`/v1/decision/{name}` + `train` / `activate` /
    `predict`) and model recommendations (`/v1/managed/models/recommendations*`). Each one's
    auth and feature-flag gating is in its operation description.
  - `/v1/agents`: `thinking` (effort now includes `none`), `tool_choice`, `direct_tools`,
    `tool_scope`, `triage`, `turn_budget_tokens`, `agent_skills`, `on_ambiguous_entity`,
    `egress_guard`, a typed `guardrails` object, and `clear_triage` on update.
  - `/v1/chat/completions`: `reasoning_effort` and `response_format`, a 0–2 range on
    `temperature`, typed `metadata` keys, and `nova_usage` on the response.
  - Chat `metadata` on all three chat surfaces: `research_query`, `research_query_only`,
    `max_searches`, `egress_guard`, `allowed_skills`, `research_depth`, `on_ambiguous_entity`,
    `thinking`, `tool_choice`.
  - The `usage` block: per-stage timing, `phases`, `timeline`, `context_budget`, `working_set`,
    `tool_calls`, `agent_skills`, and cache token counts. Native chat gains the `retrieval`
    ambiguity block. The `grounding` enum gains `unsupported_figures`.

- **Also generated since `1.1.1`** (reached through `libraos._generated`, no wrappers):
  `POST /v1/search` (#98), `/api/knowledge/*`, `/api/super-nova/*` and `/api/capabilities` (#97),
  knowledge signals and eval suites (#93), the authorization lifecycle — intents, grants,
  capabilities, decisions (#90), the Desk chat contract — conversations and attachments (#96),
  `GET /api/agents` (#101), and three grounding enum values the server already returned (#100).

### Fixed

- **`python-dateutil` is now a declared dependency.** The generated models (`libraos._generated`)
  import it, but it was never listed, so on a clean `pip install libraos-sdk` (1.1.1 included)
  `from libraos._generated import models` raised `ModuleNotFoundError`. CI did not see it because
  the dev extras pull it in transitively.

### Upgrade note

- **`drift_alert` is a new `TurnEvent.kind`, emitted by default.** A clean run's stream is unchanged
  — it fires only when a run actually drifts — and consumers that ignore unknown kinds need no
  change. Code that asserts an exhaustive set of kinds will see a new one. Default-on is deliberate:
  the premise of #29 is that partners are running multi-turn evals blind, and a warning you have to
  know to enable does not fix that. Opt out with `DriftOptions(alert=False)`.
- `SimulationResult.drift` and `TurnEvent.drift` both default to `None`, so the v1.0.0-frozen public
  API is unaffected for existing callers and stored results.

## [1.1.1] — 2026-08-05

Python SDK changes since `1.0.0`.

> **Note on what was already shipped.** Several entries below — the `c.documents`,
> `c.knowledge`, `c.hooks`, `c.filesystem`, `c.users`, `c.settings`, `c.sessions` and
> `c.personas` wrappers, and `client.simulate()` — were already present in the
> published `1.0.1`/`1.0.2` artifacts; they were bound by `Client.__init__` but never
> documented or claimed by a release. They are recorded here because this is the
> release that first documents them (the README work shipped separately in `1.0.3`).
> Nothing about their behaviour changes; if you are already calling them on `1.0.2`
> or `1.0.3`, they are the same methods. What is genuinely new in this cut is the simulator work — the
> rubric-grading harness and the vertical pack loader.
>
> `1.1.0` was published and then **yanked** — it shipped these simulator features ahead
> of the partner-prefix gate this section describes. The version number stays reserved
> on PyPI and cannot be reused, so the next minor cut is `1.1.1`. The discoverability
> fix it also carried was re-released on its own as `1.0.3`.

The OpenAPI spec advanced through `1.0.0-alpha.3` → `1.0.0-alpha.4` → `1.0.0-alpha.5` to declare new server endpoints the SDK now wraps. For LibraOS **server-side** release notes that pair with this SDK release, see [docs.meganova.ai/nova-os/releases](https://docs.meganova.ai/nova-os/releases).

### Added
- **Partner OpenAPI expanded to the full current surface** — 31 → 109 paths, with the
  Go, TypeScript and Python clients regenerated from it ([`libraos-sdk#62`](https://github.com/libraos/sdk/pull/62)). Purely additive: none of
  the 31 existing paths were removed. The regenerated code lands in
  `libraos._generated`; the hand-written public API is untouched, so partner code
  keeps working unchanged. This was the partner-prefix gate the 1.1.x line waited on.

- **Typed `Message` response** from `messages.create()` (#74). A `dict`
  subclass, so every existing access pattern is unchanged
  (`resp["content"][0]["text"]`, `isinstance(resp, dict)`, `json.dumps`) while
  callers gain typed access — `resp.content[0].text` — and a `resp.text`
  convenience that joins all text blocks. Exported as `Message`,
  `ContentBlock`, `Usage`.
- **Opt-in integration tests** against a real server (#73): `tests/integration`
  under a `-m integration` marker, skipped unless `LIBRA_OS_URL` /
  `LIBRA_OS_API_KEY` are set, plus a weekly `integration.yml` CI job that boots
  a container + Postgres and runs them. This is the layer that catches
  server-side contract breaks (like the 1.0.1 `model` fix) that mock-transport
  unit tests cannot.

- **`c.documents`** — partner-prefix CRUD wrapper for `/v1/managed/documents`. OpenAPI alpha.3.
- **`c.knowledge`** — partner-prefix wrapper for `/v1/managed/knowledge`. OpenAPI alpha.3.
- **`c.hooks`** — partner-prefix CRUD for lifecycle-hook subscriptions under `/v1/managed/hooks`. OpenAPI alpha.3. First slice is in-memory on the server; persistence + bus bridge tracked for a follow-up.
- **`c.filesystem`** — partner-prefix wrapper for `/v1/managed/filesystem`. OpenAPI alpha.3. `POST /provision` endpoint deferred to a follow-up.
- **`c.users`** + **`c.settings`** — partner-prefix wrappers for `/v1/managed/users` and `/v1/managed/settings`. OpenAPI alpha.3.
- **`c.sessions`** — partner-prefix wrapper for `/v1/managed/sessions`. OpenAPI alpha.4. Currently `create` + `get`; `list` / `delete` / `fork` tracked for a follow-up.
- **`c.personas`** — boot-time persona-contract surface (`GET /agents/v1/personas` + `:id`) with `If-None-Match` ETag round-trip and `PersonaNotFound` typed error. OpenAPI alpha.5. Closes [`libraos-sdk#14`](https://github.com/libraos/sdk/issues/14).
- **`PersonaNotFound`** typed error — subclass of `NotFoundError`, raised by `c.personas.get(persona_id)` on a 404 with the persona-envelope shape `{"error": "persona not found", "id": ...}`. `parse_error_response` detects the envelope.
- Examples 16 (sessions), 17 (personas discovery), and 18 (custom persona + `output_type.persist_fields` slot collection across sync + streaming) under `python/examples/`.

### Fixed

- **Codegen-python CI gate unblocked** ([`libraos-sdk#15`](https://github.com/libraos/sdk/issues/15)). `openapi-python-client` 0.28.3 had been crashing on every push since `AgentCreate` landed as `allOf: [Agent]`, leaving `_generated/` permanently stale. Flattened `AgentCreate` to a duplicated property block (wire shape unchanged) and loosened `Agent.route_templates` from `additionalProperties: {type: string}` to `additionalProperties: true`. Codegen now produces full output for all 8 alpha.3-alpha.5 resources (`documents`, `filesystem`, `hooks`, `knowledge`, `personas`, `sessions`, `settings`, `users`) — previously these endpoints were declared in OpenAPI but never auto-generated, so `_generated/` only carried the v0.9.0 surface. Hand-written `nova_os/resources/*.py` public API unaffected; partner code keeps working.

## [1.0.3] — 2026-08-05

Documentation and packaging only — no library code changed. Cut from `v1.0.2` rather
than from `main` so the fix reaches PyPI without shipping the unreleased simulator
work alongside it. The client surface is byte-identical to `1.0.2`: all twelve
resources and `client.simulate()` were already bound there, they were simply never
documented.

### Fixed

- **Discoverability of the published package** ([`libraos-sdk#82`](https://github.com/libraos/sdk/issues/82)) — reported by a first-time integrator who evaluated the whole SDK without being able to find this repository.
  - `[project.urls]` added to `pyproject.toml` (Homepage / Documentation / Source / Issues / Changelog), so PyPI finally links back to the repo. The published `1.0.2` metadata carries no `project_urls` at all.
  - Resources table in `python/README.md` now documents all twelve bound resources — `documents`, `knowledge`, `hooks`, `filesystem`, `users`, `settings`, `sessions` and `personas` were previously absent, with `knowledge` (`search` / `ingest` / `collections`) the one integrators concluded was missing. Notes that the sync mirror covers only `agents`, `employees`, `messages`, `jobs`.
  - New **Synthetic-customer simulator** section covering `client.simulate()`, `Archetype`, `SimulationResult` / `Turn`, the `stream=True` `TurnEvent` iterator, and `async_simulate()`. Previously reachable only via `dir(libraos)`.
  - README status line corrected from `v0.9.0-rc1` to the shipped version (also in the repo-root `README.md`).
  - The `python/examples/` reference now links to GitHub and states that examples are not shipped inside the installed package.

## [1.0.2] — 2026-07-31

### Fixed

- Documentation module references: swept every stale `from nova_os import ...`
  in the README, `python/README.md` (the PyPI project page), docs, and release
  notes to `from libraos import ...`. No code change — the module has always
  been `libraos` — but the PyPI landing page's first code block was broken.

## [1.0.1] — 2026-07-31

### Fixed

- `messages.create()` / `messages.stream()` now default the wire `model` field
  to the `agent_id` when the caller omits it. `/v1/messages` requires `model`
  for Anthropic-SDK compatibility even though routing is by `metadata.agent_id`
  (the server treats it as cosmetic), so the documented
  `messages.create(agent_id=..., messages=...)` shape had been returning
  `400 model is required` against a real server.

### Packaging

- First version actually published to PyPI. The release workflow's PyPI upload
  had been gated on an unset `PYPI_API_TOKEN` secret and silently skipped every
  tag (incl. 1.0.0); it now publishes via PyPI Trusted Publishing (OIDC).

## [1.0.0] — 2026-05-02

**Public API stable.** First stable release of the v1.x line. **No breaking changes from `v0.9.0rc1`** — upgrade is `pip install --upgrade libraos-sdk`.

See [`docs/release-notes/v1.0.0.md`](../docs/release-notes/v1.0.0.md) for the comprehensive release notes.

### Added since v0.9.0rc1

- `release.yml` extended with `build-cli` job — multi-arch CLI binaries (linux/darwin/windows × amd64/arm64), cosign keyless signing, Docker image at `ghcr.io/meganovaai/nova-os-cli`. Multi-arch manifest covers `linux/amd64` + `linux/arm64`.
- CLI surface complete: `employees`, `agents`, `jobs`, `messages` (via SDK), `sync` (one-shot + `--watch`), `validate` (with Vertex schema-bug guardrail), `test-callback` (Mode B webhook smoke), `config` (profile management), `version` (with embedded build metadata).

### Unchanged from v0.9.0rc1

Every Python public surface, including the wire formats for HMAC signing, SSE event names, and OpenAPI request/response shapes. `v1.0.0` is functionally identical at the Python API layer — the additions are CLI + release pipeline.

### Still deferred to v1.1+

- `c.knowledge` resource (depends on a future server-side endpoint)
- `c.settings` resource (admin-only)
- `nova-os-cli logs` subcommand
- `nova-os-cli sync --prune` (destructive sync)
- TypeScript / Rust / Go-direct client SDKs — codegen from `openapi/libra-os-partner.v1.yaml` if needed

## [0.9.0rc1] — 2026-05-01

**API freeze candidate.** Public surface is locked for `v1.0.0`. Downstream
consumers can integrate against this tag.

### Added

- `nova_os.Client(base_url, api_key)` — async-first with `.sync` proxy mirror
- 4 resources: `agents`, `employees`, `messages`, `jobs` — CRUD + auto-paginating `list()`
- `c.messages.stream(...)` — async context manager + Mode A `submit_tool_result`
- `libraos.callbacks.WebhookRouter` — Mode B HMAC verification + idempotency dedup
- FastAPI / Flask / AWS Lambda integration mounts (lazy-imported)
- `nova_os.AnthropicCompatClient(...)` — drop-in factory pre-configured for LibraOS's `/v1/managed` path
- Recorded fixture test proving Anthropic SDK round-trips against LibraOS-shaped responses
- Typed error hierarchy: `VertexSchemaError`, `BillingError`, `RateLimitedError`, `NotFoundError`, etc.
- `Idempotency-Key` kwarg on POST resource methods
- 7 worked examples in `python/examples/`
- `.github/workflows/release.yml` — builds sdist + wheel on tag push, publishes GitHub Release, conditionally uploads to PyPI

### Pending for v1.0.0

- `knowledge` resource (depends on a future LibraOS server-side endpoint)
- Bundle import via partner-side helpers (export side already works via raw HTTP)
- Per-skill model override (`agent.skills[].model`)
- Full PyPI publish (workflow ready; `PYPI_API_TOKEN` secret must be configured to fire)
