import { describe, expect, it, vi } from "vitest";
import { LibraOSClient } from "./client";

const auth = { getAccessToken: async () => "tok" };

describe("createMessage model observability", () => {
  it("falls back to the old x-nova-* response headers", async () => {
    const fetchMock = vi.fn(async () => new Response(JSON.stringify({
      id: "msg-1",
      type: "message",
      role: "assistant",
      content: [{ type: "text", text: "answer" }],
      model: "support-assistant",
      stop_reason: "end_turn",
    }), {
      status: 200,
      headers: {
        "content-type": "application/json",
        "x-nova-model-used": "Qwen/Qwen3.6-Plus",
        "x-nova-model-fallback-triggered": "1",
      },
    }));
    const client = new LibraOSClient({ baseUrl: "http://x", auth, fetch: fetchMock as unknown as typeof fetch });

    const response = await client.createMessage({
      model: "support-assistant",
      max_tokens: 128,
      stream: false,
      messages: [{ role: "user", content: "test" }],
    });

    expect(response.model).toBe("support-assistant");
    expect(response.model_used).toBe("Qwen/Qwen3.6-Plus");
    expect(response.fallback_triggered).toBe(true);
  });

  const reply = (headers: Record<string, string>) => vi.fn(async () => new Response(JSON.stringify({
    id: "msg-1", type: "message", role: "assistant",
    content: [{ type: "text", text: "answer" }], model: "support-assistant", stop_reason: "end_turn",
  }), { status: 200, headers: { "content-type": "application/json", ...headers } }));
  const send = (fetchMock: ReturnType<typeof reply>) =>
    new LibraOSClient({ baseUrl: "http://x", auth, fetch: fetchMock as unknown as typeof fetch })
      .createMessage({ model: "support-assistant", max_tokens: 8, stream: false, messages: [{ role: "user", content: "t" }] });

  it("reads the x-libraos-* headers", async () => {
    const r = await send(reply({ "x-libraos-model-used": "m-new", "x-libraos-model-fallback-triggered": "true" }));
    expect(r.model_used).toBe("m-new");
    expect(r.fallback_triggered).toBe(true);
  });

  it("prefers the x-libraos-* headers when both are present", async () => {
    const r = await send(reply({
      "x-libraos-model-used": "m-new", "x-nova-model-used": "m-old",
      "x-libraos-model-fallback-triggered": "0", "x-nova-model-fallback-triggered": "1",
    }));
    expect(r.model_used).toBe("m-new");
    expect(r.fallback_triggered).toBe(false);
  });
});

describe("streamMessage", () => {
  it("asks for libraos.* event names and normalizes nova.* ones", async () => {
    let sent: Headers | undefined;
    const fetchMock = vi.fn(async (_url: unknown, init?: RequestInit) => {
      sent = new Headers(init?.headers);
      return new Response('data: {"type":"CUSTOM","name":"nova.search_sources","value":{}}\n\n',
        { status: 200, headers: { "content-type": "text/event-stream" } });
    });
    const client = new LibraOSClient({ baseUrl: "http://x", auth, fetch: fetchMock as unknown as typeof fetch });
    const names: string[] = [];
    for await (const ev of client.streamMessage({ model: "a", max_tokens: 8, stream: true, messages: [{ role: "user", content: "t" }] })) {
      if (ev.type === "CUSTOM") names.push(ev.name);
    }
    expect(sent?.get("x-libraos-event-names")).toBe("libraos");
    expect(names).toEqual(["libraos.search_sources"]);
  });
});

describe("end user header", () => {
  const sentHeaders = (input: unknown, init?: RequestInit) =>
    input instanceof Request ? input.headers : new Headers(init?.headers);
  const req = { model: "a", max_tokens: 8, messages: [{ role: "user" as const, content: "t" }] };

  it("createMessage sends X-End-User only when endUser is set", async () => {
    const seen: Headers[] = [];
    const fetchMock = vi.fn(async (input: unknown, init?: RequestInit) => {
      seen.push(sentHeaders(input, init));
      return new Response(JSON.stringify({ id: "m", type: "message", role: "assistant", content: [], model: "a", stop_reason: "end_turn" }),
        { status: 200, headers: { "content-type": "application/json" } });
    });
    const client = new LibraOSClient({ baseUrl: "http://x", auth, fetch: fetchMock as unknown as typeof fetch });
    await client.createMessage({ ...req, stream: false }, { endUser: "cust-42" });
    await client.createMessage({ ...req, stream: false });
    expect(seen[0]!.get("x-end-user")).toBe("cust-42");
    expect(seen[1]!.has("x-end-user")).toBe(false);
  });

  it("streamMessage sends X-End-User only when endUser is set", async () => {
    const seen: Headers[] = [];
    const fetchMock = vi.fn(async (input: unknown, init?: RequestInit) => {
      seen.push(sentHeaders(input, init));
      return new Response("", { status: 200, headers: { "content-type": "text/event-stream" } });
    });
    const client = new LibraOSClient({ baseUrl: "http://x", auth, fetch: fetchMock as unknown as typeof fetch });
    for await (const _ of client.streamMessage({ ...req, stream: true }, { endUser: "cust-42" })) { /* drain */ }
    for await (const _ of client.streamMessage({ ...req, stream: true })) { /* drain */ }
    expect(seen[0]!.get("x-end-user")).toBe("cust-42");
    expect(seen[1]!.has("x-end-user")).toBe(false);
  });
});
