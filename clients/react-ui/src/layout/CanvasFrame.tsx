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
