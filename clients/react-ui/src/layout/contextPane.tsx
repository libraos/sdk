import { createContext, type ReactNode } from "react";
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
  if (pane.kind === "none" && !pane.reason.trim() && !isProduction()) {
    console.warn("[@libraos/react-ui] WorkspaceShell: a { kind: \"none\" } context pane needs a non-empty reason.");
  }
}
