import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent, act } from "@testing-library/react";
import { LayoutProvider, useLayout, useDockToggle } from "./LayoutProvider";
import { DockFrame } from "./DockFrame";
import type { LayoutStorage } from "./store";

function mem(init: Record<string, string> = {}): LayoutStorage & { data: Record<string, string> } {
  const data = { ...init };
  return { data, getItem: (k) => (k in data ? data[k] : null), setItem: (k, v) => { data[k] = v; } };
}
function Probe() {
  const l = useLayout();
  return (<div>
    <span data-testid="dock">{l.dockCollapsed ? "collapsed" : "open"}</span>
    <span data-testid="width">{l.dockWidth}</span>
    <button onClick={() => l.setDockWidth(9999)}>wide</button>
    <button onClick={useDockToggle()}>palette toggle</button>
    <textarea aria-label="draft" />
  </div>);
}
// ⌘J acts on a mounted docked DockFrame; `dock: false` is a surface with no dock (kind "none")
const ui = (st = mem(), dock = true) => render(
  <LayoutProvider namespace="t" storage={st}><Probe />{dock && <DockFrame title="Copilot"><p>thread</p></DockFrame>}</LayoutProvider>);
const cmdJ = (target: EventTarget = window) => {
  const ev = new KeyboardEvent("keydown", { key: "j", metaKey: true, bubbles: true, cancelable: true });
  act(() => { target.dispatchEvent(ev); });
  return ev;
};

describe("LayoutProvider", () => {
  it("starts with the dock open on a first visit and persists a toggle", () => {
    const st = mem(); ui(st);
    expect(screen.getByTestId("dock").textContent).toBe("open");
    fireEvent.keyDown(window, { key: "j", metaKey: true });
    expect(screen.getByTestId("dock").textContent).toBe("collapsed");
    expect(st.data["t.dock.collapsed"]).toBe("1");
  });
  it("toggles with Ctrl-J both ways and ignores plain j and other modifiers", () => {
    ui();
    fireEvent.keyDown(window, { key: "j" });
    fireEvent.keyDown(window, { key: "j", metaKey: true, shiftKey: true });
    fireEvent.keyDown(window, { key: "j", ctrlKey: true, altKey: true });
    expect(screen.getByTestId("dock").textContent).toBe("open");
    fireEvent.keyDown(window, { key: "J", ctrlKey: true });
    expect(screen.getByTestId("dock").textContent).toBe("collapsed");
    fireEvent.keyDown(window, { key: "j", ctrlKey: true });
    expect(screen.getByTestId("dock").textContent).toBe("open");
  });
  it("toggles from inside a textarea and prevents the default", () => {
    ui();
    const ta = screen.getByLabelText("draft");
    const ev = new KeyboardEvent("keydown", { key: "j", metaKey: true, bubbles: true, cancelable: true });
    act(() => { ta.dispatchEvent(ev); });
    expect(ev.defaultPrevented).toBe(true);
    expect(screen.getByTestId("dock").textContent).toBe("collapsed");
    fireEvent.keyDown(ta, { key: "j" });
    expect(screen.getByTestId("dock").textContent).toBe("collapsed");
  });
  it("with no dock mounted, ⌘J changes nothing and leaves the browser's own shortcut alone", () => {
    const st = mem(); ui(st, false);
    const ev = cmdJ();
    expect(ev.defaultPrevented).toBe(false);
    expect(screen.getByTestId("dock").textContent).toBe("open");
    expect(st.data["t.dock.collapsed"]).toBeUndefined();
  });
  it("useDockToggle() toggles the dock state programmatically, dock mounted or not", () => {
    const st = mem(); ui(st, false);
    fireEvent.click(screen.getByText("palette toggle"));
    expect(screen.getByTestId("dock").textContent).toBe("collapsed");
    expect(st.data["t.dock.collapsed"]).toBe("1");
  });
  it("routes ⌘J to the most recently mounted dock and stops when it unmounts", () => {
    const st = mem();
    const { rerender } = ui(st);
    expect(cmdJ().defaultPrevented).toBe(true);
    expect(screen.getByTestId("dock").textContent).toBe("collapsed");
    rerender(<LayoutProvider namespace="t" storage={st}><Probe /></LayoutProvider>);
    expect(cmdJ().defaultPrevented).toBe(false);
    expect(screen.getByTestId("dock").textContent).toBe("collapsed");
  });
  it("clamps and persists the width", () => {
    const st = mem(); ui(st);
    fireEvent.click(screen.getByText("wide"));
    expect(screen.getByTestId("width").textContent).toBe("520");
    expect(st.data["t.dock.width"]).toBe("520");
  });
  it("throws a clear error outside the provider", () => {
    const spy = vi.spyOn(console, "error").mockImplementation(() => {});
    expect(() => render(<Probe />)).toThrow(/LayoutProvider/);
    spy.mockRestore();
  });
});
