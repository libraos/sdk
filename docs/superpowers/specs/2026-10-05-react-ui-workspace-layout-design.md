# @libraos/react-ui — Workspace layout (slice 2): nav · work · context pane

**Date:** 2026-10-05 · **Status:** Design, awaiting review · **Repo:** `libraos-sdk`
**Builds on:** `2026-06-19-react-ui-kit-foundation-design.md` (slice 1: tokens + primitives).
**Source of the pattern:** Desk's employee UI (`libraos/desk`, `services/employee-ui`), where it is a
convention in `CLAUDE.md` ("Copilot-Everywhere") and an implementation in `App.tsx`,
`copilot/CopilotDock.tsx` and `canvas/CanvasPanel.tsx`. The inventory of that code is in §11.

## 1. Goal

Make the three-pane layout **the** way a LibraOS application is built, not a Desk-only habit:

```
┌──────────┬──────────────────────────────┬────────────────┐
│ Nav      │ Work                         │ Context pane   │
│ (rail)   │ list · board · record detail │ copilot dock   │
│          │ · editor                     │   — or —       │
│          │                              │ canvas         │
└──────────┴──────────────────────────────┴────────────────┘
```

A product installs `@libraos/react-ui` and gets the layout shell, the dock's frame and the canvas's
frame, with the behaviour Desk has already tested:
- first-visit-open;
- collapse to a rail;
- resize;
- ⌘/Ctrl-J;
- a narrow-screen sheet;
- "canvas takes the context pane".

Each product keeps its own domain: what the work pane shows, which agent the dock talks to, how it
is grounded, and what governance UI it shows.

**What this slice is NOT:**
- **No chat transport or thread rendering.** That is the planned chat/AG-UI slice.
- **No rich-text editor.** That is the planned canvas-editor slice.
- **No grants or approval UI,** which are product governance.
- **No routing.** The shell is router-agnostic.

## 2. Why now

- **No product shares the layout today.** Desk has it in one 1,737-line `App.tsx`, where right-pane
  priority is a nested ternary. The cookbook apps (`personal-assistant`, `digital-marketing-team`)
  each use their own layout. The public docs say nothing about app layout.
- **The SDK kit and Desk have drifted.** The kit ships 5 primitives under `--nv-*` tokens. Desk does
  not import it at all: it themes from `@meganovaai/app-kit` with bare `:root` tokens whose values
  match the kit almost 1:1 under different names.
- **More apps are coming.** libraos/libraos#1069 makes "apps" a first-class idea: Desk and the
  applications after it lease resources from the kernel. A shared layout is how those apps look and
  behave like one product family.

## 3. Components

All components are layout and chrome only, apply `.nv-*` classes and are themed by `--nv-*` tokens.
None calls a LibraOS API.

### 3.1 `WorkspaceShell`
The grid and the responsive rules.

```tsx
<WorkspaceShell
  nav={<NavRail …/>}
  context={pane}            // a ContextPane value (§3.4) — required, see §5
  topbar?={ReactNode}       // optional header inside the work column
>
  {work}                    // the work pane: list / board / detail / editor
</WorkspaceShell>
```

- **Columns:** `var(--nv-nav-w) minmax(0,1fr) var(--nv-context-w)`.
  - `--nv-nav-w` is 260px, or 0 when the rail is collapsed.
  - `--nv-context-w` is the dock width (default 312px, resizable) or the canvas width
    (`minmax(380px, 0.95fr)`).
  - With no context pane, the grid has two columns.
- **Breakpoints:** the same as Desk, and both are CSS variables so a product can tune them.
  - **≤ 1100px:** the dock becomes a **sheet**, opened by a floating launcher, with a focus trap and
    Escape. The canvas then overlays the work pane.
  - **≤ 720px:** the nav becomes a **drawer** behind a hamburger: `inert` and `aria-hidden` when
    closed, closing on navigation, on a backdrop click or on Escape.
- **Landmarks:** `nav` (rail), `main` (work), `aside` (context pane), each with an `aria-label`.
  Inert and `aria-hidden` are applied correctly in drawer and sheet modes.

### 3.2 `NavRail`
- **Slots:** `brand`, `items` (the product renders its own links, so it works with any router),
  `recents?`, `footer?` (e.g. an account menu).
- **Collapse:** the rail collapses to 0 with a restore affordance, and the collapsed state persists
  (§4).

### 3.3 `DockFrame`
The copilot dock's chrome. The product supplies the thread and composer as children.

```tsx
<DockFrame
  title={…} actions?={…}          // header: agent picker, new-thread, etc. (product)
  variant?: "docked" | "chat-first" | "embedded"
  persistKey: string              // e.g. "desk" → keys under §4
  onToggle?(collapsed: boolean)
>
  {threadAndComposer}
</DockFrame>
```

**Behaviour, ported from Desk's `CopilotDock` with its tests:**
- **First visit opens it.** It starts open when no stored state exists, then honours the user's choice
  for good. Collapsed and width are global per product; they are not per surface.
- **Collapsed** is a slim rail with a rotated label and an expand button. It never disappears
  entirely.
- **Resizing:** a draggable divider, clamped between a minimum and maximum, persisted.
- **Toggle:** ⌘/Ctrl-J from anywhere. Plain `j` and other modifier combinations are ignored. The
  shortcut is exposed as `useDockToggle()` so a command palette can call it too.
- **Variants:**
  - `chat-first`: full width, with no collapse or resize, for a page that *is* the assistant;
  - `embedded`: no own header, for a dock placed inside a tab, like Desk's project page.
- **Narrow screens:** in sheet mode the frame renders as a sheet with the launcher (§3.1).

### 3.4 `ContextPane` value and `useContextPane`
One right pane at a time, with a fixed priority. This replaces Desk's nested ternary.

```ts
type ContextPane =
  | { kind: "canvas"; render: () => ReactNode; onClose(): void }
  | { kind: "dock"; render: () => ReactNode }
  | { kind: "none"; reason: string };   // §5 — a declared, reviewable deviation
```

- **Priority: canvas > dock > none.** Opening a canvas replaces the dock. Closing it returns to the
  dock if the surface has one.
- **`useContextPane()`:** returns `openCanvas(render)`, `closeCanvas()`, `isCanvasOpen`, and canvas
  history (back and forward).
- **Canvas history:** the frame is generic; Desk's `openCanvasWith` becomes a thin call to
  `openCanvas`.

### 3.5 `CanvasFrame`
The canvas's chrome. The body is the product's: Desk's TipTap editor, its redline, IC-memo or sheet
views, or anything else.
- **Header:** title, close, and a version bar (`versionIndex`, `versionCount`, previous/next).
- **Export:** `exportFilename(title | markdown)`, using the rules Desk tests in `filenameFromMarkdown`
  and `exportStem`.
- **Scroll container:** a body slot with one documented scroll container, the contract pinned by
  Desk's `CanvasPanel.layout.test.tsx`.
- **Kinds:** an `artifactKinds` registry pattern (`describeArtifactKind`), whose entries the product
  registers.

## 4. Persistence

- **Storage adapter:** `createLayoutStore({ namespace, storage? })`. It defaults to `localStorage`,
  with every access wrapped in `try`/`catch`, and falls back to in-memory when storage is blocked.
  The layout then renders with its defaults.
- **Keys:**
  - `<namespace>.nav.collapsed`
  - `<namespace>.dock.collapsed`
  - `<namespace>.dock.width`
- **Migration:** Desk's current keys (`novadesk.copilot.collapsed` and `.width`) are read once as
  legacy fallbacks, the same way Desk already migrates its own older keys, so no user loses their
  setting.
- **Kept out of the SDK:** per-scope agent choice and per-context threads are product state.

## 5. The convention, made checkable

The Desk rule "any surface without the dock needs a stated reason" becomes part of the API:
`WorkspaceShell` requires a `context`, and opting out is
`{ kind: "none", reason: "admin console" }`.
- **Development builds** warn on a missing or empty `reason`.
- **Products** can list every route's pane kind in a test, which turns the "deviations need a reason
  in the PR" rule into a diff a reviewer sees.

Desk's current deviations become declared `none` cases. A dock that lives *inside* the work pane is
a `DockFrame` variant there, not a context pane:
- `admin`, `settings`, `connectors`, `today`, `developer`: context `{ kind: "none", reason }`, a
  settings or queue page with nothing to ground;
- `chat`: the work pane renders `DockFrame variant="chat-first"`. Context
  `{ kind: "none", reason: "the page is the assistant" }`.
- `project`: the work pane's Chats tab renders `DockFrame variant="embedded"`. Context
  `{ kind: "none", reason: "dock embedded in the Chats tab" }`.

## 6. Grounding contract (types only)

The SDK defines the **shape**; the product supplies the scopes:

```ts
interface SurfaceContext<Scope extends string = string> {
  scope: Scope;               // product-defined union, e.g. Desk's 12 scopes
  identity: string;           // coarse: a change remounts the dock + resets the thread
  key?: string;               // fine: a change rebuilds the transport, keeps the thread
  label?: string;             // shown in the dock header ("Grounded in: Deal · Acme")
}
```

- **Two levels of identity.** Desk's `contextIdentity` and `contextKey` become the documented
  `identity` and `key` semantics. A list surface grounds in its collection plus the active filter; a
  detail surface grounds in the open record. The product implements each of these.
- **Transport stays in the product.** How the dock answers (Desk's `askProject` or corporate chat) is
  product code. A future chat/AG-UI slice may supply a default transport.

## 7. Tokens

- **`--nv-*` stays canonical.** This slice adds what the shell, dock and canvas need:
  - `--nv-nav-w`, `--nv-context-w`, `--nv-context-min`, `--nv-context-max`;
  - `--nv-bp-sheet` (1100px), `--nv-bp-drawer` (720px);
  - the status tokens Desk uses that the kit lacks: `--nv-danger`, `--nv-danger-ink`, `--nv-warn-bg`,
    `--nv-warn-ink`, `--nv-warn-line`.
- **An alias sheet for migration:** `@libraos/react-ui/aliases.css` maps Desk's bare tokens
  (`--paper`, `--ink`, `--accent`, …) onto `--nv-*`. Desk can then adopt the kit without renaming
  every rule at once, and drops the aliases at the end.

## 8. Accessibility

- **Landmarks and labels** as in §3.1.
- **Keyboard and focus:**
  - The rail toggle, the dock collapse and resize controls, and the sheet launcher are keyboard
    operable. The resize divider also responds to arrow keys.
  - Focus moves into the sheet or drawer when it opens and returns to the trigger when it closes.
  - Escape closes the sheet, the drawer and the canvas, in that order of precedence.
- **Collapsed rail:** its label is readable by screen readers, not just rotated visually.
- **Reduced motion:** honoured for the sheet and drawer transitions.

## 9. Testing

Vitest + Testing Library (jsdom), testing behaviour, as in slice 1.
- **Shell:** the grid classes for each pane kind; drawer and sheet mode at both breakpoints (via
  `matchMedia` mocks); landmarks; inert and `aria-hidden` states.
- **DockFrame:**
  - first visit opens it, and a stored collapsed value is honoured;
  - the ⌘J and Ctrl-J toggle works both ways and ignores `j` with other modifiers;
  - collapsing leaves the rail;
  - resizing persists and is clamped;
  - `chat-first` has no collapse control, and `embedded` has no header;
  - the legacy keys migrate;
  - blocked storage still renders.
- **ContextPane:** canvas pre-empts the dock, closing it restores the dock, history works, and `none`
  without a reason warns.
- **CanvasFrame:** the version bar, the export file-name rules (Desk's cases), and the scroll
  container.
- **Demo:** the `examples/react-ui-demo` app gains a three-pane page: a list in the work pane, the dock
  with a fake thread, and a button that opens a canvas.

## 10. Rollout

1. **SDK.** Implement this slice in `clients/react-ui` and bump to `0.2.0-alpha.0`. The package stays
   private, as slice 1 decided.
2. **Docs.** Add a "Workspace layout" guide to `libraos/docs`: what goes in each pane, the
   grounding levels, when `none` is acceptable, and a code sample. The guide is public, but nothing
   in it is product-internal.
3. **Cookbook.** Move `apps/personal-assistant` onto `WorkspaceShell` as the reference app.
4. **Desk migration,** as its own plan in `libraos/desk`:
   1. aliases.css and the kit's stylesheet;
   2. `WorkspaceShell` and `NavRail` in `App.tsx`, replacing the grid and the right-pane ternary with
      `ContextPane` values;
   3. `CopilotDock` keeps its domain logic but renders inside `DockFrame`;
   4. `CanvasPanel` renders inside `CanvasFrame`.

   Desk's existing tests (CopilotDock, App and Canvas) must stay green at every step. That is the
   acceptance bar, because they already pin this behaviour.
5. **Desk CLAUDE.md** then states the convention as "use `@libraos/react-ui`'s `WorkspaceShell`", not
   as prose.

## 11. Inventory of the source (Desk `origin/main`, 2026-10-05)

- **Shell:** `.app` grid in `App.tsx` (~1085–1099) and `styles.css` (110–125), with modifier
  classes (`canvas-on`, `copilot-on`, `no-right`, `rail-collapsed`, …).
  - **Breakpoints:** CSS `styles.css` 438, 499; mirrored by `matchMedia` in `App.tsx` 170–175.
  - **Hamburger, drawer and sheet:** `App.tsx` 1126–1142, 1431–1440, 1600–1660.
- **Right pane:** a single ternary, canvas, else dock or sheet, else the legacy context aside, else
  nothing (`App.tsx` 1582–1683). `showCopilot` excludes admin, chat, today, project and canvas-open
  (1082).
- **Dock:** `CopilotDock(context, chatFirst, embedded, grant, onGrantResolved)` (526–560).
  - **Persistence** (`copilot/persist.ts`): collapsed and width are global, with first-visit-open
    (48–66).
  - **Toggle and rail:** ⌘J 830–842; collapsed rail 1368–1382.
  - **Coupling:** heavily tied to Desk (`lib/chat`, `lib/brain`, legal and EqualDocs, grants, i18n),
    which is why only its frame moves.
- **Context:** `copilot/context.ts`, a 12-scope union with `contextIdentity` and `contextKey`.
- **Canvas:** `CanvasPanel` props (23–43), `filenameFromMarkdown` and `exportStem` (46–72), and
  `openCanvasWith` in `App.tsx` (~481–489).
- **Tests that pin behaviour:** `CopilotDock.test.tsx` (~1,200 lines), `CanvasPanel.test.tsx`,
  `CanvasPanel.layout.test.tsx`, `App.test.tsx`.
- **Overlays that are not part of the grid:** `MemoryPanel` (a modal) and `AgentGuideDrawer` (a
  fixed drawer). They stay product overlays.

## 12. Open questions

1. **Where routing lives.** The shell is router-agnostic. Should the SDK *also* ship an optional
   `react-router` adapter, for active-link styling in `NavRail` and route-declared `ContextPane`?
   Proposed: no, not in this slice.
2. **Where the theme comes from for Desk.** Should Desk keep `@meganovaai/app-kit` for anything after
   migration, or does `@libraos/react-ui` replace it entirely? This needs an owner's decision before
   step 4.
3. **Publishing.** The kit is private. Do third-party app builders (cookbook, external developers)
   need it public for the guide in §10 step 2 to be usable? Proposed: decide with the docs guide; until
   then, the guide shows the pattern with plain CSS alongside the kit.
