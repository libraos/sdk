export interface ArtifactKindDescriptor { id: string; body: "markdown" | "custom"; title(content: string): string }
const registry = new Map<string, ArtifactKindDescriptor>();
const MARKDOWN: ArtifactKindDescriptor = { id: "markdown", body: "markdown", title: () => "" };
export function registerArtifactKind(d: ArtifactKindDescriptor): void { registry.set(d.id, d); }
export function describeArtifactKind(id: string): ArtifactKindDescriptor { return registry.get(id) ?? MARKDOWN; }
function slugify(raw: string): string {
  return raw.trim().toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 60);
}
/** Name an export after its content: the first H1, else the first non-empty line, else `fallback`. */
export function exportFilename(markdown: string, fallback: string): string {
  const md = markdown ?? "";
  const h1 = md.match(/^#\s+(.+)$/m);
  const line = md.split("\n").find((l) => l.trim());
  return slugify((h1 ? h1[1] : line ?? "").replace(/[#*`>_]/g, "")) || fallback;
}
/** A custom-body kind names its export from its own title; markdown keeps the H1 rule. */
export function exportStem(kind: string, content: string, fallback: string): string {
  const d = describeArtifactKind(kind);
  if (d.body === "custom") return slugify(d.title(content)) || fallback;
  return exportFilename(content, fallback);
}
