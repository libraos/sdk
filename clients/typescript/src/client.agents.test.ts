import { describe, it, expect, vi } from "vitest";
import { NovaClient } from "./client";

const auth = { getAccessToken: async () => "tok" };
const mk = (b: unknown, s = 200) =>
  new Response(JSON.stringify(b), { status: s, headers: { "content-type": "application/json" } });

describe("listAgents", () => {
  it("sends the managed-agents beta header and unwraps {data}", async () => {
    let capturedRequest: Request | undefined;
    const fetchMock = vi.fn(async (req: Request) => {
      capturedRequest = req;
      return mk({ data: [{ id: "marketing-assistant", name: "Marketing", agent_type: "persona", brain: true }] });
    });
    const client = new NovaClient({ baseUrl: "http://x", auth, fetch: fetchMock as unknown as typeof fetch });

    const agents = await client.listAgents();

    expect(agents).toEqual([
      { id: "marketing-assistant", name: "Marketing", agent_type: "persona", brain: true },
    ]);
    expect(capturedRequest!.url).toContain("/v1/agents");
    expect(capturedRequest!.headers.get("anthropic-beta")).toBe("managed-agents-2026-04-01");
  });
});
