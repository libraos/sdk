import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from "react";
import { clampDockWidth, createLayoutStore, type LayoutStorage, type LegacyKeys } from "./store";

export interface LayoutState {
  navCollapsed: boolean; setNavCollapsed(v: boolean): void;
  dockCollapsed: boolean; setDockCollapsed(v: boolean): void; toggleDock(): void;
  dockWidth: number; setDockWidth(px: number): void;
}
const Ctx = createContext<LayoutState | null>(null);

export function LayoutProvider({ namespace, storage, legacy, children }: { namespace: string; storage?: LayoutStorage | null; legacy?: LegacyKeys; children: ReactNode }) {
  const store = useMemo(() => createLayoutStore({ namespace, storage, legacy }), [namespace, storage, legacy]);
  const [navCollapsed, setNav] = useState(() => store.readNavCollapsed());
  const [dockCollapsed, setDock] = useState(() => store.readDockCollapsed());
  const [dockWidth, setWidth] = useState(() => store.readDockWidth());
  const setNavCollapsed = useCallback((v: boolean) => { setNav(v); store.writeNavCollapsed(v); }, [store]);
  const setDockCollapsed = useCallback((v: boolean) => { setDock(v); store.writeDockCollapsed(v); }, [store]);
  const toggleDock = useCallback(() => setDock((prev) => { store.writeDockCollapsed(!prev); return !prev; }), [store]);
  const setDockWidth = useCallback((px: number) => { const w = clampDockWidth(px); setWidth(w); store.writeDockWidth(w); }, [store]);
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && !e.altKey && !e.shiftKey && e.key.toLowerCase() === "j") { e.preventDefault(); toggleDock(); }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [toggleDock]);
  const value = useMemo<LayoutState>(() => ({ navCollapsed, setNavCollapsed, dockCollapsed, setDockCollapsed, toggleDock, dockWidth, setDockWidth }),
    [navCollapsed, setNavCollapsed, dockCollapsed, setDockCollapsed, toggleDock, dockWidth, setDockWidth]);
  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}
export function useLayout(): LayoutState {
  const v = useContext(Ctx);
  if (!v) throw new Error("useLayout must be used inside <LayoutProvider>");
  return v;
}
export function useDockToggle(): () => void { return useLayout().toggleDock; }
