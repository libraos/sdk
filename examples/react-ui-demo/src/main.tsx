import { useState, type CSSProperties } from "react";
import { createRoot } from "react-dom/client";
import {
  Button, IconButton, Card, Composer, Toggle,
  LayoutProvider, ContextPaneProvider, WorkspaceShell, NavRail, DockFrame, CanvasFrame,
  useContextPane,
} from "@libraos/react-ui";
import "@libraos/react-ui/styles.css";

function Primitives() {
  const [scope, setScope] = useState("corporate");
  const [text, setText] = useState("");
  return (
    <div className="nv" data-nv-scope={scope} style={{ minHeight: "100vh", background: "var(--nv-paper)", padding: 40, display: "flex", flexDirection: "column", gap: 20, maxWidth: 720, margin: "0 auto" }}>
      <Toggle
        options={[{ value: "corporate", label: "Corporate" }, { value: "personal", label: "Personal" }]}
        value={scope}
        onChange={setScope}
      />
      <div style={{ display: "flex", gap: 10 }}>
        <Button variant="primary">Primary</Button>
        <Button variant="ghost">Ghost</Button>
        <Button variant="subtle">Subtle</Button>
        <IconButton aria-label="icon">★</IconButton>
      </div>
      <Card title="Sources">Cited knowledge appears here.</Card>
      <Composer
        value={text}
        onChange={setText}
        onSubmit={() => setText("")}
        placeholder="Ask for a brief, draft, or summary…"
        actions={<IconButton aria-label="Send">↑</IconButton>}
      />
      {/* Rebrand proof: a violet accent override scoped to one subtree */}
      <div className="nv" style={{ "--nv-accent": "#5b4bdb", "--nv-accent-ink": "#3f33a8" } as CSSProperties}>
        <Button variant="primary">Rebranded accent</Button>
      </div>
    </div>
  );
}

// Fake data only — this demo never talks to a backend.
const DEALS = [
  { id: "d1", name: "Acme Corp — renewal", value: "$42,000" },
  { id: "d2", name: "Globex — new seats", value: "$18,500" },
  { id: "d3", name: "Initech — pilot", value: "$6,200" },
  { id: "d4", name: "Umbrella — upsell", value: "$27,900" },
  { id: "d5", name: "Soylent — renewal", value: "$11,000" },
];

function DealsSurface() {
  const { openCanvas, closeCanvas } = useContextPane();
  return (
    <WorkspaceShell
      nav={
        <NavRail brand="Desk">
          <a href="#deals">Deals</a>
          <a href="#contacts">Contacts</a>
          <a href="#reports">Reports</a>
        </NavRail>
      }
      context={{ kind: "dock", render: () => (
        <DockFrame title="Copilot">
          <div style={{ padding: 12, display: "flex", flexDirection: "column", gap: 10 }}>
            <p style={{ margin: 0 }}>Here's a summary of your open deals this week.</p>
            <p style={{ margin: 0, color: "var(--nv-muted)" }}>Want me to draft a follow-up for any of them?</p>
          </div>
          <Composer value="" onChange={() => {}} onSubmit={() => {}} placeholder="Ask the copilot…" />
        </DockFrame>
      ) }}
    >
      <div style={{ padding: 24, display: "flex", flexDirection: "column", gap: 12 }}>
        <h1 style={{ margin: 0, fontSize: 18 }}>Deals</h1>
        {DEALS.map((deal) => (
          <Card key={deal.id} title={deal.name}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 12 }}>
              <span>{deal.value}</span>
              <Button variant="subtle" onClick={() => openCanvas(() => (
                <CanvasFrame title="Deal memo" onClose={closeCanvas}>
                  <div style={{ padding: 16 }}>
                    <h2 style={{ marginTop: 0 }}>{deal.name}</h2>
                    <p>Value: {deal.value}</p>
                    <p>A drafted memo would appear here, ready for review before sending.</p>
                  </div>
                </CanvasFrame>
              ))}>
                Open memo
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </WorkspaceShell>
  );
}

function Workspace() {
  return (
    <LayoutProvider namespace="demo">
      <ContextPaneProvider>
        <DealsSurface />
      </ContextPaneProvider>
    </LayoutProvider>
  );
}

function Demo() {
  const [view, setView] = useState("primitives");
  return (
    <>
      <div style={{ position: "fixed", top: 10, right: 10, zIndex: 100 }}>
        <Toggle
          options={[{ value: "primitives", label: "Primitives" }, { value: "workspace", label: "Workspace" }]}
          value={view}
          onChange={setView}
        />
      </div>
      {view === "primitives" ? <Primitives /> : <Workspace />}
    </>
  );
}

createRoot(document.getElementById("root")!).render(<Demo />);
