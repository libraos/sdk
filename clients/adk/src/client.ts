// LibraAdk — the control-plane + data-plane client. `deploy` writes the agent
// to `/v1/agents`; `run` executes it on the LibraOS managed runtime and streams
// events. v1 targets the durable jobs surface (works today); the exact wire
// shapes are the documented mapping (docs/design/agent-sdk-rfc.md §5) — confirm
// against the server before GA.

import type { Agent } from "./agent.js";

export interface LibraAdkOptions {
  /** LibraOS base URL. Defaults to $LIBRA_OS_URL. */
  baseUrl?: string;
  /** Bearer token / agent API key. Defaults to $LIBRA_OS_API_KEY. */
  apiKey?: string;
  /** Custom fetch (tests / non-Node runtimes). */
  fetch?: typeof fetch;
}

/** A single event streamed from a LibraOS agent run. */
export interface RunEvent {
  type: string;
  [key: string]: unknown;
}

export interface DeployResult {
  id: string;
  etag?: string;
}

export interface RunOptions {
  onEvent?: (event: RunEvent) => void;
  signal?: AbortSignal;
}

const env = (k: string): string | undefined =>
  typeof process !== "undefined" ? process.env[k] : undefined;

/** Value of the managed-agents beta header sent on /v1/agents (older servers require it; current ones ignore it). */
const MANAGED_AGENTS_BETA = "managed-agents-2026-04-01";

export class LibraAdk {
  private readonly baseUrl: string;
  private readonly apiKey: string;
  private readonly doFetch: typeof fetch;

  constructor(opts: LibraAdkOptions = {}) {
    const baseUrl = opts.baseUrl ?? env("LIBRA_OS_URL");
    const apiKey = opts.apiKey ?? env("LIBRA_OS_API_KEY");
    if (!baseUrl) throw new Error("LibraAdk: baseUrl (or $LIBRA_OS_URL) is required");
    if (!apiKey) throw new Error("LibraAdk: apiKey (or $LIBRA_OS_API_KEY) is required");
    this.baseUrl = baseUrl.replace(/\/+$/, "");
    this.apiKey = apiKey;
    this.doFetch = opts.fetch ?? fetch;
  }

  private headers(): Record<string, string> {
    return { authorization: `Bearer ${this.apiKey}`, "content-type": "application/json" };
  }

  /** Older servers require the managed-agents beta header on /v1/agents (426 without it); current ones accept and ignore it. */
  private agentHeaders(): Record<string, string> {
    return { ...this.headers(), "anthropic-beta": MANAGED_AGENTS_BETA };
  }

  /**
   * Create or update the agent on the LibraOS control plane. Updates with
   * `PUT /v1/agents/:name`; a new agent (404) is created with `POST /v1/agents`.
   * Idempotent — safe to re-run on deploy.
   */
  async deploy(agent: Agent): Promise<DeployResult> {
    const name = agent.definition.name;
    const body = agent.toManagedAgentBody();
    let res = await this.doFetch(`${this.baseUrl}/v1/agents/${encodeURIComponent(name)}`, {
      method: "PUT",
      headers: this.agentHeaders(),
      body: JSON.stringify(body),
    });
    if (res.status === 404) {
      res = await this.doFetch(`${this.baseUrl}/v1/agents`, {
        method: "POST",
        headers: this.agentHeaders(),
        body: JSON.stringify({ id: name, ...body }),
      });
    }
    if (!res.ok) throw new Error(`deploy ${name}: ${res.status} ${await safeText(res)}`);
    const j = (await res.json().catch(() => ({}))) as { id?: string; etag?: string };
    return { id: j.id ?? name, ...(j.etag ? { etag: j.etag } : {}) };
  }

  /**
   * Run an agent on the LibraOS stack and stream its events. Targets the
   * durable jobs surface (`POST /agents/v1/:key/jobs` + `…/jobs/:id/stream`) —
   * resumable + SSE today. Once the P0 seam lands (libraos/libraos#840/#841)
   * this can move to the session surface for full Managed-Agents compat.
   */
  async run(agentName: string, input: string, opts: RunOptions = {}): Promise<RunEvent[]> {
    // The path names the agent; the API key goes in the Authorization header.
    const key = encodeURIComponent(agentName);
    const submit = await this.doFetch(`${this.baseUrl}/agents/v1/${key}/jobs`, {
      method: "POST",
      headers: this.headers(),
      body: JSON.stringify({ message: input }),
      ...(opts.signal ? { signal: opts.signal } : {}),
    });
    if (!submit.ok) throw new Error(`run ${agentName}: submit ${submit.status} ${await safeText(submit)}`);
    const submitted = (await submit.json().catch(() => ({}))) as { job_id?: string };
    if (!submitted.job_id) throw new Error(`run ${agentName}: server did not return a job_id`);

    const stream = await this.doFetch(`${this.baseUrl}/agents/v1/${key}/jobs/${submitted.job_id}/stream`, {
      headers: { authorization: `Bearer ${this.apiKey}`, accept: "text/event-stream" },
      ...(opts.signal ? { signal: opts.signal } : {}),
    });
    if (!stream.ok || !stream.body) throw new Error(`run ${agentName}: stream ${stream.status}`);

    const events: RunEvent[] = [];
    for await (const ev of parseSSE(stream.body)) {
      events.push(ev);
      opts.onEvent?.(ev);
    }
    return events;
  }
}

async function safeText(res: Response): Promise<string> {
  try {
    return await res.text();
  } catch {
    return "";
  }
}

/** Minimal SSE parser over a web ReadableStream of bytes. */
async function* parseSSE(body: ReadableStream<Uint8Array>): AsyncGenerator<RunEvent> {
  const reader = body.getReader();
  const decoder = new TextDecoder();
  let buf = "";
  for (;;) {
    const { value, done } = await reader.read();
    if (done) break;
    buf += decoder.decode(value, { stream: true });
    let idx = buf.indexOf("\n\n");
    while (idx !== -1) {
      const ev = frameToEvent(buf.slice(0, idx));
      buf = buf.slice(idx + 2);
      if (ev) yield ev;
      idx = buf.indexOf("\n\n");
    }
  }
}

function frameToEvent(frame: string): RunEvent | undefined {
  let type = "message";
  const data: string[] = [];
  for (const line of frame.split("\n")) {
    if (line.startsWith("event:")) type = line.slice(6).trim();
    else if (line.startsWith("data:")) data.push(line.slice(5).trim());
  }
  if (data.length === 0) return undefined;
  const raw = data.join("\n");
  try {
    const parsed = JSON.parse(raw) as Record<string, unknown>;
    const parsedType = typeof parsed.type === "string" ? parsed.type : type;
    return { ...parsed, type: parsedType };
  } catch {
    return { type, data: raw };
  }
}
