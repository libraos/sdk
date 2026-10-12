import { useEffect, useState } from "react";
export const SHEET_QUERY = "(max-width: 1100px)";
export const DRAWER_QUERY = "(max-width: 720px)";
function matches(query: string): boolean {
  try { return typeof window !== "undefined" && typeof window.matchMedia === "function" ? window.matchMedia(query).matches : false; } catch { return false; }
}
export function useMediaQuery(query: string): boolean {
  const [hit, setHit] = useState(() => matches(query));
  useEffect(() => {
    if (typeof window === "undefined" || typeof window.matchMedia !== "function") return;
    const mql = window.matchMedia(query);
    const on = () => setHit(mql.matches);
    on();
    mql.addEventListener?.("change", on);
    return () => mql.removeEventListener?.("change", on);
  }, [query]);
  return hit;
}
