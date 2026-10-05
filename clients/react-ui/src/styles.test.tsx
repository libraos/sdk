import { describe, it, expect } from "vitest";

declare global {
  var CSS_STYLES: string;
  var CSS_ALIASES: string;
}

// Use global CSS content pre-loaded by vitest setup
const css = globalThis.CSS_STYLES;
const aliases = globalThis.CSS_ALIASES;

describe("layout tokens and classes", () => {
  it("defines the layout and status tokens on .nv", () => {
    for (const t of ["--nv-nav-w:", "--nv-context-w:", "--nv-context-min:", "--nv-context-max:", "--nv-rail-w:", "--nv-danger:", "--nv-danger-ink:", "--nv-warn-bg:", "--nv-warn-ink:", "--nv-warn-line:"]) {
      expect(css).toContain(t);
    }
  });
  it("styles the shell, dock, canvas and nav rail and has both breakpoints", () => {
    for (const c of [".nv-shell", ".nv-shell__context", ".nv-dock__rail", ".nv-dock__divider", ".nv-canvas__body", ".nv-navrail"]) expect(css).toContain(c);
    expect(css).toContain("@media (max-width: 1100px)");
    expect(css).toContain("@media (max-width: 720px)");
    expect(css).toContain("prefers-reduced-motion");
  });
  it("aliases Desk's bare tokens onto --nv-*", () => {
    for (const t of ["--paper", "--surface", "--surface-2", "--ink", "--ink-soft", "--muted", "--line", "--line-strong", "--accent", "--accent-ink", "--accent-tint", "--sh-1", "--sh-2", "--sh-pop", "--r-sm", "--r", "--r-lg"]) {
      expect(aliases).toMatch(new RegExp(`${t}:\\s*var\\(--nv-`));
    }
  });
});
