import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { CanvasFrame } from "./CanvasFrame";
describe("CanvasFrame", () => {
  it("renders a header with close and a version bar, and one scroll container around the body", () => {
    const onClose = vi.fn(), prev = vi.fn(), next = vi.fn();
    render(<CanvasFrame title="Offer letter" onClose={onClose} versionIndex={1} versionCount={3} onPrevVersion={prev} onNextVersion={next}><p>BODY</p></CanvasFrame>);
    expect(screen.getByText("Version 2 of 3")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "Previous version" })); expect(prev).toHaveBeenCalled();
    fireEvent.click(screen.getByRole("button", { name: "Next version" })); expect(next).toHaveBeenCalled();
    fireEvent.click(screen.getByRole("button", { name: "Close canvas" })); expect(onClose).toHaveBeenCalled();
    const body = screen.getByText("BODY").closest(".nv-canvas__body");
    expect(body).toBeTruthy();
    expect(document.querySelectorAll(".nv-canvas__body").length).toBe(1);
  });
  it("hides the version bar for a single version and disables the ends", () => {
    const { rerender } = render(<CanvasFrame title="T" onClose={() => {}} versionIndex={0} versionCount={1}><p>x</p></CanvasFrame>);
    expect(screen.queryByText(/Version/)).toBeNull();
    rerender(<CanvasFrame title="T" onClose={() => {}} versionIndex={0} versionCount={2} onPrevVersion={() => {}} onNextVersion={() => {}}><p>x</p></CanvasFrame>);
    expect((screen.getByRole("button", { name: "Previous version" }) as HTMLButtonElement).disabled).toBe(true);
    expect((screen.getByRole("button", { name: "Next version" }) as HTMLButtonElement).disabled).toBe(false);
  });
  it("closes on Escape, but not on an Escape a sheet or drawer already handled", () => {
    const onClose = vi.fn();
    render(<CanvasFrame title="T" onClose={onClose}><p>x</p></CanvasFrame>);
    const handled = (e: KeyboardEvent) => e.preventDefault();
    window.addEventListener("keydown", handled, true);
    fireEvent.keyDown(window, { key: "Escape" });
    expect(onClose).not.toHaveBeenCalled();
    window.removeEventListener("keydown", handled, true);
    fireEvent.keyDown(window, { key: "Escape" });
    expect(onClose).toHaveBeenCalledTimes(1);
  });
  it("closes on an Escape from inside the canvas or from the page body, not from the work pane or a composition", () => {
    const onClose = vi.fn();
    render(<><input aria-label="search" /><CanvasFrame title="T" onClose={onClose}><textarea aria-label="draft" /></CanvasFrame></>);
    fireEvent.keyDown(screen.getByLabelText("search"), { key: "Escape" }); // a work-pane field (or a product modal)
    expect(onClose).not.toHaveBeenCalled();
    fireEvent.keyDown(screen.getByLabelText("draft"), { key: "Escape", isComposing: true }); // an IME cancel
    expect(onClose).not.toHaveBeenCalled();
    fireEvent.keyDown(screen.getByLabelText("draft"), { key: "Escape" });
    expect(onClose).toHaveBeenCalledTimes(1);
    fireEvent.keyDown(document.body, { key: "Escape" });
    expect(onClose).toHaveBeenCalledTimes(2);
  });
});
