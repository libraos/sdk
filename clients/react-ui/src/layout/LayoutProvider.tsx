import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState, type ReactNode } from "react";
import { clampDockWidth, createLayoutStore, type LayoutStorage, type LegacyKeys } from "./store";

export interface LayoutState {
  navCollapsed: boolean; setNavCollapsed(v: boolean): void;
  dockCollapsed: boolean; setDockCollapsed(v: boolean): void; toggleDock(): void;
  dockWidth: number; setDockWidth(px: number): void;
}
const Ctx = createContext<LayoutState | null>(null);

/**
 * ⌘/Ctrl-J acts on the dock that is actually showing. A mounted, docked DockFrame registers a
 * handler (collapse/expand, or open/close in sheet mode); chat-first and embedded frames register
 * none. A handler returns false to decline (its frame sits inside an inert subtree, e.g. behind the
 * nav drawer). Internal: not exported from the package barrel.
 */
export type DockToggleHandler = () => boolean;
export const DockToggleRegistry = createContext<((handler: DockToggleHandler) => () => void) | null>(null);

export function LayoutProvider({ namespace, storage, legacy, children }: { namespace: string; storage?: LayoutStorage | null; legacy?: LegacyKeys; children: ReactNode }) {
  const store = useMemo(() => createLayoutStore({ namespace, storage, legacy }), [namespace, storage, legacy]);
  const [navCollapsed, setNav] = useState(() => store.readNavCollapsed());
  const [dockCollapsed, setDock] = useState(() => store.readDockCollapsed());
  const [dockWidth, setWidth] = useState(() => store.readDockWidth());
  const setNavCollapsed = useCallback((v: boolean) => { setNav(v); store.writeNavCollapsed(v); }, [store]);
  const setDockCollapsed = useCallback((v: boolean) => { setDock(v); store.writeDockCollapsed(v); }, [store]);
  const toggleDock = useCallback(() => setDock((prev) => { store.writeDockCollapsed(!prev); return !prev; }), [store]);
  const setDockWidth = useCallback((px: number) => { const w = clampDockWidth(px); setWidth(w); store.writeDockWidth(w); }, [store]);
  // most recent last; ⌘J goes to the newest registration only
  const handlers = useRef<DockToggleHandler[]>([]);
  const register = useCallback((handler: DockToggleHandler) => {
    handlers.current.push(handler);
    return () => { handlers.current = handlers.current.filter((h) => h !== handler); };
  }, []);
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (!(e.metaKey || e.ctrlKey) || e.altKey || e.shiftKey || e.key.toLowerCase() !== "j") return;
      // No dock showing (a "none" surface, a canvas in its place, chat-first/embedded, or a dock
      // behind the nav drawer): leave hidden persisted state and the browser's shortcut alone.
      const handler = handlers.current[handlers.current.length - 1];
      if (handler && handler()) e.preventDefault();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);
  const value = useMemo<LayoutState>(() => ({ navCollapsed, setNavCollapsed, dockCollapsed, setDockCollapsed, toggleDock, dockWidth, setDockWidth }),
    [navCollapsed, setNavCollapsed, dockCollapsed, setDockCollapsed, toggleDock, dockWidth, setDockWidth]);
  return <Ctx.Provider value={value}><DockToggleRegistry.Provider value={register}>{children}</DockToggleRegistry.Provider></Ctx.Provider>;
}
export function useLayout(): LayoutState {
  const v = useContext(Ctx);
  if (!v) throw new Error("useLayout must be used inside <LayoutProvider>");
  return v;
}
/** Toggles the persisted dock state — for a command palette or any programmatic caller. */
export function useDockToggle(): () => void { return useLayout().toggleDock; }
