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
