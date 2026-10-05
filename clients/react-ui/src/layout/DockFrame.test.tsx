import { describe, it, expect, beforeEach } from "vitest";
import { render, screen, fireEvent, act } from "@testing-library/react";
import { LayoutProvider } from "./LayoutProvider";
import { DockFrame } from "./DockFrame";

type Listener = () => void;
let sheet = false; const listeners = new Set<Listener>();
beforeEach(() => {
  sheet = false; listeners.clear();
  window.matchMedia = ((q: string) => ({ get matches() { return q.includes("1100") ? sheet : false; }, media: q,
    addEventListener: (_: string, l: Listener) => listeners.add(l), removeEventListener: (_: string, l: Listener) => listeners.delete(l) })) as unknown as typeof window.matchMedia;
});
const setSheet = (v: boolean) => act(() => { sheet = v; listeners.forEach((l) => l()); });
const mem = (init: Record<string, string> = {}) => { const d = { ...init }; return { d, getItem: (k: string) => d[k] ?? null, setItem: (k: string, v: string) => { d[k] = v; } }; };
const dock = (variant?: "docked" | "chat-first" | "embedded", st = mem()) => render(
  <LayoutProvider namespace="t" storage={st}>
    <DockFrame title="Copilot" variant={variant} labels={{ name: "Copilot" }}><textarea aria-label="ask" /></DockFrame>
  </LayoutProvider>);

describe("DockFrame", () => {
  it("is open on a first visit and collapses to a labelled rail that expands again", () => {
    const st = mem(); dock("docked", st);
    expect(screen.getByLabelText("ask")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "Collapse Copilot" }));
    expect(screen.queryByLabelText("ask")).toBeNull();
    expect(st.d["t.dock.collapsed"]).toBe("1");
    fireEvent.click(screen.getByRole("button", { name: "Expand Copilot" }));
    expect(screen.getByLabelText("ask")).toBeTruthy();
  });
  it("honours a stored collapsed state", () => {
    dock("docked", mem({ "t.dock.collapsed": "1" }));
    expect(screen.getByRole("button", { name: "Expand Copilot" })).toBeTruthy();
  });
  it("resizes from the divider with arrow keys, clamped and persisted", () => {
    const st = mem(); dock("docked", st);
    const sep = screen.getByRole("separator", { name: "Resize Copilot" });
    expect(sep.getAttribute("aria-valuenow")).toBe("360");
    fireEvent.keyDown(sep, { key: "ArrowLeft" });   // dock is on the right: left = wider
    expect(sep.getAttribute("aria-valuenow")).toBe("376");
    for (let i = 0; i < 40; i++) fireEvent.keyDown(sep, { key: "ArrowLeft" });
    expect(sep.getAttribute("aria-valuenow")).toBe("520");
    expect(st.d["t.dock.width"]).toBe("520");
  });
  it("resizes by mouse drag", () => {
    dock();
    const sep = screen.getByRole("separator", { name: "Resize Copilot" });
    fireEvent.mouseDown(sep, { clientX: 1000 });
    fireEvent.mouseMove(document, { clientX: 960 });
    fireEvent.mouseUp(document);
    expect(sep.getAttribute("aria-valuenow")).toBe("400");
  });
  it("chat-first has no collapse or resize; embedded has no header", () => {
    const a = dock("chat-first");
    expect(screen.queryByRole("button", { name: "Collapse Copilot" })).toBeNull();
    expect(screen.queryByRole("separator")).toBeNull();
    a.unmount();
    dock("embedded");
    expect(screen.queryByText("Copilot")).toBeNull();
    expect(screen.getByLabelText("ask")).toBeTruthy();
  });
  it("becomes a sheet at ≤1100px: a launcher opens a modal dialog, Escape closes it, focus returns", () => {
    sheet = true; dock();
    expect(screen.queryByLabelText("ask")).toBeNull();
    const launcher = screen.getByRole("button", { name: "Open Copilot" });
    fireEvent.click(launcher);
    const dlg = screen.getByRole("dialog", { name: "Copilot" });
    expect(dlg.getAttribute("aria-modal")).toBe("true");
    expect(dlg.contains(document.activeElement)).toBe(true);
    fireEvent.keyDown(window, { key: "Escape" });
    expect(screen.queryByRole("dialog")).toBeNull();
    // the launcher re-mounts after the sheet closes: re-query it
    expect(document.activeElement).toBe(screen.getByRole("button", { name: "Open Copilot" }));
  });
  it("leaving the sheet breakpoint while the sheet is open returns to the docked frame", () => {
    sheet = true; dock();
    fireEvent.click(screen.getByRole("button", { name: "Open Copilot" }));
    setSheet(false);
    expect(screen.queryByRole("dialog")).toBeNull();
    expect(screen.getByLabelText("ask")).toBeTruthy();
  });
});
