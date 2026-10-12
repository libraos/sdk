import { describe, it, expect } from "vitest";
import { exportFilename, exportStem, registerArtifactKind, describeArtifactKind } from "./artifacts";
describe("export helpers", () => {
  it("names a markdown export after its first H1, else its first line, else the fallback", () => {
    expect(exportFilename("# Q3 Launch Plan\n\nbody", "draft")).toBe("q3-launch-plan");
    expect(exportFilename("Intro line\nmore", "draft")).toBe("intro-line");
    expect(exportFilename("\n\n", "draft")).toBe("draft");
    expect(exportFilename("# **Bold** `code` > quote", "x")).toBe("bold-code-quote");
    expect(exportFilename("# " + "a".repeat(80), "x")).toHaveLength(60);
  });
  it("uses a custom kind's own title for its stem", () => {
    registerArtifactKind({ id: "sheet", body: "custom", title: (c) => c.split("\n")[1] ?? "" });
    expect(describeArtifactKind("sheet").body).toBe("custom");
    expect(exportStem("sheet", "```sheet\nPipeline Q4\n", "fallback")).toBe("pipeline-q4");
    expect(exportStem("unknown-kind", "# Memo", "fallback")).toBe("memo");
    expect(describeArtifactKind("unknown-kind").body).toBe("markdown");
  });
});
