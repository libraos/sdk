export const DOCK_MIN_WIDTH = 280;
export const DOCK_MAX_WIDTH = 520;
export const DOCK_DEFAULT_WIDTH = 360;

export function clampDockWidth(px: number): number {
  return Math.min(DOCK_MAX_WIDTH, Math.max(DOCK_MIN_WIDTH, Math.round(px)));
}

export interface LayoutStorage { getItem(key: string): string | null; setItem(key: string, value: string): void }
export interface LegacyKeys { navCollapsed?: string[]; dockCollapsed?: string[]; dockWidth?: string[] }
export interface LayoutStore {
  readNavCollapsed(): boolean; writeNavCollapsed(v: boolean): void;
  readDockCollapsed(): boolean; writeDockCollapsed(v: boolean): void;
  readDockWidth(): number; writeDockWidth(px: number): void;
}

function defaultStorage(): LayoutStorage | null {
  try { return typeof window !== "undefined" && window.localStorage ? window.localStorage : null; } catch { return null; }
}

/**
 * Persisted layout state. Every storage access is guarded: a throwing or
 * absent storage falls back to an in-memory map, so the layout always renders.
 * Legacy keys are read (never written) when the namespaced key is absent.
 */
export function createLayoutStore(opts: { namespace: string; storage?: LayoutStorage | null; legacy?: LegacyKeys }): LayoutStore {
  const storage = opts.storage === undefined ? defaultStorage() : opts.storage;
  const memory = new Map<string, string>();
  const k = (name: string) => `${opts.namespace}.${name}`;
  const get = (key: string): string | null => {
    if (memory.has(key)) return memory.get(key)!;
    try { return storage ? storage.getItem(key) : null; } catch { return null; }
  };
  const set = (key: string, value: string) => {
    memory.set(key, value);
    try { storage?.setItem(key, value); } catch { /* memory keeps it */ }
  };
  const readFirst = (key: string, legacy: string[] = []): string | null => {
    for (const candidate of [key, ...legacy]) { const v = get(candidate); if (v != null) return v; }
    return null;
  };
  return {
    readNavCollapsed: () => readFirst(k("nav.collapsed"), opts.legacy?.navCollapsed) === "1",
    writeNavCollapsed: (v) => set(k("nav.collapsed"), v ? "1" : "0"),
    readDockCollapsed: () => readFirst(k("dock.collapsed"), opts.legacy?.dockCollapsed) === "1",
    writeDockCollapsed: (v) => set(k("dock.collapsed"), v ? "1" : "0"),
    readDockWidth: () => {
      const raw = readFirst(k("dock.width"), opts.legacy?.dockWidth);
      if (raw == null) return DOCK_DEFAULT_WIDTH;
      const n = Number(raw);
      return Number.isFinite(n) ? clampDockWidth(n) : DOCK_DEFAULT_WIDTH;
    },
    writeDockWidth: (px) => set(k("dock.width"), String(clampDockWidth(px))),
  };
}
