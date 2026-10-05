# @libraos/react-ui

A private alpha UI kit for LibraOS company-facing products: the Atelier
design system plus a small set of primitives and a workspace-layout slice.
Not yet stable — expect breaking changes between `0.x` releases.

Every surface renders inside a `.nv` root. Import the stylesheet once at
your app's entry point, and optionally the alias sheet if you want the
shorthand custom-property names:

```ts
import "@libraos/react-ui/styles.css";
import "@libraos/react-ui/aliases.css"; // optional
```

```tsx
<div className="nv" data-nv-scope="corporate">
  <App />
</div>
```

## Workspace layout

The layout slice gives every primary surface the same shape: a collapsible
nav rail, a work pane, and a right-hand context pane that is either a
docked copilot or a full canvas. Wire it up with `LayoutProvider` (persists
nav/dock state) and `ContextPaneProvider` (owns the canvas history) around
a `WorkspaceShell`:

```tsx
import {
  LayoutProvider, ContextPaneProvider, WorkspaceShell, NavRail,
  DockFrame, CanvasFrame, useContextPane, Button,
} from "@libraos/react-ui";

function TicketsSurface() {
  const { openCanvas, closeCanvas } = useContextPane();
  return (
    <WorkspaceShell
      nav={<NavRail brand="Desk"><a href="/inbox">Inbox</a></NavRail>}
      context={{ kind: "dock", render: () => <DockFrame title="Copilot">…</DockFrame> }}
    >
      <Button onClick={() => openCanvas(() => (
        <CanvasFrame title="Offer letter" onClose={closeCanvas}>…draft…</CanvasFrame>
      ))}>
        Open draft
      </Button>
    </WorkspaceShell>
  );
}

export function App() {
  return (
    <LayoutProvider namespace="tickets">
      <ContextPaneProvider>
        <TicketsSurface />
      </ContextPaneProvider>
    </LayoutProvider>
  );
}
```

`WorkspaceShell`'s `context` prop takes one of three shapes: `{ kind:
"canvas", render, onClose }`, `{ kind: "dock", render }`, or `{ kind:
"none", reason }`. A surface with no context pane isn't silently missing
one — `reason` is the reviewable deviation from the Copilot-Everywhere
convention, and an empty `reason` logs a dev warning. While a canvas is
open (via `useContextPane().openCanvas`), it takes over the context pane
regardless of what `context` says, and `closeCanvas()` (or the canvas's own
close button) returns it to the surface's own `context`.

### `SurfaceContext`

```ts
type SurfaceContext<Scope extends string = string> = {
  scope: Scope; identity: string; key?: string; label?: string;
};
```

This is what a surface hands to the copilot to ground it. `scope` names the
kind of surface (e.g. `"ticket"`, `"contact"`; the product defines the union)
and `label` is a human-readable name for the dock header, never compared for
identity. What a surface grounds in: **a list surface grounds in its
collection plus the active filter; a detail surface grounds in the open
record.** The two identity levels carry that contract:

- **`identity`** (coarse) — a change **remounts the dock and resets the
  thread**. Use the surface and record, e.g. `"deal:42"` or `"deals"`.
- **`key`** (fine, optional) — a change **rebuilds the transport but keeps the
  thread**. Use what is volatile within the same identity, e.g. a list's
  active filter, so switching filters re-grounds the copilot without wiping
  the conversation.

In practice the product keys its dock content on `identity` (React `key`) and
feeds `key` to its transport. Transport — how the dock answers — stays product
code.

### Keeping dock state

`DockFrame` keeps its children mounted while the dock is collapsed to its
rail, while the narrow-screen sheet is closed, and across the 1100px
breakpoint: it hides them (`hidden` + `inert`) rather than unmounting them, so
a draft, an in-flight turn or a scroll position survives. Whether thread state
lives in the dock's children or above them is your choice; it is the
`identity` change above, not collapsing, that resets it. (A canvas opening
does replace the dock in the context pane, so state that must survive a canvas
belongs above `WorkspaceShell`.)

⌘/Ctrl-J toggles the dock that is showing — collapse/expand, or open/close the
sheet. On a surface with no docked `DockFrame` (a `none` pane, an open canvas,
a `chat-first`/`embedded` frame, or while the nav drawer is open) it does
nothing and leaves the browser's own shortcut alone. `useDockToggle()` returns
a function that toggles the persisted dock state for a command palette.

### `LayoutProvider` props must be stable

`namespace`, `storage` and `legacy` build the layout store; a new value on
every render rebuilds it. Pass string literals, hoist objects to module scope,
or memoize them:

```tsx
const LEGACY = { dockCollapsed: ["copilot.collapsed"] }; // module scope, not inline
<LayoutProvider namespace="desk" legacy={LEGACY}>…</LayoutProvider>
```

### Linking the kit locally

When you depend on the kit through `file:` (as `examples/react-ui-demo` does),
it resolves `react` from its own `node_modules`, and two copies of React fail
at runtime with `Cannot read properties of null (reading 'useRef')`. Dedupe
`react`/`react-dom` in your bundler, e.g. for Vite:

```ts
export default defineConfig({ plugins: [react()], resolve: { dedupe: ["react", "react-dom"] } });
```
