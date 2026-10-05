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
function isProduction(): boolean {
  // no @types/node in this package: read NODE_ENV through globalThis (bundlers replace it at build time anyway)
  const env = (globalThis as { process?: { env?: Record<string, string | undefined> } }).process?.env;
  return env?.NODE_ENV === "production";
}
/** A surface without a context pane must say why — the reviewable deviation. */
export function warnIfNoReason(pane: ContextPane): void {
  if (pane.kind === "none" && !pane.reason.trim() && !isProduction()) {
    console.warn("[@libraos/react-ui] WorkspaceShell: a { kind: \"none\" } context pane needs a non-empty reason.");
  }
}
