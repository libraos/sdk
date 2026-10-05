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
  const restoreFocusRef = useRef(false);

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
  useEffect(() => {
    // Focus can only land on the hamburger once <main> is no longer inert. That attribute
    // is removed by this same render (drawerOpen -> false), but only after it commits —
    // calling .focus() synchronously inside closeDrawer() would still target an inert
    // ancestor and silently no-op. Restoring focus from an effect keyed on drawerOpen
    // guarantees the DOM mutation has landed first.
    if (!drawerOpen && restoreFocusRef.current) {
      restoreFocusRef.current = false;
      burgerRef.current?.focus();
    }
  }, [drawerOpen]);
  function closeDrawer() { restoreFocusRef.current = true; setDrawerOpen(false); }

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
      <main className="nv-shell__work" aria-label={labels.work ?? "Work"} inert={drawerOpen || undefined}>
        {drawer && <IconButton ref={burgerRef} className="nv-shell__hamburger" aria-label={labels.openNav ?? "Open navigation"} aria-expanded={drawerOpen} onClick={() => setDrawerOpen(true)}>☰</IconButton>}
        {!drawer && layout.navCollapsed && <IconButton className="nv-shell__nav-restore" aria-label={labels.restoreNav ?? "Show navigation"} onClick={() => layout.setNavCollapsed(false)}>›</IconButton>}
        {topbar}
        {children}
      </main>
      {pane.kind !== "none" && <aside className="nv-shell__context" aria-label={labels.context ?? (pane.kind === "canvas" ? "Canvas" : "Copilot")} inert={drawerOpen || undefined}>{pane.render()}</aside>}
    </div>
  );
}
