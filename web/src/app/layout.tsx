import type { ReactNode } from "react";
import "./globals.css";

/**
 * Root layout is intentionally minimal: the real <html> attributes are set in
 * the [locale] layout, because dir and lang differ per locale.
 * V1 shipped dir="rtl" lang="ar" on its English, French and Italian pages.
 */
export default function RootLayout({ children }: { children: ReactNode }) {
  return children;
}
