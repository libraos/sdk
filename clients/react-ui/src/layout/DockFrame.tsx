import { useContext, useEffect, useRef, useState, type ReactNode } from "react";
import { DockToggleRegistry, useLayout, type DockToggleHandler } from "./LayoutProvider";
import { SHEET_QUERY, useMediaQuery } from "./useMediaQuery";
import { DOCK_MAX_WIDTH, DOCK_MIN_WIDTH } from "./store";
import { IconButton } from "../components/IconButton";

export const DOCK_KEY_STEP = 16;
export interface DockLabels { name?: string; collapse?: string; expand?: string; open?: string; close?: string; resize?: string }

/** What a Tab cycle may land on: enabled controls and real links, outside any hidden or inert subtree. */
const FOCUSABLE = 'a[href], button:not([disabled]), textarea:not([disabled]), input:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])';
function focusables(root: HTMLElement): HTMLElement[] {
  return Array.from(root.querySelectorAll<HTMLElement>(FOCUSABLE)).filter((el) => !el.closest("[hidden],[inert]"));
}

export function DockFrame({ title, actions, variant = "docked", labels = {}, children }: {
  title?: ReactNode; actions?: ReactNode; variant?: "docked" | "chat-first" | "embedded"; labels?: DockLabels; children: ReactNode;
}) {
  const l = useLayout();
  const name = labels.name ?? "Copilot";
  const sheetMode = useMediaQuery(SHEET_QUERY) && variant === "docked";
  const [sheetOpen, setSheetOpen] = useState(false);
  const launcherRef = useRef<HTMLButtonElement>(null);
  const frameRef = useRef<HTMLElement>(null);
  // the launcher is unmounted while the sheet is open, so focus returns after it re-mounts
  const restoreFocus = useRef(false);
  const closeSheet = () => { restoreFocus.current = true; setSheetOpen(false); };

  useEffect(() => { if (!sheetMode) setSheetOpen(false); }, [sheetMode]);
  useEffect(() => {
    if (!sheetOpen && restoreFocus.current) { restoreFocus.current = false; launcherRef.current?.focus(); }
  }, [sheetOpen]);
  useEffect(() => {
    if (!sheetOpen) return;
    const el = frameRef.current;
    if (el) focusables(el)[0]?.focus();
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") { e.preventDefault(); closeSheet(); return; }
      if (e.key !== "Tab" || !el) return;
      const f = focusables(el);
      if (!f.length) return;
      const first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    };
    window.addEventListener("keydown", onKey, true); // capture: sheet beats canvas (ruling P4c)
    return () => window.removeEventListener("keydown", onKey, true);
  }, [sheetOpen]);

  // tracks the in-flight drag's teardown so a divider that disappears mid-drag
  // (sheet breakpoint crossed, dock collapsed via ⌘J, or DockFrame unmounts)
  // doesn't leave document-level listeners still calling setDockWidth
  const endDrag = useRef<(() => void) | null>(null);
  const startDrag = (e: React.MouseEvent) => {
    endDrag.current?.();
    const startX = e.clientX, startW = l.dockWidth;
    const move = (ev: MouseEvent) => l.setDockWidth(startW + (startX - ev.clientX));
    const up = () => endDrag.current?.();
    endDrag.current = () => {
      document.removeEventListener("mousemove", move);
      document.removeEventListener("mouseup", up);
      endDrag.current = null;
    };
    document.addEventListener("mousemove", move); document.addEventListener("mouseup", up);
  };
  useEffect(() => () => endDrag.current?.(), [sheetMode, l.dockCollapsed]);

  // ⌘J: a docked frame registers itself with the provider while mounted; the handler reads the
  // latest render through a ref so the registration itself never churns.
  const register = useContext(DockToggleRegistry);
  const onToggle = useRef<DockToggleHandler>(() => false);
  useEffect(() => {
    onToggle.current = () => {
      if (frameRef.current?.parentElement?.closest("[inert]")) return false; // e.g. behind the nav drawer
      if (sheetMode) { if (sheetOpen) closeSheet(); else setSheetOpen(true); }
      else l.toggleDock();
      return true;
    };
  });
  useEffect(() => {
    if (variant !== "docked" || !register) return;
    return register(() => onToggle.current());
  }, [variant, register]);

  const collapsed = variant === "docked" && !sheetMode && l.dockCollapsed;
  const visible = sheetMode ? sheetOpen : !collapsed;
  // One frame element in a fixed tree position, whatever the mode: collapse, the sheet closing and
  // the 1100px crossing hide it (hidden + inert) instead of unmounting it, so a stateful child —
  // a draft, an in-flight turn, a scroll position — survives. The launcher and the rail are
  // siblings rendered before it; each slot is a conditional, so positions never shift.
  return (
    <>
      {sheetMode && !sheetOpen && (
        <IconButton ref={launcherRef} className="nv-dock__launcher" aria-label={labels.open ?? `Open ${name}`} aria-expanded={false} onClick={() => setSheetOpen(true)}>✦</IconButton>
      )}
      {collapsed && (
        <div className="nv-dock nv-dock--collapsed">
          <button type="button" className="nv-dock__rail" aria-label={labels.expand ?? `Expand ${name}`} onClick={() => l.setDockCollapsed(false)}>
            <span className="nv-dock__rail-label">{name}</span>
          </button>
        </div>
      )}
      <section ref={frameRef} className={`nv-dock nv-dock--${sheetMode ? "sheet" : variant}`}
        aria-label={name} role={sheetMode ? "dialog" : undefined} aria-modal={sheetMode ? "true" : undefined}
        hidden={!visible || undefined} inert={!visible || undefined}>
        {variant === "docked" && !sheetMode && (
          <div className="nv-dock__divider" role="separator" aria-orientation="vertical" tabIndex={0}
            aria-label={labels.resize ?? `Resize ${name}`} aria-valuemin={DOCK_MIN_WIDTH} aria-valuemax={DOCK_MAX_WIDTH} aria-valuenow={l.dockWidth}
            onMouseDown={startDrag}
            onKeyDown={(e) => {
              if (e.key === "ArrowLeft") { e.preventDefault(); l.setDockWidth(l.dockWidth + DOCK_KEY_STEP); }
              if (e.key === "ArrowRight") { e.preventDefault(); l.setDockWidth(l.dockWidth - DOCK_KEY_STEP); }
            }} />
        )}
        {variant !== "embedded" && (
          <div className="nv-dock__header">
            <div style={{ flex: 1, minWidth: 0 }}>{title}</div>
            {actions}
            {variant === "docked" && !sheetMode && <IconButton size="sm" aria-label={labels.collapse ?? `Collapse ${name}`} onClick={() => l.setDockCollapsed(true)}>›</IconButton>}
            {sheetMode && <IconButton size="sm" aria-label={labels.close ?? `Close ${name}`} onClick={closeSheet}>×</IconButton>}
          </div>
        )}
        <div className="nv-dock__body">{children}</div>
      </section>
    </>
  );
}
