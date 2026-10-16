import { describe, it, expect } from "vitest";
import { parseSse, parseAgUiStream, normalizeCustomEventName } from "../src/streaming/sse.js";
import type { AgUiEvent } from "../src/streaming/events.js";

function sseResponse(body: string): Response {
  const stream = new ReadableStream<Uint8Array>({
    start(controller) {
      controller.enqueue(new TextEncoder().encode(body));
      controller.close();
    },
  });
  return new Response(stream, {
    headers: { "content-type": "text/event-stream" },
  });
}

describe("parseSse", () => {
  it("parses framed JSON data and skips heartbeats/[DONE]", async () => {
    const body =
      ":libraos-heartbeat elapsed_ms=10\n\n" +
      ":nova-heartbeat elapsed_ms=10\n\n" +
      'data: {"type":"RUN_STARTED","threadId":"t1","runId":"r1"}\n\n' +
      'event: message\ndata: {"type":"TEXT_MESSAGE_CONTENT","messageId":"m1","delta":"hi"}\n\n' +
      "data: [DONE]\n\n";
    const frames: unknown[] = [];
    for await (const f of parseSse(sseResponse(body))) frames.push(f.data);
    expect(frames).toHaveLength(2);
    expect((frames[0] as { type: string }).type).toBe("RUN_STARTED");
  });

  it("yields typed AG-UI events via parseAgUiStream", async () => {
    const body =
      'data: {"type":"RUN_STARTED","threadId":"t","runId":"r"}\n\n' +
      'data: {"type":"TEXT_MESSAGE_CONTENT","messageId":"m","delta":"a"}\n\n' +
      'data: {"type":"RUN_FINISHED","threadId":"t","runId":"r"}\n\n';
    const events: AgUiEvent[] = [];
    for await (const ev of parseAgUiStream(sseResponse(body))) events.push(ev);
    expect(events.map((e) => e.type)).toEqual([
      "RUN_STARTED",
      "TEXT_MESSAGE_CONTENT",
      "RUN_FINISHED",
    ]);
  });

  it("preserves SSE ids and accepts the complete AG-UI vocabulary", async () => {
    const body =
      'id: 7\ndata: {"type":"REASONING_MESSAGE_CONTENT","messageId":"m","delta":"why"}\n\n' +
      'data: {"type":"TOOL_CALL_RESULT","messageId":"m","toolCallId":"t","content":"ok","role":"tool"}\n\n';
    const events = [];
    for await (const ev of parseAgUiStream(sseResponse(body))) events.push(ev);
    expect(events.map((e) => e.type)).toEqual(["REASONING_MESSAGE_CONTENT", "TOOL_CALL_RESULT"]);
    expect(events[0]?.sseId).toBe("7");
  });

  it("normalizes message-stream citation deltas into a LibraOS custom event", async () => {
    const body = 'data: {"type":"content_block_delta","delta":{"type":"citations_delta","citation":{"type":"web","cite_source":"web","web_uri":"https://example.com"}}}\n\n';
    const events = [];
    for await (const ev of parseAgUiStream(sseResponse(body))) events.push(ev);
    expect(events).toEqual([{
      type: "CUSTOM",
      name: "libraos.citations",
      value: { citations: [{ type: "web", cite_source: "web", web_uri: "https://example.com" }] },
    }]);
  });

  it("normalizes CUSTOM event names from either prefix to libraos.", async () => {
    const body =
      'data: {"type":"CUSTOM","name":"libraos.route_hint","value":{"a":1}}\n\n' +
      'data: {"type":"CUSTOM","name":"nova.route_hint","value":{"a":2}}\n\n' +
      'data: {"type":"CUSTOM","name":"nova.citations","value":{"citations":[]}}\n\n' +
      'data: {"type":"CUSTOM","name":"partner.thing","value":null}\n\n';
    const names: string[] = [];
    for await (const ev of parseAgUiStream(sseResponse(body))) {
      if (ev.type === "CUSTOM") names.push(ev.name);
    }
    expect(names).toEqual([
      "libraos.route_hint",
      "libraos.route_hint",
      "libraos.citations",
      "partner.thing",
    ]);
  });
});

describe("normalizeCustomEventName", () => {
  it("maps nova.<x> to libraos.<x> and leaves other names alone", () => {
    expect(normalizeCustomEventName("nova.done_meta")).toBe("libraos.done_meta");
    expect(normalizeCustomEventName("libraos.done_meta")).toBe("libraos.done_meta");
    expect(normalizeCustomEventName("novastar")).toBe("novastar");
  });
});
