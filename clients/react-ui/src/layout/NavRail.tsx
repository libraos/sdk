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
