import { describe, it, expect, vi } from "vitest";
import { LibraOSClient } from "../src/index.js";

// A job stream as the server sends it: the job's own events with SSE ids,
// not AG-UI. streamJob used to parse it as AG-UI and yield nothing.
const body = [
  'id: 1\nevent: text\ndata: {"turn": 0, "type": "text", "content": "yes"}\n\n',
  ":nova-heartbeat elapsed_ms=10000\n\n",
  'id: 2\nevent: response_complete\ndata: {"turn": 0, "type": "response_complete", "content": "yes"}\n\n',
  'id: 3\nevent: done\ndata: {"turn": 0, "type": "done", "content": "yes", "metadata": {"status": "done"}}\n\n',
].join("");

describe("streamJob", () => {
  it("yields the job's events, with done.status at the top level", async () => {
    const fetchMock = vi.fn(async (_url: unknown, _init?: RequestInit) =>
      new Response(body, { status: 200, headers: { "content-type": "text/event-stream" } }),
    );
    const client = new LibraOSClient({ baseUrl: "https://libraos.example", fetch: fetchMock as unknown as typeof fetch });
    const events = [];
    for await (const ev of client.streamJob("job_1", "0")) events.push(ev as Record<string, unknown>);

    expect(events.map((e) => e.type)).toEqual(["text", "response_complete", "done"]);
    expect(events[0]?.content).toBe("yes");
    expect(events[2]?.status).toBe("done");

    const [url, init] = fetchMock.mock.calls[0] as [string, RequestInit];
    expect(String(url)).toContain("/v1/managed/agents/jobs/job_1/stream");
    const headers = new Headers(init.headers);
    expect(headers.get("last-event-id")).toBe("0");
    expect(headers.get("x-protocol")).toBeNull();
  });
});
