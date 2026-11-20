import { describe, it, expect, vi } from "vitest";
import { LibraOSClient } from "./client";
import { LibraOSApiError } from "./errors";

const auth = { getAccessToken: async () => "tok" };
const mk = (b: unknown, s = 200) =>
  new Response(JSON.stringify(b), { status: s, headers: { "content-type": "application/json" } });

const client = (fetchMock: unknown) =>
  new LibraOSClient({ baseUrl: "http://x", auth, fetch: fetchMock as unknown as typeof fetch });

const call = (fetchMock: { mock: { calls: unknown[][] } }, i = 0) =>
  fetchMock.mock.calls[i] as unknown as [string, RequestInit];

const commit = "0123456789abcdef0123456789abcdef01234567";

const rawPending = {
  id: "req-1", user_id: "alice", url: "https://github.com/mvanhorn/last30days-skill",
  repo: "mvanhorn/last30days-skill", note: "market research", status: "pending", created_at: "t1",
};

const rawApproved = {
  ...rawPending, status: "approved", decided_by: "ada", decided_at: "t2", commit, license: "MIT",
  skills: [{ name: "last30days", version: 1, sha256: "s1" }],
};

const rawSkill = {
  name: "last30days", version: 1, sha256: "s1", request_id: "req-1", activated_by: "ada",
  activated_at: "t2", status: "active", description: "Research the last 30 days.",
  source: `github.com/mvanhorn/last30days-skill@${commit}/skills/last30days`,
};

/**
 * A person asks for a skill from a GitHub link; an admin of their org
 * previews it at a pinned commit and approves or rejects it.
 */
describe("user skills, the person's own", () => {
  it("createSkillRequest posts the link and note, maps the request and keeps `created`", async () => {
    const fetchMock = vi.fn(async () => mk({ request: rawPending, created: true }, 201));
    const out = await client(fetchMock).createSkillRequest(rawPending.url, { note: "market research" });
    expect(out).toEqual({
      created: true,
      request: {
        id: "req-1", userId: "alice", url: rawPending.url, repo: "mvanhorn/last30days-skill",
        note: "market research", status: "pending", createdAt: "t1", skills: [],
      },
    });
    const [url, init] = call(fetchMock);
    expect(url).toBe("http://x/v1/skill-requests");
    expect(init.method).toBe("POST");
    // The person comes from the token; the body names no one.
    expect(JSON.parse(init.body as string)).toEqual({ url: rawPending.url, note: "market research" });
  });

  it("an existing pending request for the same link comes back with created: false", async () => {
    const fetchMock = vi.fn(async () => mk({ request: rawPending, created: false }));
    const out = await client(fetchMock).createSkillRequest(rawPending.url);
    expect(out.created).toBe(false);
    expect(JSON.parse(call(fetchMock)[1].body as string)).toEqual({ url: rawPending.url });
  });

  it("listMySkillRequests filters by status and limit and maps an approval", async () => {
    const fetchMock = vi.fn(async () => mk({ data: [rawApproved] }));
    const [req] = await client(fetchMock).listMySkillRequests({ status: "approved", limit: 5 });
    expect(call(fetchMock)[0]).toBe("http://x/v1/skill-requests?status=approved&limit=5");
    expect(req).toMatchObject({
      status: "approved", decidedBy: "ada", decidedAt: "t2", commit, license: "MIT",
      skills: [{ name: "last30days", version: 1, sha256: "s1" }],
    });
  });

  it("getMySkillRequest and withdrawSkillRequest unwrap {request} and encode the id", async () => {
    const fetchMock = vi.fn(async () => mk({ request: { ...rawPending, status: "withdrawn", decided_by: "alice" } }));
    const c = client(fetchMock);
    await c.getMySkillRequest("req 1");
    const withdrawn = await c.withdrawSkillRequest("req 1");
    expect(call(fetchMock, 0)[0]).toBe("http://x/v1/skill-requests/req%201");
    expect(call(fetchMock, 0)[1].method).toBe("GET");
    expect(call(fetchMock, 1)[0]).toBe("http://x/v1/skill-requests/req%201");
    expect(call(fetchMock, 1)[1].method).toBe("DELETE");
    expect(withdrawn).toMatchObject({ status: "withdrawn", decidedBy: "alice" });
  });

  it("listMyUserSkills maps the pinned versions; an unknown status reads as unavailable", async () => {
    const fetchMock = vi.fn(async () => mk({
      data: [rawSkill, { ...rawSkill, name: "other", status: "paused", reason: "?" }],
    }));
    const out = await client(fetchMock).listMyUserSkills();
    expect(call(fetchMock)[0]).toBe("http://x/v1/user-skills");
    expect(out[0]).toEqual({
      name: "last30days", version: 1, sha256: "s1", requestId: "req-1", activatedBy: "ada",
      activatedAt: "t2", status: "active", reason: undefined, description: "Research the last 30 days.",
      source: rawSkill.source,
    });
    expect(out[1]?.status).toBe("unavailable");
  });

  it("removeMyUserSkill DELETEs by name", async () => {
    const fetchMock = vi.fn(async () => new Response(null, { status: 204 }));
    await client(fetchMock).removeMyUserSkill("last30days");
    const [url, init] = call(fetchMock);
    expect(url).toBe("http://x/v1/user-skills/last30days");
    expect(init.method).toBe("DELETE");
  });

  it("absent lists degrade to empty, not undefined", async () => {
    expect(await client(vi.fn(async () => mk({}))).listMySkillRequests()).toEqual([]);
    expect(await client(vi.fn(async () => mk({}))).listMyUserSkills()).toEqual([]);
  });

  // A service client or API key is not a person: the 403 must reach the caller.
  it("surfaces the 403 a service client or API key gets", async () => {
    const body = { error: { type: "forbidden", message: "user skills belong to a signed-in person" } };
    await expect(client(vi.fn(async () => mk(body, 403))).listMyUserSkills())
      .rejects.toMatchObject({ status: 403, body });
  });
});

describe("user skills, the org admin's review", () => {
  it("listSkillRequests filters by status, person and limit", async () => {
    const fetchMock = vi.fn(async () => mk({ data: [rawPending] }));
    const out = await client(fetchMock).listSkillRequests({ status: "pending", userId: "alice", limit: 10 });
    expect(call(fetchMock)[0]).toBe("http://x/v1/managed/skill-requests?status=pending&user_id=alice&limit=10");
    expect(out.map((r) => r.id)).toEqual(["req-1"]);
  });

  it("previewSkillRequest maps the candidates, left-out files and catalog placement", async () => {
    const fetchMock = vi.fn(async () => mk({
      request: rawPending, repo: "mvanhorn/last30days-skill", ref: "", commit, license: "MIT",
      skills: [
        {
          name: "last30days", path: "skills/last30days", description: "Research.", body: "Search.",
          sha256: "s1", files: ["references/synthesis.md"], catalog: "published", catalog_version: 3,
          left_out: [{ path: "scripts/last30days.py", reason: "script: LibraOS never runs scripts" }],
        },
        { path: "skills/broken", error: "SKILL.md must start with YAML frontmatter" },
      ],
    }));
    const out = await client(fetchMock).previewSkillRequest("req-1");
    const [url, init] = call(fetchMock);
    expect(url).toBe("http://x/v1/managed/skill-requests/req-1/preview");
    expect(init.method).toBe("POST");
    expect(out.commit).toBe(commit);
    expect(out.request.id).toBe("req-1");
    expect(out.skills[0]).toMatchObject({
      name: "last30days", files: ["references/synthesis.md"], catalog: "published", catalogVersion: 3,
      leftOut: [{ path: "scripts/last30days.py", reason: "script: LibraOS never runs scripts" }],
    });
    expect(out.skills[1]).toMatchObject({ path: "skills/broken", files: [], leftOut: [], catalog: undefined });
  });

  it("approveSkillRequest sends the previewed commit, and skills only when named", async () => {
    const fetchMock = vi.fn(async () => mk({ request: rawApproved }));
    const c = client(fetchMock);
    const approved = await c.approveSkillRequest("req-1", commit);
    await c.approveSkillRequest("req-1", commit, { skills: ["last30days"] });
    expect(call(fetchMock, 0)[0]).toBe("http://x/v1/managed/skill-requests/req-1/approve");
    expect(JSON.parse(call(fetchMock, 0)[1].body as string)).toEqual({ commit });
    expect(JSON.parse(call(fetchMock, 1)[1].body as string)).toEqual({ commit, skills: ["last30days"] });
    expect(approved.skills).toEqual([{ name: "last30days", version: 1, sha256: "s1" }]);
  });

  it("an approval the org's catalog refuses surfaces name_taken in the error body", async () => {
    const body = { error: { type: "name_taken", message: "the org already uses the skill name", field: "skills" } };
    const err = await client(vi.fn(async () => mk(body, 409))).approveSkillRequest("req-1", commit).catch((e) => e);
    expect(err).toBeInstanceOf(LibraOSApiError);
    expect(err).toMatchObject({ status: 409, body });
  });

  it("rejectSkillRequest sends the reason", async () => {
    const fetchMock = vi.fn(async () => mk({ request: { ...rawPending, status: "rejected", reason: "No." } }));
    const out = await client(fetchMock).rejectSkillRequest("req-1", "No.");
    expect(call(fetchMock)[0]).toBe("http://x/v1/managed/skill-requests/req-1/reject");
    expect(JSON.parse(call(fetchMock)[1].body as string)).toEqual({ reason: "No." });
    expect(out).toMatchObject({ status: "rejected", reason: "No." });
  });

  it("listUserSkills filters by person, name and limit and keeps whose each skill is", async () => {
    const fetchMock = vi.fn(async () => mk({ data: [{ ...rawSkill, user_id: "alice" }] }));
    const c = client(fetchMock);
    const out = await c.listUserSkills({ userId: "alice", name: "last30days", limit: 2 });
    await c.listUserSkills();
    expect(call(fetchMock, 0)[0]).toBe("http://x/v1/managed/user-skills?user_id=alice&name=last30days&limit=2");
    expect(call(fetchMock, 1)[0]).toBe("http://x/v1/managed/user-skills");
    expect(out[0]).toMatchObject({ userId: "alice", name: "last30days", status: "active" });
  });

  // A non-admin is refused by the route gate, whose body is a plain string.
  it("surfaces the route gate's 403 admin_required on an admin method", async () => {
    const body = { error: "admin_required" };
    await expect(client(vi.fn(async () => mk(body, 403))).listUserSkills())
      .rejects.toMatchObject({ status: 403, body });
  });

  it("removeUserSkill DELETEs the person's skill by name, naming the person in user_id", async () => {
    const fetchMock = vi.fn(async () => new Response(null, { status: 204 }));
    await client(fetchMock).removeUserSkill("alice@acme", "last30days");
    const [url, init] = call(fetchMock);
    expect(url).toBe("http://x/v1/managed/user-skills/last30days?user_id=alice%40acme");
    expect(init.method).toBe("DELETE");
  });
});
