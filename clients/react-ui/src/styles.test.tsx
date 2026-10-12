import { describe, it, expect } from "vitest";
import css from "./styles.css?raw";
import aliases from "./aliases.css?raw";

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
  it("collapses the dock column to the rail: the inline width feeds --nv-dock-w, not --nv-context-w", () => {
    // the shell's inline style sets --nv-dock-w; --nv-context-w is derived from it in CSS,
    // so the collapsed-state override is not beaten by an inline declaration
    expect(css).toMatch(/\.nv-shell\s*\{[^}]*--nv-context-w:\s*var\(--nv-dock-w/);
    expect(css).toMatch(/\.nv-shell\.is-dock-collapsed\s*\{[^}]*--nv-context-w:\s*var\(--nv-rail-w\)/);
    expect(css).toMatch(/\.nv-dock--sheet\s*\{[^}]*width:[^;]*var\(--nv-dock-w/);
  });
  it("lays the shell's own controls out in a bar, not absolutely over the topbar", () => {
    expect(css).toContain(".nv-shell__bar");
    expect(css).not.toMatch(/\.nv-shell__(hamburger|nav-restore)[^{]*\{[^}]*position:\s*absolute/);
  });
  it("aliases Desk's bare tokens onto --nv-*", () => {
    for (const t of ["--paper", "--surface", "--surface-2", "--ink", "--ink-soft", "--muted", "--line", "--line-strong", "--accent", "--accent-ink", "--accent-tint", "--sh-1", "--sh-2", "--sh-pop", "--r-sm", "--r", "--r-lg"]) {
      expect(aliases).toMatch(new RegExp(`${t}:\\s*var\\(--nv-`));
    }
  });
});
