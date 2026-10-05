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

This is what a surface hands to the copilot to ground it: `scope` names
the kind of surface (e.g. `"ticket"`, `"contact"`), `identity` is the
stable id of what the surface is about — a record id, or a collection+view
for a list surface — `key` optionally distinguishes a sub-view of that same
identity (a tab, a filter), and `label` is a human-readable name for
display, not for identity comparisons.
