import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, act } from "@testing-library/react";
import { LayoutProvider } from "./LayoutProvider";
import { WorkspaceShell } from "./WorkspaceShell";
import { NavRail } from "./NavRail";
import { resolveContextPane, warnIfNoReason, type ContextPane } from "./contextPane";

type Listener = () => void;
let narrow = { drawer: false, sheet: false };
const listeners = new Set<Listener>();
beforeEach(() => {
  narrow = { drawer: false, sheet: false }; listeners.clear();
  window.matchMedia = ((q: string) => ({
    get matches() { return q.includes("720") ? narrow.drawer : q.includes("1100") ? narrow.sheet : false; },
    media: q, addEventListener: (_: string, l: Listener) => listeners.add(l), removeEventListener: (_: string, l: Listener) => listeners.delete(l),
  })) as unknown as typeof window.matchMedia;
});
const setNarrow = (n: typeof narrow) => act(() => { narrow = n; listeners.forEach((l) => l()); });
const mem = () => { const d: Record<string, string> = {}; return { getItem: (k: string) => d[k] ?? null, setItem: (k: string, v: string) => { d[k] = v; } }; };
const dock: ContextPane = { kind: "dock", render: () => <div>DOCK</div> };
const shell = (context: ContextPane = dock) => render(
  <LayoutProvider namespace="t" storage={mem()}>
    <WorkspaceShell nav={<NavRail brand="B"><a href="#a">Inbox</a></NavRail>} context={context}><p>WORK</p></WorkspaceShell>
  </LayoutProvider>);

describe("resolveContextPane", () => {
  it("canvas beats dock beats none", () => {
    const canvas = { render: () => "C", onClose: () => {} };
    expect(resolveContextPane(dock, canvas).kind).toBe("canvas");
    expect(resolveContextPane(dock, null).kind).toBe("dock");
    expect(resolveContextPane({ kind: "none", reason: "admin" }, canvas).kind).toBe("canvas");
  });
});

describe("WorkspaceShell", () => {
  it("renders the three landmarks with the dock pane", () => {
    shell();
    expect(screen.getByRole("navigation")).toBeTruthy();
    expect(screen.getByRole("main").textContent).toContain("WORK");
    expect(screen.getByRole("complementary").textContent).toBe("DOCK");
    expect(document.querySelector(".nv-shell--dock")).toBeTruthy();
  });
  it("feeds the stored dock width to --nv-dock-w and leaves --nv-context-w to the stylesheet", () => {
    shell();
    const el = document.querySelector<HTMLElement>(".nv-shell")!;
    expect(el.style.getPropertyValue("--nv-dock-w")).toBe("360px");
    expect(el.style.getPropertyValue("--nv-context-w")).toBe("");
  });
  it("has no aside for a declared none, and warns in dev when the reason is empty", () => {
    const warn = vi.spyOn(console, "warn").mockImplementation(() => {});
    shell({ kind: "none", reason: "admin console" });
    expect(screen.queryByRole("complementary")).toBeNull();
    expect(warn).not.toHaveBeenCalled();
    shell({ kind: "none", reason: " " });
    expect(warn).toHaveBeenCalledWith(expect.stringMatching(/reason/));
    warn.mockRestore();
  });
  it("does not warn in a production build even with an empty reason", () => {
    const warn = vi.spyOn(console, "warn").mockImplementation(() => {});
    vi.stubEnv("NODE_ENV", "production");
    warnIfNoReason({ kind: "none", reason: " " });
    expect(warn).not.toHaveBeenCalled();
    vi.unstubAllEnvs();
    warn.mockRestore();
  });
  it("collapses the nav from the rail and restores it from the work area", () => {
    shell();
    fireEvent.click(screen.getByRole("button", { name: "Collapse navigation" }));
    expect(document.querySelector(".nv-shell.is-nav-collapsed")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "Show navigation" }));
    expect(document.querySelector(".nv-shell.is-nav-collapsed")).toBeNull();
  });
  it("turns the nav into a drawer at ≤720px: inert when closed, Escape and backdrop close, focus returns", () => {
    narrow = { drawer: true, sheet: true };
    shell();
    const nav = screen.getByRole("navigation", { hidden: true });
    expect(nav.getAttribute("aria-hidden")).toBe("true");
    expect(nav.hasAttribute("inert")).toBe(true);
    const burger = screen.getByRole("button", { name: "Open navigation" });
    fireEvent.click(burger);
    expect(nav.getAttribute("aria-hidden")).toBeNull();
    const main = screen.getByRole("main", { hidden: true });
    expect(main.hasAttribute("inert")).toBe(true);
    fireEvent.keyDown(window, { key: "Escape" });
    expect(nav.getAttribute("aria-hidden")).toBe("true");
    expect(main.hasAttribute("inert")).toBe(false);
    expect(document.activeElement).toBe(burger);
    fireEvent.click(burger);
    fireEvent.click(document.querySelector(".nv-shell__backdrop")!);
    expect(nav.getAttribute("aria-hidden")).toBe("true");
  });
  it("leaving the narrow breakpoint closes the drawer and un-inerts the nav", () => {
    narrow = { drawer: true, sheet: true };
    shell();
    fireEvent.click(screen.getByRole("button", { name: "Open navigation" }));
    setNarrow({ drawer: false, sheet: false });
    const nav = screen.getByRole("navigation");
    expect(nav.hasAttribute("inert")).toBe(false);
    expect(document.querySelector(".nv-shell.is-drawer-open")).toBeNull();
  });
});
