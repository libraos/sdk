import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, act } from "@testing-library/react";
import { LayoutProvider } from "./LayoutProvider";
import type { ReactNode } from "react";
import { WorkspaceShell, type ShellLabels } from "./WorkspaceShell";
import { NavRail } from "./NavRail";
import { DockFrame } from "./DockFrame";
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
const mem = () => { const d: Record<string, string> = {}; return { d, getItem: (k: string) => d[k] ?? null, setItem: (k: string, v: string) => { d[k] = v; } }; };
const dock: ContextPane = { kind: "dock", render: () => <div>DOCK</div> };
const shell = (context: ContextPane = dock, opts: { st?: ReturnType<typeof mem>; topbar?: ReactNode; labels?: ShellLabels } = {}) => render(
  <LayoutProvider namespace="t" storage={opts.st ?? mem()}>
    <WorkspaceShell nav={<NavRail brand="B"><a href="#a">Inbox</a></NavRail>} context={context} topbar={opts.topbar} labels={opts.labels}><p>WORK</p></WorkspaceShell>
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
  it("does not crash on a none pane with no reason at all (untyped callers): it warns", () => {
    const warn = vi.spyOn(console, "warn").mockImplementation(() => {});
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    expect(() => warnIfNoReason({ kind: "none" } as any)).not.toThrow();
    expect(warn).toHaveBeenCalledWith(expect.stringMatching(/reason/));
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    expect(() => shell({ kind: "none" } as any)).not.toThrow();
    warn.mockRestore();
  });
  it("puts its own controls in a bar before the topbar, never over it, and renders no bar when empty", () => {
    const st = mem();
    const a = shell(dock, { st });
    expect(document.querySelector(".nv-shell__bar")).toBeNull(); // nothing to show
    a.unmount();
    shell(dock, { st, topbar: <span>TOPBAR</span> });
    const bar = document.querySelector(".nv-shell__bar")!;
    expect(bar.parentElement).toBe(screen.getByRole("main"));
    expect(bar.textContent).toBe("TOPBAR");
    fireEvent.click(screen.getByRole("button", { name: "Collapse navigation" }));
    const restore = screen.getByRole("button", { name: "Show navigation" });
    expect(restore.parentElement).toBe(bar);
    expect(bar.firstElementChild).toBe(restore);
    expect(bar.lastElementChild!.textContent).toBe("TOPBAR");
  });
  it("puts the hamburger in the same bar at ≤720px", () => {
    narrow = { drawer: true, sheet: true };
    shell(dock, { topbar: <span>TOPBAR</span> });
    const bar = document.querySelector(".nv-shell__bar")!;
    expect(bar.firstElementChild).toBe(screen.getByRole("button", { name: "Open navigation" }));
    expect(bar.textContent).toContain("TOPBAR");
  });
  it("in drawer mode the rail's brand button closes the drawer (focus returns) and never collapses the nav", () => {
    narrow = { drawer: true, sheet: true };
    const st = mem();
    shell(dock, { st, labels: { closeNav: "Hide menu" } });
    const burger = screen.getByRole("button", { name: "Open navigation" });
    fireEvent.click(burger);
    expect(screen.queryByRole("button", { name: "Collapse navigation" })).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: "Hide menu" }));
    expect(screen.getByRole("navigation", { hidden: true }).getAttribute("aria-hidden")).toBe("true");
    expect(document.activeElement).toBe(burger);
    expect(st.d["t.nav.collapsed"]).toBeUndefined();
    expect(document.querySelector(".nv-shell.is-nav-collapsed")).toBeNull();
  });
  it("labels the drawer close button \"Close navigation\" by default", () => {
    narrow = { drawer: true, sheet: true };
    shell();
    fireEvent.click(screen.getByRole("button", { name: "Open navigation" }));
    expect(screen.getByRole("button", { name: "Close navigation" })).toBeTruthy();
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
  it("⌘J while the nav drawer is open does nothing: the dock behind it is inert", () => {
    narrow = { drawer: true, sheet: true };
    shell({ kind: "dock", render: () => <DockFrame title="Copilot"><p>thread</p></DockFrame> });
    fireEvent.click(screen.getByRole("button", { name: "Open navigation" }));
    const ev = new KeyboardEvent("keydown", { key: "j", metaKey: true, bubbles: true, cancelable: true });
    act(() => { window.dispatchEvent(ev); });
    expect(ev.defaultPrevented).toBe(false);
    expect(screen.queryByRole("dialog", { hidden: true })?.hasAttribute("hidden")).toBe(true);
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
