import { describe, it, expect } from "vitest";
import { render, screen, fireEvent, act } from "@testing-library/react";
import { DockFrame } from "./DockFrame";
import { LayoutProvider, useLayout } from "./LayoutProvider";
import { ContextPaneProvider, useContextPane } from "./contextPane";
import { WorkspaceShell } from "./WorkspaceShell";

const mem = () => { const d: Record<string, string> = {}; return { getItem: (k: string) => d[k] ?? null, setItem: (k: string, v: string) => { d[k] = v; } }; };
function Work() {
  const pane = useContextPane(); const l = useLayout();
  return (<div>
    <button onClick={() => pane.openCanvas(() => <div>DOC 1</div>)}>open1</button>
    <button onClick={() => pane.openCanvas(() => <div>DOC 2</div>)}>open2</button>
    <button onClick={pane.closeCanvas}>close</button>
    <button onClick={pane.back} disabled={!pane.canGoBack}>back</button>
    <button onClick={pane.forward} disabled={!pane.canGoForward}>fwd</button>
    <button onClick={() => l.setDockCollapsed(true)}>collapse dock</button>
  </div>);
}
const app = () => render(
  <LayoutProvider namespace="t" storage={mem()}><ContextPaneProvider>
    <WorkspaceShell nav={<div />} context={{ kind: "dock", render: () => <div>DOCK</div> }}><Work /></WorkspaceShell>
  </ContextPaneProvider></LayoutProvider>);

describe("ContextPaneProvider", () => {
  it("a canvas pre-empts the dock and closing it restores the dock", () => {
    app();
    fireEvent.click(screen.getByText("open1"));
    expect(screen.getByRole("complementary").textContent).toBe("DOC 1");
    fireEvent.click(screen.getByText("close"));
    expect(screen.getByRole("complementary").textContent).toBe("DOCK");
  });
  it("keeps history: back and forward between opened documents", () => {
    app();
    fireEvent.click(screen.getByText("open1")); fireEvent.click(screen.getByText("open2"));
    fireEvent.click(screen.getByText("back"));
    expect(screen.getByRole("complementary").textContent).toBe("DOC 1");
    fireEvent.click(screen.getByText("fwd"));
    expect(screen.getByRole("complementary").textContent).toBe("DOC 2");
  });
  it("a dock collapsed before the canvas opened comes back collapsed", () => {
    app();
    fireEvent.click(screen.getByText("collapse dock"));
    fireEvent.click(screen.getByText("open1"));
    expect(document.querySelector(".nv-shell.is-dock-collapsed")).toBeNull();
    fireEvent.click(screen.getByText("close"));
    expect(document.querySelector(".nv-shell.is-dock-collapsed")).toBeTruthy();
  });
  it("⌘J while a canvas pre-empts the dock leaves the dock state alone", () => {
    render(
      <LayoutProvider namespace="t" storage={mem()}><ContextPaneProvider>
        <WorkspaceShell nav={<div />} context={{ kind: "dock", render: () => <DockFrame title="Copilot"><p>thread</p></DockFrame> }}><Work /></WorkspaceShell>
      </ContextPaneProvider></LayoutProvider>);
    fireEvent.click(screen.getByText("open1"));
    const ev = new KeyboardEvent("keydown", { key: "j", ctrlKey: true, bubbles: true, cancelable: true });
    act(() => { window.dispatchEvent(ev); });
    expect(ev.defaultPrevented).toBe(false);
    fireEvent.click(screen.getByText("close"));
    expect(document.querySelector(".nv-shell.is-dock-collapsed")).toBeNull();
    expect(screen.getByRole("button", { name: "Collapse Copilot" })).toBeTruthy();
  });
});
