# @libraos/react-ui Workspace Layout (slice 2) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the three-pane workspace layout in `@libraos/react-ui`:
- `LayoutProvider`;
- `WorkspaceShell` and `NavRail`;
- `ContextPane` with `ContextPaneProvider`;
- `DockFrame`;
- `CanvasFrame` and the export helpers;
- the tokens and `aliases.css`;
- a demo page.

Version 0.2.0-alpha.0.

**Architecture:**
- **State:** one `LayoutProvider` owns the persisted layout state: nav collapsed, dock collapsed, dock width. The store is pluggable, and the provider also owns the global ⌘/Ctrl-J toggle.
- **Shell:** `WorkspaceShell` renders the grid (nav · work · context). It resolves the right pane from the surface's `ContextPane` plus an open canvas, with priority canvas > dock > none.
- **Frames:** `DockFrame` and `CanvasFrame` are chrome only; products pass their content as children.
- **Breakpoints:** narrow-screen behaviour (the nav drawer at ≤ 720px, the dock sheet at ≤ 1100px) comes from `useMediaQuery`.

**Tech Stack:** React 19, TypeScript 5 (strict), tsup (ESM, CJS, d.ts), Vitest 3 with jsdom, and @testing-library/react 16. Styles are plain CSS in `src/styles.css`, copied to `dist/`.

**Spec:** `docs/superpowers/specs/2026-10-05-react-ui-workspace-layout-design.md` (rollout step 1 only: the SDK slice plus the demo).

## Rulings made while planning
- **P1:** dock widths follow Desk's source (`copilot/persist.ts`): **default 360, min 280, max 520**. The spec's "312px" was the grid column, not the dock default. Cost if wrong: one constant.
- **P2:** CSS media queries can't read CSS variables, so the breakpoints are **literal `1100px` and `720px`** in CSS, plus exported JS constants `SHEET_QUERY` and `DRAWER_QUERY`. The spec's `--nv-bp-*` tokens are dropped. Cost if wrong: a product can't retune breakpoints through tokens.
- **P3:** resize uses **mouse events plus arrow keys**, not pointer events, because jsdom's PointerEvent support is partial. Cost if wrong: touch resizing isn't supported, which is acceptable at alpha.
- **P4b:** Desk has no `--danger`/`--warn` tokens; it hard-codes them. The new `--nv-*` status tokens get the kit's own values, and `aliases.css` maps only the tokens Desk actually defines.
- **P4c:** Escape ordering (spec: sheet → drawer → canvas). The sheet and drawer listen in the capture phase and call `preventDefault`. The canvas listens in the bubble phase and ignores an already-handled Escape.
- **P5:** persistence is keyed by `LayoutProvider`'s `namespace`, not by a `persistKey` on each `DockFrame` as the spec sketched. ⌘J has to reach the one dock that's showing, so there is a single dock state per app. Consumers observe toggles through `useLayout().dockCollapsed`, so there is no `onToggle` prop. Legacy Desk keys are passed as `legacy` and are read only, never written. Cost if wrong: an app wanting two independently persisted docks would need two providers.
- **P4:** the open questions are resolved with the spec's proposals:
  - no router adapter;
  - the Desk app-kit question is deferred to the Desk migration plan;
  - publishing is decided with the docs guide.

  The docs guide, the cookbook and the Desk migration are separate plans.

## Global Constraints
- **Namespaces:** classes `.nv-*`; tokens `--nv-*`. Everything renders inside a `.nv` root.
- **No LibraOS API calls,** no router dependency and no icon library. Icons are passed in as nodes.
- **Peer dependencies only:** `react ^19` and `react-dom ^19`. No new runtime dependencies.
- **Storage access is always wrapped in `try`/`catch`.** If storage is unavailable, everything renders with defaults.
- **Keys:** `<namespace>.nav.collapsed`, `<namespace>.dock.collapsed`, `<namespace>.dock.width`. Collapsed values are stored as `"1"`/`"0"`.
- **Dock first visit:** OPEN when no key, and no legacy key, exists. After that, the user's choice is kept.
- **⌘/Ctrl-J:** toggles the dock from anywhere, including inside a text field. Any other modifier combination, or a plain `j`, is ignored.
- **Pane priority:** canvas > dock > none. `{ kind: "none" }` requires a non-empty `reason`, otherwise a dev-mode `console.warn`.
- **Landmarks:** `nav` (rail), `main` (work), `aside` (context pane), each with an `aria-label`.
- **Tests run from `clients/react-ui`:** `npx vitest run <files>`, `npx tsc --noEmit`, `npm run build`. If `node_modules` is missing, `ln -sfn /mnt/data/ccao/libraos/sdk/clients/react-ui/node_modules node_modules`, and never commit it.
- **No `@types/node`** in this package: no `node:*` imports, `__dirname` or bare `process` in `src/`. Tests read CSS with Vite's `?raw` imports.
- **Commits:** no attribution lines; one commit per task.

## Review Focus
1. **Blocked storage:** storage that throws on read or write (Safari private mode, blocked cookies). The layout renders with defaults and toggles still work in memory. *Task 1.*
2. **A garbage stored width** (`"abc"`, `"99999"`, `"-5"`) gives the default width, or a clamped one. *Task 1.*
3. **⌘J while typing in a textarea** still toggles the dock and calls `preventDefault`. Plain `j` typed in the textarea does nothing. *Task 3.*
4. **Crossing a breakpoint** while the nav drawer or dock sheet is open: when the window widens past it, the drawer or sheet closes. The nav or dock returns to normal and the page doesn't stay `inert`. *Tasks 4 and 6.*
5. **A canvas opened while the dock is collapsed, then closed:** the dock comes back collapsed, not reset. *Task 5.*

---

### Task 1: Layout store

**Files:**
- Create: `clients/react-ui/src/layout/store.ts`
- Test: `clients/react-ui/src/layout/store.test.tsx`

**Interfaces:**
- Produces:
```ts
export const DOCK_MIN_WIDTH = 280;
export const DOCK_MAX_WIDTH = 520;
export const DOCK_DEFAULT_WIDTH = 360;
export function clampDockWidth(px: number): number;
export interface LayoutStorage { getItem(key: string): string | null; setItem(key: string, value: string): void }
export interface LegacyKeys { navCollapsed?: string[]; dockCollapsed?: string[]; dockWidth?: string[] }
export interface LayoutStore {
  readNavCollapsed(): boolean;   writeNavCollapsed(v: boolean): void;
  readDockCollapsed(): boolean;  writeDockCollapsed(v: boolean): void;
  readDockWidth(): number;       writeDockWidth(px: number): void;
}
export function createLayoutStore(opts: { namespace: string; storage?: LayoutStorage | null; legacy?: LegacyKeys }): LayoutStore;
```

- [ ] **Step 1: Write the failing tests** (`store.test.tsx`)
```tsx
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
    const st = mem({ "novadesk.copilot.collapsed": "1", "novadesk.copilot.width": "333" });
    const s = createLayoutStore({ namespace: "desk", storage: st, legacy: { dockCollapsed: ["novadesk.copilot.collapsed"], dockWidth: ["novadesk.copilot.width"] } });
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
```
- [ ] **Step 2: Run.** `npx vitest run src/layout/store.test.tsx`. Expected: FAIL (module not found).
- [ ] **Step 3: Implement** (`store.ts`)
```ts
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
```
- [ ] **Step 4: Run.** The same command. Expected: PASS (6 tests).
- [ ] **Step 5: Commit**
```bash
git add clients/react-ui/src/layout/store.ts clients/react-ui/src/layout/store.test.tsx
git commit -m "feat(react-ui): layout store — namespaced, first-visit-open, legacy-key migration, clamped width, never throws"
```

---

### Task 2: Tokens, layout CSS and `aliases.css`

**Files:**
- Modify: `clients/react-ui/src/styles.css` (tokens inside the `.nv` block, plus new blocks at the end)
- Create: `clients/react-ui/src/aliases.css`
- Modify: `clients/react-ui/scripts/copy-styles.mjs`, `clients/react-ui/package.json` (`exports`)
- Test: `clients/react-ui/src/styles.test.tsx`
- Create: `clients/react-ui/src/raw.d.ts` (`declare module "*.css?raw" { const s: string; export default s; }`)

**Interfaces:**
- Produces:
  - **CSS classes** used by Tasks 4–7: `nv-shell`, `nv-shell__nav`, `nv-shell__work`, `nv-shell__context`, `nv-shell__hamburger`, `nv-shell__backdrop`, `nv-shell__nav-restore`; modifiers `nv-shell--canvas`, `nv-shell--dock`, `nv-shell--none`, `is-nav-collapsed`, `is-drawer`, `is-drawer-open`, `is-dock-collapsed`.
  - **Dock and canvas classes:** `nv-dock`, `nv-dock--collapsed`, `nv-dock--chat-first`, `nv-dock--embedded`, `nv-dock__rail`, `nv-dock__rail-label`, `nv-dock__divider`, `nv-dock__header`, `nv-dock__body`, `nv-dock__launcher`, `nv-dock--sheet`, `nv-canvas`, `nv-canvas__header`, `nv-canvas__versions`, `nv-canvas__body`, `nv-navrail`, `nv-navrail__brand`, `nv-navrail__items`, `nv-navrail__recents`, `nv-navrail__footer`.
  - **Export path:** `@libraos/react-ui/aliases.css`.

- [ ] **Step 1: Write the failing test** (`styles.test.tsx`)
```tsx
import { describe, it, expect } from "vitest";
import css from "./styles.css?raw";
import aliases from "./aliases.css?raw";

describe("layout tokens and classes", () => {
  it("defines the layout and status tokens on .nv", () => {
    for (const t of ["--nv-nav-w:", "--nv-context-w:", "--nv-context-min:", "--nv-context-max:", "--nv-rail-w:", "--nv-danger:", "--nv-danger-ink:", "--nv-warn-bg:", "--nv-warn-ink:", "--nv-warn-line:"]) {
      expect(css).toContain(t);
    }
  });
  it("styles the shell, dock, canvas and nav rail and has both breakpoints", () => {
    for (const c of [".nv-shell", ".nv-shell__context", ".nv-dock__rail", ".nv-dock__divider", ".nv-canvas__body", ".nv-navrail"]) expect(css).toContain(c);
    expect(css).toContain("@media (max-width: 1100px)");
    expect(css).toContain("@media (max-width: 720px)");
    expect(css).toContain("prefers-reduced-motion");
  });
  it("aliases Desk's bare tokens onto --nv-*", () => {
    for (const t of ["--paper", "--surface", "--surface-2", "--ink", "--ink-soft", "--muted", "--line", "--line-strong", "--accent", "--accent-ink", "--accent-tint", "--sh-1", "--sh-2", "--sh-pop", "--r-sm", "--r", "--r-lg"]) {
      expect(aliases).toMatch(new RegExp(`${t}:\\s*var\\(--nv-`));
    }
  });
});
```
- [ ] **Step 2: Run.** `npx vitest run src/styles.test.tsx`. Expected: FAIL (`aliases.css` missing; tokens absent).
- [ ] **Step 3: Implement.** Create `src/raw.d.ts` as listed under Files.
  - **Tokens.** Inside the existing `.nv { … }` block, after `--nv-font-prose`, add the following. The status colours are the kit's own (ruling P4b):
```css
  --nv-nav-w: 260px;
  --nv-rail-w: 36px;
  --nv-context-w: 360px;
  --nv-context-min: 280px;
  --nv-context-max: 520px;
  --nv-danger: #a3392f;
  --nv-danger-ink: #7a2a22;
  --nv-warn-bg: #fbf1dc;
  --nv-warn-ink: #7a5212;
  --nv-warn-line: rgba(122, 82, 18, 0.25);
```
  - **Layout blocks.** Append to the end of `styles.css`:
```css
/* ── Workspace shell (slice 2) ─────────────────────────────────────────── */
.nv-shell { display: grid; grid-template-columns: var(--nv-nav-w) minmax(0, 1fr) var(--nv-context-w); height: 100vh; background: var(--nv-paper); }
.nv-shell.is-nav-collapsed { --nv-nav-w: 0px; }
.nv-shell.is-dock-collapsed { --nv-context-w: var(--nv-rail-w); }
.nv-shell--none { grid-template-columns: var(--nv-nav-w) minmax(0, 1fr); }
.nv-shell--canvas { grid-template-columns: var(--nv-nav-w) minmax(0, 1fr) minmax(380px, 0.95fr); }
.nv-shell__nav { overflow: auto; border-right: 1px solid var(--nv-line); background: var(--nv-surface); min-width: 0; }
.nv-shell.is-nav-collapsed .nv-shell__nav { visibility: hidden; }
.nv-shell__work { min-width: 0; overflow: auto; position: relative; }
.nv-shell__context { min-width: 0; overflow: hidden; border-left: 1px solid var(--nv-line); background: var(--nv-surface); }
.nv-shell__hamburger, .nv-shell__nav-restore { display: none; }
.nv-shell.is-nav-collapsed .nv-shell__nav-restore { display: inline-flex; position: absolute; top: 10px; left: 10px; z-index: 2; }
.nv-shell__backdrop { position: fixed; inset: 0; background: rgba(33, 30, 24, 0.28); z-index: 40; }
.nv-navrail { display: flex; flex-direction: column; height: 100%; padding: 14px 12px; gap: 12px; }
.nv-navrail__items { display: flex; flex-direction: column; gap: 2px; }
.nv-navrail__recents { flex: 1; overflow: auto; }
.nv-navrail__footer { margin-top: auto; }
/* Dock */
.nv-dock { position: relative; display: flex; flex-direction: column; height: 100%; min-width: 0; }
.nv-dock__divider { position: absolute; left: -3px; top: 0; bottom: 0; width: 6px; cursor: col-resize; z-index: 3; }
.nv-dock__divider:focus-visible { outline: 2px solid var(--nv-accent); }
.nv-dock__header { display: flex; align-items: center; gap: 8px; padding: 10px 12px; border-bottom: 1px solid var(--nv-line); }
.nv-dock__body { flex: 1; min-height: 0; overflow: auto; }
.nv-dock--collapsed { height: 100%; }
.nv-dock__rail { width: var(--nv-rail-w); height: 100%; border: 0; background: var(--nv-surface); cursor: pointer; color: var(--nv-muted); }
.nv-dock__rail-label { display: inline-block; writing-mode: vertical-rl; transform: rotate(180deg); font-size: 12px; letter-spacing: 0.04em; }
.nv-dock--chat-first, .nv-dock--embedded { height: 100%; }
.nv-dock__launcher { position: fixed; right: 16px; bottom: 16px; z-index: 30; }
.nv-dock--sheet { position: fixed; top: 0; right: 0; bottom: 0; width: min(92vw, var(--nv-context-w)); z-index: 50; background: var(--nv-surface); box-shadow: var(--nv-sh-pop); }
/* Canvas */
.nv-canvas { display: flex; flex-direction: column; height: 100%; min-width: 0; }
.nv-canvas__header { display: flex; align-items: center; gap: 8px; padding: 10px 14px; border-bottom: 1px solid var(--nv-line); }
.nv-canvas__versions { display: inline-flex; align-items: center; gap: 4px; color: var(--nv-muted); font-size: 12px; }
.nv-canvas__body { flex: 1; min-height: 0; overflow: auto; }

@media (max-width: 1100px) {
  .nv-shell, .nv-shell--canvas { grid-template-columns: var(--nv-nav-w) minmax(0, 1fr); }
  /* the dock's launcher and sheet are position:fixed — keep the aside rendered but out of the grid */
  .nv-shell__context { position: fixed; width: 0; height: 0; overflow: visible; border: 0; }
  .nv-shell--canvas .nv-shell__context { height: auto; overflow: hidden; position: fixed; inset: 0 0 0 auto; width: min(100vw, 720px); z-index: 45; box-shadow: var(--nv-sh-pop); }
}
@media (max-width: 720px) {
  .nv-shell, .nv-shell--canvas, .nv-shell--none { grid-template-columns: minmax(0, 1fr); }
  .nv-shell__hamburger { display: inline-flex; position: absolute; top: 10px; left: 10px; z-index: 2; }
  .nv-shell.is-drawer .nv-shell__nav { position: fixed; top: 0; bottom: 0; left: 0; width: min(86vw, 300px); z-index: 50; transform: translateX(-100%); transition: transform 0.2s var(--nv-ease); visibility: visible; }
  .nv-shell.is-drawer-open .nv-shell__nav { transform: translateX(0); }
}
@media (prefers-reduced-motion: reduce) {
  .nv-shell.is-drawer .nv-shell__nav { transition: none; }
}
```
  - **`src/aliases.css`:**
```css
/* @libraos/react-ui — aliases for apps migrating from bare tokens (e.g. Desk).
   Import AFTER styles.css. Bare names resolve to the kit's --nv-* tokens. Drop when migrated. */
.nv {
  --paper: var(--nv-paper); --surface: var(--nv-surface); --surface-2: var(--nv-surface-2);
  --ink: var(--nv-ink); --ink-soft: var(--nv-ink-soft); --muted: var(--nv-muted);
  --line: var(--nv-line); --line-strong: var(--nv-line-strong);
  --accent: var(--nv-accent); --accent-ink: var(--nv-accent-ink); --accent-tint: var(--nv-accent-tint); --accent-glow: var(--nv-accent-glow);
  --sh-1: var(--nv-sh-1); --sh-2: var(--nv-sh-2); --sh-pop: var(--nv-sh-pop);
  --r-sm: var(--nv-r-sm); --r: var(--nv-r); --r-lg: var(--nv-r-lg);
}
```
  - **`scripts/copy-styles.mjs`:**
```js
import { copyFileSync } from "node:fs";
copyFileSync("src/styles.css", "dist/styles.css");
copyFileSync("src/aliases.css", "dist/aliases.css");
```
  - **`package.json`:** add `"./aliases.css": "./dist/aliases.css"` to `exports`.
- [ ] **Step 4: Run.** `npx vitest run src/styles.test.tsx`, then `npm run build`, and check that `ls dist` shows `styles.css` and `aliases.css`. Expected: PASS.
- [ ] **Step 5: Commit**
```bash
git add clients/react-ui/src/styles.css clients/react-ui/src/aliases.css clients/react-ui/src/raw.d.ts clients/react-ui/src/styles.test.tsx clients/react-ui/scripts/copy-styles.mjs clients/react-ui/package.json
git commit -m "feat(react-ui): layout and status tokens, shell/dock/canvas/nav CSS with both breakpoints, aliases.css for bare-token apps"
```

---

### Task 3: `useMediaQuery`, `LayoutProvider` and the ⌘J toggle

**Files:**
- Create: `clients/react-ui/src/layout/useMediaQuery.ts`, `clients/react-ui/src/layout/LayoutProvider.tsx`
- Test: `clients/react-ui/src/layout/LayoutProvider.test.tsx`

**Interfaces:**
- Consumes: `createLayoutStore`, `clampDockWidth`, `LayoutStorage`, `LegacyKeys` (Task 1).
- Produces:
```ts
export const SHEET_QUERY = "(max-width: 1100px)";
export const DRAWER_QUERY = "(max-width: 720px)";
export function useMediaQuery(query: string): boolean;
export interface LayoutState {
  navCollapsed: boolean; setNavCollapsed(v: boolean): void;
  dockCollapsed: boolean; setDockCollapsed(v: boolean): void; toggleDock(): void;
  dockWidth: number; setDockWidth(px: number): void;   // clamps + persists
}
export function LayoutProvider(props: { namespace: string; storage?: LayoutStorage | null; legacy?: LegacyKeys; children: ReactNode }): JSX.Element;
export function useLayout(): LayoutState;   // throws a clear Error outside LayoutProvider
export function useDockToggle(): () => void;
```

- [ ] **Step 1: Write the failing tests**
```tsx
import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent, act } from "@testing-library/react";
import { LayoutProvider, useLayout } from "./LayoutProvider";
import type { LayoutStorage } from "./store";

function mem(init: Record<string, string> = {}): LayoutStorage & { data: Record<string, string> } {
  const data = { ...init };
  return { data, getItem: (k) => (k in data ? data[k] : null), setItem: (k, v) => { data[k] = v; } };
}
function Probe() {
  const l = useLayout();
  return (<div>
    <span data-testid="dock">{l.dockCollapsed ? "collapsed" : "open"}</span>
    <span data-testid="width">{l.dockWidth}</span>
    <button onClick={() => l.setDockWidth(9999)}>wide</button>
    <textarea aria-label="draft" />
  </div>);
}
const ui = (st = mem()) => render(<LayoutProvider namespace="t" storage={st}><Probe /></LayoutProvider>);

describe("LayoutProvider", () => {
  it("starts with the dock open on a first visit and persists a toggle", () => {
    const st = mem(); ui(st);
    expect(screen.getByTestId("dock").textContent).toBe("open");
    fireEvent.keyDown(window, { key: "j", metaKey: true });
    expect(screen.getByTestId("dock").textContent).toBe("collapsed");
    expect(st.data["t.dock.collapsed"]).toBe("1");
  });
  it("toggles with Ctrl-J both ways and ignores plain j and other modifiers", () => {
    ui();
    fireEvent.keyDown(window, { key: "j" });
    fireEvent.keyDown(window, { key: "j", metaKey: true, shiftKey: true });
    fireEvent.keyDown(window, { key: "j", ctrlKey: true, altKey: true });
    expect(screen.getByTestId("dock").textContent).toBe("open");
    fireEvent.keyDown(window, { key: "J", ctrlKey: true });
    expect(screen.getByTestId("dock").textContent).toBe("collapsed");
    fireEvent.keyDown(window, { key: "j", ctrlKey: true });
    expect(screen.getByTestId("dock").textContent).toBe("open");
  });
  it("toggles from inside a textarea and prevents the default", () => {
    ui();
    const ta = screen.getByLabelText("draft");
    const ev = new KeyboardEvent("keydown", { key: "j", metaKey: true, bubbles: true, cancelable: true });
    act(() => { ta.dispatchEvent(ev); });
    expect(ev.defaultPrevented).toBe(true);
    expect(screen.getByTestId("dock").textContent).toBe("collapsed");
    fireEvent.keyDown(ta, { key: "j" });
    expect(screen.getByTestId("dock").textContent).toBe("collapsed");
  });
  it("clamps and persists the width", () => {
    const st = mem(); ui(st);
    fireEvent.click(screen.getByText("wide"));
    expect(screen.getByTestId("width").textContent).toBe("520");
    expect(st.data["t.dock.width"]).toBe("520");
  });
  it("throws a clear error outside the provider", () => {
    const spy = vi.spyOn(console, "error").mockImplementation(() => {});
    expect(() => render(<Probe />)).toThrow(/LayoutProvider/);
    spy.mockRestore();
  });
});
```
- [ ] **Step 2: Run.** `npx vitest run src/layout/LayoutProvider.test.tsx`. Expected: FAIL.
- [ ] **Step 3: Implement**

`useMediaQuery.ts`:
```ts
import { useEffect, useState } from "react";
export const SHEET_QUERY = "(max-width: 1100px)";
export const DRAWER_QUERY = "(max-width: 720px)";
function matches(query: string): boolean {
  try { return typeof window !== "undefined" && typeof window.matchMedia === "function" ? window.matchMedia(query).matches : false; } catch { return false; }
}
export function useMediaQuery(query: string): boolean {
  const [hit, setHit] = useState(() => matches(query));
  useEffect(() => {
    if (typeof window === "undefined" || typeof window.matchMedia !== "function") return;
    const mql = window.matchMedia(query);
    const on = () => setHit(mql.matches);
    on();
    mql.addEventListener?.("change", on);
    return () => mql.removeEventListener?.("change", on);
  }, [query]);
  return hit;
}
```
`LayoutProvider.tsx`:
```tsx
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
```
- [ ] **Step 4: Run.** The same command. Expected: PASS (5 tests).
- [ ] **Step 5: Commit**
```bash
git add clients/react-ui/src/layout/useMediaQuery.ts clients/react-ui/src/layout/LayoutProvider.tsx clients/react-ui/src/layout/LayoutProvider.test.tsx
git commit -m "feat(react-ui): LayoutProvider — persisted nav/dock state, Cmd/Ctrl-J from anywhere, useMediaQuery breakpoints"
```

---

### Task 4: `ContextPane` types and resolution, `WorkspaceShell` and `NavRail`

**Files:**
- Create: `clients/react-ui/src/layout/contextPane.tsx`, `clients/react-ui/src/layout/WorkspaceShell.tsx`, `clients/react-ui/src/layout/NavRail.tsx`
- Test: `clients/react-ui/src/layout/WorkspaceShell.test.tsx`

**Interfaces:**
- Consumes: `useLayout`, `useMediaQuery`, `DRAWER_QUERY`, `SHEET_QUERY` (Task 3); the CSS classes (Task 2).
- Produces:
```ts
export type ContextPane =
  | { kind: "canvas"; render: () => ReactNode; onClose: () => void }
  | { kind: "dock"; render: () => ReactNode }
  | { kind: "none"; reason: string };
export interface OpenCanvas { render: () => ReactNode; onClose: () => void }
export function resolveContextPane(surface: ContextPane, canvas: OpenCanvas | null): ContextPane;
export function warnIfNoReason(pane: ContextPane): void;          // dev-only console.warn
export const CanvasStateContext: React.Context<OpenCanvas | null>; // provided by Task 5's ContextPaneProvider
export interface ShellLabels { nav?: string; work?: string; context?: string; openNav?: string; closeNav?: string; restoreNav?: string }
export function WorkspaceShell(props: { nav: ReactNode; context: ContextPane; topbar?: ReactNode; labels?: ShellLabels; children: ReactNode }): JSX.Element;
export function NavRail(props: { brand?: ReactNode; recents?: ReactNode; footer?: ReactNode; collapseLabel?: string; children: ReactNode }): JSX.Element;
```

- [ ] **Step 1: Write the failing tests**
```tsx
import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, act } from "@testing-library/react";
import { LayoutProvider } from "./LayoutProvider";
import { WorkspaceShell } from "./WorkspaceShell";
import { NavRail } from "./NavRail";
import { resolveContextPane, type ContextPane } from "./contextPane";

type Listener = () => void;
let narrow = { drawer: false, sheet: false };
const listeners = new Set<Listener>();
beforeEach(() => {
  narrow = { drawer: false, sheet: false }; listeners.clear();
  window.matchMedia = ((q: string) => ({
    get matches() { return q.includes("720") ? narrow.drawer : q.includes("1100") ? narrow.sheet : false; },
    media: q, addEventListener: (_: string, l: Listener) => listeners.add(l), removeEventListener: (_: string, l: Listener) => listeners.delete(l),
  })) as unknown as typeof window.matchMedia;
});
const setNarrow = (n: typeof narrow) => act(() => { narrow = n; listeners.forEach((l) => l()); });
const mem = () => { const d: Record<string, string> = {}; return { getItem: (k: string) => d[k] ?? null, setItem: (k: string, v: string) => { d[k] = v; } }; };
const dock: ContextPane = { kind: "dock", render: () => <div>DOCK</div> };
const shell = (context: ContextPane = dock) => render(
  <LayoutProvider namespace="t" storage={mem()}>
    <WorkspaceShell nav={<NavRail brand="B"><a href="#a">Inbox</a></NavRail>} context={context}><p>WORK</p></WorkspaceShell>
  </LayoutProvider>);

describe("resolveContextPane", () => {
  it("canvas beats dock beats none", () => {
    const canvas = { render: () => "C", onClose: () => {} };
    expect(resolveContextPane(dock, canvas).kind).toBe("canvas");
    expect(resolveContextPane(dock, null).kind).toBe("dock");
    expect(resolveContextPane({ kind: "none", reason: "admin" }, canvas).kind).toBe("canvas");
  });
});

describe("WorkspaceShell", () => {
  it("renders the three landmarks with the dock pane", () => {
    shell();
    expect(screen.getByRole("navigation")).toBeTruthy();
    expect(screen.getByRole("main").textContent).toContain("WORK");
    expect(screen.getByRole("complementary").textContent).toBe("DOCK");
    expect(document.querySelector(".nv-shell--dock")).toBeTruthy();
  });
  it("has no aside for a declared none, and warns in dev when the reason is empty", () => {
    const warn = vi.spyOn(console, "warn").mockImplementation(() => {});
    shell({ kind: "none", reason: "admin console" });
    expect(screen.queryByRole("complementary")).toBeNull();
    expect(warn).not.toHaveBeenCalled();
    shell({ kind: "none", reason: " " });
    expect(warn).toHaveBeenCalledWith(expect.stringMatching(/reason/));
    warn.mockRestore();
  });
  it("collapses the nav from the rail and restores it from the work area", () => {
    shell();
    fireEvent.click(screen.getByRole("button", { name: "Collapse navigation" }));
    expect(document.querySelector(".nv-shell.is-nav-collapsed")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "Show navigation" }));
    expect(document.querySelector(".nv-shell.is-nav-collapsed")).toBeNull();
  });
  it("turns the nav into a drawer at ≤720px: inert when closed, Escape and backdrop close, focus returns", () => {
    narrow = { drawer: true, sheet: true };
    shell();
    const nav = screen.getByRole("navigation", { hidden: true });
    expect(nav.getAttribute("aria-hidden")).toBe("true");
    expect(nav.hasAttribute("inert")).toBe(true);
    const burger = screen.getByRole("button", { name: "Open navigation" });
    fireEvent.click(burger);
    expect(nav.getAttribute("aria-hidden")).toBeNull();
    fireEvent.keyDown(window, { key: "Escape" });
    expect(nav.getAttribute("aria-hidden")).toBe("true");
    expect(document.activeElement).toBe(burger);
    fireEvent.click(burger);
    fireEvent.click(document.querySelector(".nv-shell__backdrop")!);
    expect(nav.getAttribute("aria-hidden")).toBe("true");
  });
  it("leaving the narrow breakpoint closes the drawer and un-inerts the nav", () => {
    narrow = { drawer: true, sheet: true };
    shell();
    fireEvent.click(screen.getByRole("button", { name: "Open navigation" }));
    setNarrow({ drawer: false, sheet: false });
    const nav = screen.getByRole("navigation");
    expect(nav.hasAttribute("inert")).toBe(false);
    expect(document.querySelector(".nv-shell.is-drawer-open")).toBeNull();
  });
});
```
- [ ] **Step 2: Run.** `npx vitest run src/layout/WorkspaceShell.test.tsx`. Expected: FAIL.
- [ ] **Step 3: Implement**

`contextPane.tsx`:
```tsx
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
```
`NavRail.tsx`:
```tsx
import type { ReactNode } from "react";
import { useLayout } from "./LayoutProvider";
import { IconButton } from "../components/IconButton";
export function NavRail({ brand, recents, footer, collapseLabel = "Collapse navigation", children }: { brand?: ReactNode; recents?: ReactNode; footer?: ReactNode; collapseLabel?: string; children: ReactNode }) {
  const { setNavCollapsed } = useLayout();
  return (
    <div className="nv-navrail">
      <div className="nv-navrail__brand">{brand}<IconButton aria-label={collapseLabel} size="sm" onClick={() => setNavCollapsed(true)}>‹</IconButton></div>
      <div className="nv-navrail__items">{children}</div>
      {recents && <div className="nv-navrail__recents">{recents}</div>}
      {footer && <div className="nv-navrail__footer">{footer}</div>}
    </div>
  );
}
```
`WorkspaceShell.tsx`:
```tsx
import { useContext, useEffect, useRef, useState, type CSSProperties, type ReactNode } from "react";
import { useLayout } from "./LayoutProvider";
import { DRAWER_QUERY, useMediaQuery } from "./useMediaQuery";
import { CanvasStateContext, resolveContextPane, warnIfNoReason, type ContextPane } from "./contextPane";
import { IconButton } from "../components/IconButton";

export interface ShellLabels { nav?: string; work?: string; context?: string; openNav?: string; closeNav?: string; restoreNav?: string }

export function WorkspaceShell({ nav, context, topbar, labels = {}, children }: { nav: ReactNode; context: ContextPane; topbar?: ReactNode; labels?: ShellLabels; children: ReactNode }) {
  const layout = useLayout();
  const canvas = useContext(CanvasStateContext);
  const pane = resolveContextPane(context, canvas);
  const drawer = useMediaQuery(DRAWER_QUERY);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const burgerRef = useRef<HTMLButtonElement>(null);
  const navRef = useRef<HTMLElement>(null);

  const noneReason = context.kind === "none" ? context.reason : null;
  useEffect(() => { warnIfNoReason(context); }, [context.kind, noneReason]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => { if (!drawer) setDrawerOpen(false); }, [drawer]);
  useEffect(() => {
    if (!drawerOpen) return;
    navRef.current?.querySelector<HTMLElement>("a,button,[tabindex]")?.focus();
    // capture phase + preventDefault: the drawer closes before (and instead of) an open canvas (ruling P4c)
    const onKey = (e: KeyboardEvent) => { if (e.key === "Escape") { e.preventDefault(); closeDrawer(); } };
    window.addEventListener("keydown", onKey, true);
    return () => window.removeEventListener("keydown", onKey, true);
  }, [drawerOpen]);
  function closeDrawer() { setDrawerOpen(false); burgerRef.current?.focus(); }

  const navHidden = drawer && !drawerOpen;
  const cls = ["nv", "nv-shell", `nv-shell--${pane.kind}`,
    layout.navCollapsed && !drawer ? "is-nav-collapsed" : "",
    pane.kind === "dock" && layout.dockCollapsed ? "is-dock-collapsed" : "",
    drawer ? "is-drawer" : "", drawerOpen ? "is-drawer-open" : ""].filter(Boolean).join(" ");
  const style = { "--nv-context-w": `${layout.dockWidth}px` } as CSSProperties;
  return (
    <div className={cls} style={style}>
      <nav ref={navRef} className="nv-shell__nav" aria-label={labels.nav ?? "Navigation"}
        aria-hidden={navHidden ? "true" : undefined} inert={navHidden || undefined}
        onClick={(e) => { if (drawerOpen && (e.target as HTMLElement).closest("a")) closeDrawer(); }}>
        {nav}
      </nav>
      {drawerOpen && <div className="nv-shell__backdrop" onClick={closeDrawer} />}
      <main className="nv-shell__work" aria-label={labels.work ?? "Work"}>
        {drawer && <IconButton ref={burgerRef} className="nv-shell__hamburger" aria-label={labels.openNav ?? "Open navigation"} aria-expanded={drawerOpen} onClick={() => setDrawerOpen(true)}>☰</IconButton>}
        {!drawer && layout.navCollapsed && <IconButton className="nv-shell__nav-restore" aria-label={labels.restoreNav ?? "Show navigation"} onClick={() => layout.setNavCollapsed(false)}>›</IconButton>}
        {topbar}
        {children}
      </main>
      {pane.kind !== "none" && <aside className="nv-shell__context" aria-label={labels.context ?? (pane.kind === "canvas" ? "Canvas" : "Copilot")}>{pane.render()}</aside>}
    </div>
  );
}
```
  **`IconButton` needs a `ref` type.** It already merges `className`, but its props extend `ButtonHTMLAttributes`, which has no `ref`, so `ref={burgerRef}` fails `tsc`. In `src/components/IconButton.tsx`, change the import to `import type { ComponentPropsWithRef } from "react";` and the interface to `export interface IconButtonProps extends ComponentPropsWithRef<"button"> {`. In React 19, `ref` is a plain prop, and `...rest` already passes it to the `<button>`. Existing IconButton tests must stay green.
- [ ] **Step 4: Run.** `npx vitest run src/layout src/components` and `npx tsc --noEmit`. Expected: PASS.
- [ ] **Step 5: Commit**
```bash
git add clients/react-ui/src
git commit -m "feat(react-ui): WorkspaceShell + NavRail — three landmarks, canvas > dock > none, declared none with a reason, collapsible nav, drawer at 720px"
```

---

### Task 5: `ContextPaneProvider` (canvas open, close and history)

**Files:**
- Modify: `clients/react-ui/src/layout/contextPane.tsx`
- Test: `clients/react-ui/src/layout/contextPane.test.tsx`

**Interfaces:**
- Consumes: `CanvasStateContext`, `OpenCanvas` (Task 4); `LayoutProvider` (Task 3).
- Produces:
```ts
export interface ContextPaneApi {
  openCanvas(render: () => ReactNode): void;   // pushes onto history, opens
  closeCanvas(): void;                          // closes; history kept
  isCanvasOpen: boolean;
  back(): void; forward(): void; canGoBack: boolean; canGoForward: boolean;
}
export function ContextPaneProvider(props: { children: ReactNode }): JSX.Element;
export function useContextPane(): ContextPaneApi;   // throws outside the provider
```

- [ ] **Step 1: Write the failing tests**
```tsx
import { describe, it, expect } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
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
});
```
- [ ] **Step 2: Run.** `npx vitest run src/layout/contextPane.test.tsx`. Expected: FAIL.
- [ ] **Step 3: Implement.** Append to `contextPane.tsx`:
```tsx
import { useCallback, useContext, useMemo, useState } from "react";
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
```
  Merge these imports into the file's existing `import` line from `react`, without duplicating it.
- [ ] **Step 4: Run.** `npx vitest run src/layout` and `npx tsc --noEmit`. Expected: PASS.
- [ ] **Step 5: Commit**
```bash
git add clients/react-ui/src/layout/contextPane.tsx clients/react-ui/src/layout/contextPane.test.tsx
git commit -m "feat(react-ui): ContextPaneProvider — openCanvas/closeCanvas with back/forward history; the dock returns as the user left it"
```

---

### Task 6: `DockFrame`

**Files:**
- Create: `clients/react-ui/src/layout/DockFrame.tsx`
- Test: `clients/react-ui/src/layout/DockFrame.test.tsx`

**Interfaces:**
- Consumes: `useLayout`, `useMediaQuery`, `SHEET_QUERY` (Task 3).
- Produces:
```ts
export interface DockLabels { name?: string; collapse?: string; expand?: string; open?: string; close?: string; resize?: string }
export function DockFrame(props: {
  title?: ReactNode; actions?: ReactNode;
  variant?: "docked" | "chat-first" | "embedded";
  labels?: DockLabels; children: ReactNode;
}): JSX.Element;
export const DOCK_KEY_STEP = 16; // px per ArrowLeft/ArrowRight on the divider
```

- [ ] **Step 1: Write the failing tests.** Reuse the `matchMedia` mock from Task 4's test, copied in full into this file.
```tsx
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
    expect(document.activeElement).toBe(launcher);
  });
  it("leaving the sheet breakpoint while the sheet is open returns to the docked frame", () => {
    sheet = true; dock();
    fireEvent.click(screen.getByRole("button", { name: "Open Copilot" }));
    setSheet(false);
    expect(screen.queryByRole("dialog")).toBeNull();
    expect(screen.getByLabelText("ask")).toBeTruthy();
  });
});
```
- [ ] **Step 2: Run.** `npx vitest run src/layout/DockFrame.test.tsx`. Expected: FAIL.
- [ ] **Step 3: Implement** (`DockFrame.tsx`)
```tsx
import { useEffect, useRef, useState, type ReactNode } from "react";
import { useLayout } from "./LayoutProvider";
import { SHEET_QUERY, useMediaQuery } from "./useMediaQuery";
import { DOCK_MAX_WIDTH, DOCK_MIN_WIDTH } from "./store";
import { IconButton } from "../components/IconButton";

export const DOCK_KEY_STEP = 16;
export interface DockLabels { name?: string; collapse?: string; expand?: string; open?: string; close?: string; resize?: string }

export function DockFrame({ title, actions, variant = "docked", labels = {}, children }: {
  title?: ReactNode; actions?: ReactNode; variant?: "docked" | "chat-first" | "embedded"; labels?: DockLabels; children: ReactNode;
}) {
  const l = useLayout();
  const name = labels.name ?? "Copilot";
  const sheetMode = useMediaQuery(SHEET_QUERY) && variant === "docked";
  const [sheetOpen, setSheetOpen] = useState(false);
  const launcherRef = useRef<HTMLButtonElement>(null);
  const sheetRef = useRef<HTMLElement>(null);
  // the launcher is unmounted while the sheet is open, so focus returns after it re-mounts
  const restoreFocus = useRef(false);
  const closeSheet = () => { restoreFocus.current = true; setSheetOpen(false); };

  useEffect(() => { if (!sheetMode) setSheetOpen(false); }, [sheetMode]);
  useEffect(() => {
    if (!sheetOpen && restoreFocus.current) { restoreFocus.current = false; launcherRef.current?.focus(); }
  }, [sheetOpen]);
  useEffect(() => {
    if (!sheetOpen) return;
    const el = sheetRef.current;
    el?.querySelector<HTMLElement>("textarea,input,button,a,[tabindex]")?.focus();
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") { e.preventDefault(); closeSheet(); return; }
      if (e.key !== "Tab" || !el) return;
      const f = Array.from(el.querySelectorAll<HTMLElement>("textarea,input,button,a,[tabindex]:not([tabindex='-1'])"));
      if (!f.length) return;
      const first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    };
    window.addEventListener("keydown", onKey, true); // capture: sheet beats canvas (ruling P4c)
    return () => window.removeEventListener("keydown", onKey, true);
  }, [sheetOpen]);

  const startDrag = (e: React.MouseEvent) => {
    const startX = e.clientX, startW = l.dockWidth;
    const move = (ev: MouseEvent) => l.setDockWidth(startW + (startX - ev.clientX));
    const up = () => { document.removeEventListener("mousemove", move); document.removeEventListener("mouseup", up); };
    document.addEventListener("mousemove", move); document.addEventListener("mouseup", up);
  };
  const header = variant === "embedded" ? null : (
    <div className="nv-dock__header">
      <div style={{ flex: 1, minWidth: 0 }}>{title}</div>
      {actions}
      {variant === "docked" && !sheetMode && <IconButton size="sm" aria-label={labels.collapse ?? `Collapse ${name}`} onClick={() => l.setDockCollapsed(true)}>›</IconButton>}
      {sheetMode && <IconButton size="sm" aria-label={labels.close ?? `Close ${name}`} onClick={closeSheet}>×</IconButton>}
    </div>
  );

  if (sheetMode) {
    return sheetOpen ? (
      <section ref={sheetRef} className="nv-dock nv-dock--sheet" role="dialog" aria-modal="true" aria-label={name}>
        {header}<div className="nv-dock__body">{children}</div>
      </section>
    ) : (
      <IconButton ref={launcherRef} className="nv-dock__launcher" aria-label={labels.open ?? `Open ${name}`} onClick={() => setSheetOpen(true)}>✦</IconButton>
    );
  }
  if (variant === "docked" && l.dockCollapsed) {
    return (
      <div className="nv-dock nv-dock--collapsed">
        <button type="button" className="nv-dock__rail" aria-label={labels.expand ?? `Expand ${name}`} onClick={() => l.setDockCollapsed(false)}>
          <span className="nv-dock__rail-label">{name}</span>
        </button>
      </div>
    );
  }
  return (
    <section className={`nv-dock nv-dock--${variant}`} aria-label={name}>
      {variant === "docked" && (
        <div className="nv-dock__divider" role="separator" aria-orientation="vertical" tabIndex={0}
          aria-label={labels.resize ?? `Resize ${name}`} aria-valuemin={DOCK_MIN_WIDTH} aria-valuemax={DOCK_MAX_WIDTH} aria-valuenow={l.dockWidth}
          onMouseDown={startDrag}
          onKeyDown={(e) => {
            if (e.key === "ArrowLeft") { e.preventDefault(); l.setDockWidth(l.dockWidth + DOCK_KEY_STEP); }
            if (e.key === "ArrowRight") { e.preventDefault(); l.setDockWidth(l.dockWidth - DOCK_KEY_STEP); }
          }} />
      )}
      {header}
      <div className="nv-dock__body">{children}</div>
    </section>
  );
}
```
  The rail's visible label is real text inside the button. Rotation is CSS only, so screen readers read it.
- [ ] **Step 4: Run.** `npx vitest run src/layout` and `npx tsc --noEmit`. Expected: PASS.
- [ ] **Step 5: Commit**
```bash
git add clients/react-ui/src/layout/DockFrame.tsx clients/react-ui/src/layout/DockFrame.test.tsx
git commit -m "feat(react-ui): DockFrame — first-visit-open, collapse to a labelled rail, mouse and keyboard resize (clamped, persisted), chat-first/embedded variants, sheet with focus trap at 1100px"
```

---

### Task 7: `CanvasFrame`, export helpers, barrel, version, demo

**Files:**
- Create: `clients/react-ui/src/layout/CanvasFrame.tsx`, `clients/react-ui/src/layout/artifacts.ts`
- Test: `clients/react-ui/src/layout/CanvasFrame.test.tsx`, `clients/react-ui/src/layout/artifacts.test.tsx`
- Modify: `clients/react-ui/src/index.ts`, `clients/react-ui/package.json` (version), `clients/react-ui/README.md` (create if absent), `examples/react-ui-demo/src/main.tsx`

**Interfaces:**
- Produces:
```ts
// artifacts.ts
export interface ArtifactKindDescriptor { id: string; body: "markdown" | "custom"; title(content: string): string }
export function registerArtifactKind(d: ArtifactKindDescriptor): void;
export function describeArtifactKind(id: string): ArtifactKindDescriptor;   // unknown → markdown
export function exportFilename(markdown: string, fallback: string): string;   // Desk's filenameFromMarkdown
export function exportStem(kind: string, content: string, fallback: string): string;
// CanvasFrame.tsx
export interface CanvasLabels { close?: string; previous?: string; next?: string; version?(i: number, n: number): string }
export function CanvasFrame(props: { title: ReactNode; onClose(): void; versionIndex?: number; versionCount?: number;
  onPrevVersion?(): void; onNextVersion?(): void; actions?: ReactNode; labels?: CanvasLabels; children: ReactNode }): JSX.Element;
```

- [ ] **Step 1: Write the failing tests**

`artifacts.test.tsx`. These are Desk's filename cases, kept identical so Desk can swap later:
```tsx
import { describe, it, expect } from "vitest";
import { exportFilename, exportStem, registerArtifactKind, describeArtifactKind } from "./artifacts";
describe("export helpers", () => {
  it("names a markdown export after its first H1, else its first line, else the fallback", () => {
    expect(exportFilename("# Q3 Launch Plan\n\nbody", "draft")).toBe("q3-launch-plan");
    expect(exportFilename("Intro line\nmore", "draft")).toBe("intro-line");
    expect(exportFilename("\n\n", "draft")).toBe("draft");
    expect(exportFilename("# **Bold** `code` > quote", "x")).toBe("bold-code-quote");
    expect(exportFilename("# " + "a".repeat(80), "x")).toHaveLength(60);
  });
  it("uses a custom kind's own title for its stem", () => {
    registerArtifactKind({ id: "sheet", body: "custom", title: (c) => c.split("\n")[1] ?? "" });
    expect(describeArtifactKind("sheet").body).toBe("custom");
    expect(exportStem("sheet", "```sheet\nPipeline Q4\n", "fallback")).toBe("pipeline-q4");
    expect(exportStem("unknown-kind", "# Memo", "fallback")).toBe("memo");
    expect(describeArtifactKind("unknown-kind").body).toBe("markdown");
  });
});
```
`CanvasFrame.test.tsx`:
```tsx
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
});
```
- [ ] **Step 2: Run.** `npx vitest run src/layout/artifacts.test.tsx src/layout/CanvasFrame.test.tsx`. Expected: FAIL.
- [ ] **Step 3: Implement**

`artifacts.ts`:
```ts
export interface ArtifactKindDescriptor { id: string; body: "markdown" | "custom"; title(content: string): string }
const registry = new Map<string, ArtifactKindDescriptor>();
const MARKDOWN: ArtifactKindDescriptor = { id: "markdown", body: "markdown", title: () => "" };
export function registerArtifactKind(d: ArtifactKindDescriptor): void { registry.set(d.id, d); }
export function describeArtifactKind(id: string): ArtifactKindDescriptor { return registry.get(id) ?? MARKDOWN; }
function slugify(raw: string): string {
  return raw.trim().toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 60);
}
/** Name an export after its content: the first H1, else the first non-empty line, else `fallback`. */
export function exportFilename(markdown: string, fallback: string): string {
  const md = markdown ?? "";
  const h1 = md.match(/^#\s+(.+)$/m);
  const line = md.split("\n").find((l) => l.trim());
  return slugify((h1 ? h1[1] : line ?? "").replace(/[#*`>_]/g, "")) || fallback;
}
/** A custom-body kind names its export from its own title; markdown keeps the H1 rule. */
export function exportStem(kind: string, content: string, fallback: string): string {
  const d = describeArtifactKind(kind);
  if (d.body === "custom") return slugify(d.title(content)) || fallback;
  return exportFilename(content, fallback);
}
```
`CanvasFrame.tsx`:
```tsx
import { useEffect, type ReactNode } from "react";
import { IconButton } from "../components/IconButton";
export interface CanvasLabels { close?: string; previous?: string; next?: string; version?(i: number, n: number): string }
export function CanvasFrame({ title, onClose, versionIndex = 0, versionCount = 1, onPrevVersion, onNextVersion, actions, labels = {}, children }: {
  title: ReactNode; onClose(): void; versionIndex?: number; versionCount?: number; onPrevVersion?(): void; onNextVersion?(): void;
  actions?: ReactNode; labels?: CanvasLabels; children: ReactNode;
}) {
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => { if (e.key === "Escape" && !e.defaultPrevented) onClose(); };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose]);
  return (
    <section className="nv-canvas" aria-label={typeof title === "string" ? title : "Canvas"}>
      <div className="nv-canvas__header">
        <div style={{ flex: 1, minWidth: 0, fontWeight: 600 }}>{title}</div>
        {versionCount > 1 && (
          <span className="nv-canvas__versions">
            <IconButton size="sm" aria-label={labels.previous ?? "Previous version"} disabled={versionIndex <= 0} onClick={onPrevVersion}>‹</IconButton>
            <span>{labels.version ? labels.version(versionIndex, versionCount) : `Version ${versionIndex + 1} of ${versionCount}`}</span>
            <IconButton size="sm" aria-label={labels.next ?? "Next version"} disabled={versionIndex >= versionCount - 1} onClick={onNextVersion}>›</IconButton>
          </span>
        )}
        {actions}
        <IconButton size="sm" aria-label={labels.close ?? "Close canvas"} onClick={onClose}>×</IconButton>
      </div>
      <div className="nv-canvas__body">{children}</div>
    </section>
  );
}
```
**Barrel (`src/index.ts`).** Append:
```ts
export { createLayoutStore, clampDockWidth, DOCK_MIN_WIDTH, DOCK_MAX_WIDTH, DOCK_DEFAULT_WIDTH } from "./layout/store";
export type { LayoutStore, LayoutStorage, LegacyKeys } from "./layout/store";
export { LayoutProvider, useLayout, useDockToggle } from "./layout/LayoutProvider";
export type { LayoutState } from "./layout/LayoutProvider";
export { useMediaQuery, SHEET_QUERY, DRAWER_QUERY } from "./layout/useMediaQuery";
export { WorkspaceShell } from "./layout/WorkspaceShell";
export type { ShellLabels } from "./layout/WorkspaceShell";
export { NavRail } from "./layout/NavRail";
export { ContextPaneProvider, useContextPane, resolveContextPane } from "./layout/contextPane";
export type { ContextPane, ContextPaneApi, OpenCanvas } from "./layout/contextPane";
export { DockFrame, DOCK_KEY_STEP } from "./layout/DockFrame";
export type { DockLabels } from "./layout/DockFrame";
export { CanvasFrame } from "./layout/CanvasFrame";
export type { CanvasLabels } from "./layout/CanvasFrame";
export { registerArtifactKind, describeArtifactKind, exportFilename, exportStem } from "./layout/artifacts";
export type { ArtifactKindDescriptor } from "./layout/artifacts";
export type SurfaceContext<Scope extends string = string> = { scope: Scope; identity: string; key?: string; label?: string };
```
**Version.** In `package.json`, set `"version": "0.2.0-alpha.0"`.

**README (`clients/react-ui/README.md`).** Add a "Workspace layout" section with a 25-line example: `LayoutProvider`, then `ContextPaneProvider`, then `WorkspaceShell` with a `NavRail`, a dock pane rendering `DockFrame`, and a button calling `openCanvas`. Also document the `{ kind: "none", reason }` rule and the `SurfaceContext` identity/key semantics, as spec §6 states them.

**Demo (`examples/react-ui-demo/src/main.tsx`).** Add a "Workspace" view behind a top-level `Toggle` (Primitives / Workspace). The Workspace view:
- wraps `LayoutProvider namespace="demo"` and `ContextPaneProvider` around a `WorkspaceShell`;
- has a `NavRail` with three links;
- has a work pane with a list of 5 fake deals, each with an "Open memo" button that calls `openCanvas(() => <CanvasFrame title="Deal memo" onClose={closeCanvas}>…</CanvasFrame>)`;
- has a context pane `{ kind: "dock", render: () => <DockFrame title="Copilot">…a fake thread + Composer…</DockFrame> }`.
- [ ] **Step 4: Run.**
  - `npx vitest run` (the whole kit), `npx tsc --noEmit` and `npm run build`. Expected: all PASS, and `dist/` has `index.js`, `index.cjs`, `index.d.ts`, `styles.css` and `aliases.css`.
  - Then `cd ../../examples/react-ui-demo && npm install --no-audit --no-fund && npm run build`. Expected: the build succeeds. If the network is unavailable, report it and skip this step.
- [ ] **Step 5: Commit**
```bash
git add clients/react-ui examples/react-ui-demo/src/main.tsx
git commit -m "feat(react-ui): CanvasFrame + export helpers (Desk's filename rules), barrel exports, 0.2.0-alpha.0, README section and a three-pane demo"
```
