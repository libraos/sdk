import { describe, it, expect } from "vitest";
import { createLayoutStore, clampDockWidth, DOCK_DEFAULT_WIDTH, DOCK_MIN_WIDTH, DOCK_MAX_WIDTH, type LayoutStorage } from "./store";

function mem(init: Record<string, string> = {}): LayoutStorage & { data: Record<string, string> } {
  const data = { ...init };
  return { data, getItem: (k) => (k in data ? data[k] : null), setItem: (k, v) => { data[k] = v; } };
}
const throwing: LayoutStorage = { getItem: () => { throw new Error("blocked"); }, setItem: () => { throw new Error("blocked"); } };

describe("createLayoutStore", () => {
  it("opens the dock and expands the nav on a first visit", () => {
    const s = createLayoutStore({ namespace: "t", storage: mem() });
    expect(s.readDockCollapsed()).toBe(false);
    expect(s.readNavCollapsed()).toBe(false);
    expect(s.readDockWidth()).toBe(DOCK_DEFAULT_WIDTH);
  });
  it("honours and writes namespaced keys", () => {
    const st = mem();
    const s = createLayoutStore({ namespace: "desk", storage: st });
    s.writeDockCollapsed(true); s.writeNavCollapsed(true); s.writeDockWidth(400);
    expect(st.data).toEqual({ "desk.dock.collapsed": "1", "desk.nav.collapsed": "1", "desk.dock.width": "400" });
    expect(s.readDockCollapsed()).toBe(true);
    expect(s.readDockWidth()).toBe(400);
  });
  it("reads legacy keys when the new key is absent, but always writes the new key", () => {
    const st = mem({ "legacydesk.copilot.collapsed": "1", "legacydesk.copilot.width": "333" });
    const s = createLayoutStore({ namespace: "desk", storage: st, legacy: { dockCollapsed: ["legacydesk.copilot.collapsed"], dockWidth: ["legacydesk.copilot.width"] } });
    expect(s.readDockCollapsed()).toBe(true);
    expect(s.readDockWidth()).toBe(333);
    s.writeDockCollapsed(false);
    expect(st.data["desk.dock.collapsed"]).toBe("0");
    expect(s.readDockCollapsed()).toBe(false);
  });
  it("clamps or defaults a garbage width", () => {
    expect(createLayoutStore({ namespace: "t", storage: mem({ "t.dock.width": "abc" }) }).readDockWidth()).toBe(DOCK_DEFAULT_WIDTH);
    expect(createLayoutStore({ namespace: "t", storage: mem({ "t.dock.width": "99999" }) }).readDockWidth()).toBe(DOCK_MAX_WIDTH);
    expect(createLayoutStore({ namespace: "t", storage: mem({ "t.dock.width": "-5" }) }).readDockWidth()).toBe(DOCK_MIN_WIDTH);
    expect(clampDockWidth(300)).toBe(300);
  });
  it("never throws when storage is blocked and keeps values in memory", () => {
    const s = createLayoutStore({ namespace: "t", storage: throwing });
    expect(s.readDockCollapsed()).toBe(false);
    expect(() => s.writeDockCollapsed(true)).not.toThrow();
    expect(s.readDockCollapsed()).toBe(true);
  });
  it("works with no storage at all (SSR / tests)", () => {
    const s = createLayoutStore({ namespace: "t", storage: null });
    s.writeNavCollapsed(true);
    expect(s.readNavCollapsed()).toBe(true);
  });
});
