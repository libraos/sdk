import { createContext, useCallback, useContext, useMemo, useState, type ReactNode } from "react";
export type ContextPane =
  | { kind: "canvas"; render: () => ReactNode; onClose: () => void }
  | { kind: "dock"; render: () => ReactNode }
  | { kind: "none"; reason: string };
export interface OpenCanvas { render: () => ReactNode; onClose: () => void }
export const CanvasStateContext = createContext<OpenCanvas | null>(null);

/** One right pane at a time: canvas > dock > none. */
export function resolveContextPane(surface: ContextPane, canvas: OpenCanvas | null): ContextPane {
  return canvas ? { kind: "canvas", render: canvas.render, onClose: canvas.onClose } : surface;
}
// no @types/node in this package: bundlers replace the literal expression `process.env.NODE_ENV`
// at build time, so this ambient declaration is enough to type-check it without a Node dependency.
declare const process: { env: Record<string, string | undefined> };
function isProduction(): boolean {
  // In an unreplaced browser build `process` is undefined and the reference throws —
  // that's treated as "not production" (dev-safe default) rather than crashing.
  try { return process.env.NODE_ENV === "production"; } catch { return false; }
}
/** A surface without a context pane must say why — the reviewable deviation. */
export function warnIfNoReason(pane: ContextPane): void {
  // production first, and `reason` may be missing altogether for an untyped caller: never throw here
  if (pane.kind !== "none" || isProduction()) return;
  if (typeof pane.reason !== "string" || !pane.reason.trim()) {
    console.warn("[@libraos/react-ui] WorkspaceShell: a { kind: \"none\" } context pane needs a non-empty reason.");
  }
}

export interface ContextPaneApi {
  openCanvas(render: () => ReactNode): void; closeCanvas(): void; isCanvasOpen: boolean;
  back(): void; forward(): void; canGoBack: boolean; canGoForward: boolean;
}
const ApiContext = createContext<ContextPaneApi | null>(null);

export function ContextPaneProvider({ children }: { children: ReactNode }) {
  // one state object, pure updaters (StrictMode runs updaters twice)
  const [{ history, index, open }, setState] = useState<{ history: Array<() => ReactNode>; index: number; open: boolean }>({ history: [], index: -1, open: false });
  const openCanvas = useCallback((render: () => ReactNode) => setState((s) => {
    const next = [...s.history.slice(0, s.index + 1), render];
    return { history: next, index: next.length - 1, open: true };
  }), []);
  const closeCanvas = useCallback(() => setState((s) => ({ ...s, open: false })), []);
  const back = useCallback(() => setState((s) => ({ ...s, index: Math.max(0, s.index - 1) })), []);
  const forward = useCallback(() => setState((s) => ({ ...s, index: Math.min(s.history.length - 1, s.index + 1) })), []);
  const api = useMemo<ContextPaneApi>(() => ({
    openCanvas, closeCanvas, isCanvasOpen: open, back, forward,
    canGoBack: open && index > 0, canGoForward: open && index < history.length - 1,
  }), [openCanvas, closeCanvas, open, back, forward, index, history.length]);
  const canvas: OpenCanvas | null = open && history[index] ? { render: history[index], onClose: closeCanvas } : null;
  return <ApiContext.Provider value={api}><CanvasStateContext.Provider value={canvas}>{children}</CanvasStateContext.Provider></ApiContext.Provider>;
}
export function useContextPane(): ContextPaneApi {
  const v = useContext(ApiContext);
  if (!v) throw new Error("useContextPane must be used inside <ContextPaneProvider>");
  return v;
}
