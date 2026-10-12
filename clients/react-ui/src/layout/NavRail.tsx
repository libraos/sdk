import { useContext, type ReactNode } from "react";
import { useLayout } from "./LayoutProvider";
import { ShellContext } from "./WorkspaceShell";
import { IconButton } from "../components/IconButton";
export function NavRail({ brand, recents, footer, collapseLabel = "Collapse navigation", children }: { brand?: ReactNode; recents?: ReactNode; footer?: ReactNode; collapseLabel?: string; children: ReactNode }) {
  const { setNavCollapsed } = useLayout();
  const shell = useContext(ShellContext);
  // In drawer mode (≤720px) collapsing makes no sense — the drawer is already transient — so the
  // same button closes the drawer (focus returns to the hamburger) and leaves nav.collapsed alone.
  const button = shell?.drawer
    ? <IconButton aria-label={shell.labels.closeNav ?? "Close navigation"} size="sm" onClick={shell.closeDrawer}>×</IconButton>
    : <IconButton aria-label={collapseLabel} size="sm" onClick={() => setNavCollapsed(true)}>‹</IconButton>;
  return (
    <div className="nv-navrail">
      <div className="nv-navrail__brand">{brand}{button}</div>
      <div className="nv-navrail__items">{children}</div>
      {recents && <div className="nv-navrail__recents">{recents}</div>}
      {footer && <div className="nv-navrail__footer">{footer}</div>}
    </div>
  );
}
