# libraos-cli

Single static Go binary for managing LibraOS employees, agents, and jobs from the terminal.

## Install

### Pre-built binary (recommended)

Pre-built binaries for linux/darwin/windows × amd64/arm64 are attached to every GitHub Release:

```bash
# linux/amd64 example — adjust for your platform
TAG=v0.9.0rc2  # or whichever tag you want
curl -L "https://github.com/libraos/sdk/releases/download/$TAG/libraos-cli_linux_amd64.tar.gz" \
  | tar -xz -C /usr/local/bin libraos-cli

libraos-cli version
```

### Docker

```bash
docker run --rm -it ghcr.io/libraos/libraos-cli:latest version
```

Mount your config + data:

```bash
docker run --rm -it \
  -v ~/.libraos:/home/nonroot/.libraos \
  -v $PWD/data:/data \
  -e LIBRAOS_API_KEY \
  ghcr.io/libraos/libraos-cli:latest sync /data/
```

### Verify signature (cosign keyless)

Every binary archive is signed with cosign keyless. Verify:

```bash
TAG=v0.9.0rc2
cosign verify-blob \
  --certificate-identity-regexp 'https://github.com/libraos/sdk/.+' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature libraos-cli_linux_amd64.tar.gz.sig \
  --certificate libraos-cli_linux_amd64.tar.gz.pem \
  libraos-cli_linux_amd64.tar.gz
```

### From source

```bash
go install github.com/libraos/sdk/cli@latest
```

(Installs as `cli` in `$GOPATH/bin`; rename to `libraos-cli` for clarity.)

## Quick start

```bash
# One-time profile setup
libraos-cli config set partner-prod \
  --url https://libraos.partner.com \
  --api-key-env LIBRAOS_PROD_KEY

libraos-cli config default partner-prod
export LIBRAOS_PROD_KEY=<your-bearer-token>

# Verify connection
libraos-cli version

# Day-to-day
libraos-cli employees list
libraos-cli employees get frontdesk
libraos-cli employees create -f frontdesk.json

libraos-cli agents list --owner-employee frontdesk
libraos-cli agents get marketing-assistant

libraos-cli jobs list --status running
libraos-cli jobs get job_abc123

# Validate + sync a local folder of agent/employee definitions
libraos-cli validate ./data/
libraos-cli sync ./data/
libraos-cli sync --watch ./data/

libraos-cli version --json
```

## Profile config

Profiles are stored at `~/.libraos/config.yaml`:

```yaml
default: partner-prod
profiles:
  partner-prod:
    url: https://libraos.partner.com
    api_key_env: LIBRAOS_PROD_KEY
  customer-acme:
    url: https://libraos.acme.example.com
    api_key_env: LIBRAOS_ACME_KEY
    callback_url: https://partner.example.com/libraos/acme
```

Manage profiles with the `config` subcommand:

```bash
libraos-cli config set staging --url https://staging.example.com --api-key-env LIBRAOS_STAGING_KEY
libraos-cli config list
libraos-cli config get staging
libraos-cli config default staging
libraos-cli config delete staging
```

## Auth resolution order

For each command, credentials are resolved in this priority order:

1. `--url` / `--api-key` flags
2. `LIBRAOS_BASE_URL` / `LIBRAOS_API_KEY` env vars
3. Profile in `~/.libraos/config.yaml` (selected by `--profile` flag or `LIBRAOS_PROFILE` env var, falls back to `default:`)

## Global flags

| Flag | Description |
|------|-------------|
| `--profile <name>` | Override active profile |
| `--url <url>` | LibraOS server URL |
| `--api-key <token>` | Bearer token |
| `--json` | Emit JSON output (one object per record, suitable for piping to `jq`) |

## Subcommands

### employees

```bash
libraos-cli employees list
libraos-cli employees get <id>
libraos-cli employees create -f <definition.json>
libraos-cli employees update <id> -f <patch.json>
libraos-cli employees delete <id>
```

### agents

```bash
libraos-cli agents list [--owner-employee <employee-id>]
libraos-cli agents get <id>
libraos-cli agents create -f <definition.json>
libraos-cli agents update <id> -f <patch.json>
libraos-cli agents delete <id>
```

### jobs

```bash
libraos-cli jobs list [--status queued|running|completed|failed|cancelled] [--agent-id <id>]
libraos-cli jobs get <job-id>
libraos-cli jobs create -f <job.json>
libraos-cli jobs cancel <job-id>
```

### messages

Smoke-test path matching the shape of `test-callback`. One short HTTP round-trip from the same auth/profile resolution as the rest of the CLI.

```bash
libraos-cli messages send <agent-id> <prompt> \
    [--end-user <id>] [--metadata '<json>'] [--model <vendor/model>] \
    [--system <prompt>] [--max-tokens <n>] [--timeout 60]

libraos-cli messages stream <agent-id> <prompt> \
    [--end-user <id>] [--metadata '<json>'] [--model <vendor/model>]
```

`send` returns the parsed `MessageResponse` JSON; `stream` opens an SSE connection and prints one event per line (pipe through `jq` for filtering). Both honor the same `LIBRAOS_BASE_URL` / `LIBRAOS_API_KEY` / `--profile` resolution as the rest of the CLI.

Quick smoke test:

```bash
libraos-cli messages send legal-assistant "What's clause 7.3 about?" --end-user demo-user
libraos-cli messages stream legal-assistant "Walk me through the agreement" | jq 'select(.type=="text")'
```

### knowledge

Hybrid search + ingest against the partner's knowledge collections. Backed by `/v1/managed/knowledge/*`.

```bash
libraos-cli knowledge search <query> \
    [--collection <name>] [--top-k 5] [--threshold 0.0]

libraos-cli knowledge ingest <content> \
    [--title <title>] [--collection <name>]

# Or read content from disk:
libraos-cli knowledge ingest -f document.md \
    [--title <title>] [--collection <name>]

libraos-cli knowledge collections
```

`search` returns ranked passages (each with `content`, `score`, `collection`, `document_id`). `ingest` indexes a single document into a collection (defaults to `default`). `collections` lists every collection accessible via the partner's API key.

Quick smoke test:

```bash
libraos-cli knowledge ingest "Section 7.3: termination requires written notice" --title "Sample Clause" --collection case-files
libraos-cli knowledge search "termination" --collection case-files --top-k 3
libraos-cli knowledge collections
```

### config

```bash
libraos-cli config list
libraos-cli config get <profile>
libraos-cli config set <profile> --url <url> --api-key-env <ENV_VAR> [--callback-url <url>]
libraos-cli config default <profile>
libraos-cli config delete <profile>
```

### validate (offline CI gate)

```bash
libraos-cli validate ./data/
```

Walks `./data/employees/*.md` and `./data/agents/*.md`, runs the rule chain on each, exits non-zero if any issue is found. Use it as your CI pre-deploy gate.

Rules checked:

- Frontmatter parses cleanly
- `model_config.{answer,planner,skill}.primary` matches `<vendor>/<model>` shape (e.g. `Qwen/Qwen3.6-35B-A3B`)
- `custom_tools[].input_schema` recursively contains no `type: array` without `items` (catches the deterministic Vertex AI 400 class before runtime)
- `callback.url` is HTTPS (localhost is allowed for dev)
- `agent.owner_employee` references resolve within the validated folder

Exit 0 = green. Exit 1 = block deploy.

```bash
# Machine-readable (suitable for piping to jq)
libraos-cli validate ./data/ --json
```

### sync (folder → server)

```bash
# One-shot
libraos-cli sync ./data/

# Watch mode — re-run on every change, 300ms debounce
libraos-cli sync --watch ./data/

# Preview the plan without executing
libraos-cli sync --dry-run ./data/
```

Diffs `./data/employees/` and `./data/agents/` against the server, computes a plan (create/update by default, with optional `--prune` for destructive sync), and executes it.

By default this is forward-only: server-side resources missing from the folder are NOT deleted. Pass `--prune` to also delete server-side resources whose ID is absent from the folder; pair with `--dry-run` first to preview the destructive set.

```bash
libraos-cli sync ./data                      # forward-only
libraos-cli sync --prune --dry-run ./data    # preview destructive set
libraos-cli sync --prune ./data              # destructive — actually delete
```

### test-callback (Mode B webhook smoke)

Forges a LibraOS-shaped signed webhook POST to your partner endpoint. Use it to smoke-test your `WebhookRouter` handler before exposing it to live traffic.

```bash
export LIBRAOS_CB_SECRET=your-shared-hmac-secret
libraos-cli test-callback \
  --target https://partner.example.com/libraos/cb \
  --tool fetch_invoice \
  --input '{"invoice_id":"INV-9912"}'

# Same shape LibraOS's Mode B dispatcher would send. Verify your handler
# returns 200 with {"output":"...","is_error":false}.

# Test idempotency dedup — POST 3x with the same tool_use_id, your handler
# should run exactly once
libraos-cli test-callback --target ... --tool ... --repeat 3 --tool-use-id toolu_dedupe_test
```

The signature scheme is `t=<unix_ts>,v1=<hex(hmac_sha256(secret, ts + "." + tool_use_id + "." + body))>` — matches what `libraos.callbacks.WebhookRouter` (Python SDK) verifies.

| Flag | Default | Description |
|------|---------|-------------|
| `--target` | (required) | Partner endpoint URL |
| `--tool` | (required) | Tool name to send in the payload |
| `--input` | `{}` | Tool input args as a JSON object |
| `--secret-env` | `LIBRAOS_CB_SECRET` | Name of the env var holding the HMAC secret |
| `--tool-use-id` | random | Fixed `tool_use_id` (useful for idempotency tests) |
| `--agent-id` | `test-agent` | `agent_id` field in the payload |
| `--employee-id` | (empty) | `employee_id` field in the payload |
| `--repeat` | `1` | POST N times to test partner-side idempotency dedup |
| `--timeout` | `30` | Per-request timeout in seconds |

### version

```bash
libraos-cli version         # human-readable
libraos-cli version --json  # machine-readable
```

## Coming soon

- Pre-built binaries for linux/darwin/windows (amd64 + arm64)
