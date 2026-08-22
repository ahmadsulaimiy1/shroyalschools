"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import type { Locale } from "@/lib/i18n";
import { getDict } from "@/lib/dictionary";
import { SITE } from "@/lib/site";

/**
 * Mobile navigation.
 *
 * V1's menu had no focus trap, no Escape handler and did not lock body scroll
 * (docs/03 §4). This uses a native <dialog>, which provides focus trapping,
 * Escape-to-close and the top layer for free.
 */
export default function MobileNav({
  locale,
  links,
}: {
  locale: Locale;
  links: { href: string; label: string }[];
}) {
  const t = getDict(locale);
  const ref = useRef<HTMLDialogElement>(null);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const d = ref.current;
    if (!d) return;
    if (open && !d.open) d.showModal();
    if (!open && d.open) d.close();
  }, [open]);

  useEffect(() => {
    document.body.style.overflow = open ? "hidden" : "";
    return () => {
      document.body.style.overflow = "";
    };
  }, [open]);

  return (
    <div className="lg:hidden">
      <button
        type="button"
        onClick={() => setOpen(true)}
        aria-label={t.nav.menu}
        aria-expanded={open}
        className="grid h-11 w-11 place-items-center rounded-lg border border-primary/20 text-primary"
      >
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="M3 6h18M3 12h18M3 18h18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
        </svg>
      </button>

      <dialog
        ref={ref}
        onClose={() => setOpen(false)}
        onClick={(e) => {
          if (e.target === ref.current) setOpen(false);
        }}
        className="m-0 h-full max-h-full w-[min(20rem,85vw)] max-w-full bg-surface-warm p-0 backdrop:bg-black/50 ms-auto"
      >
        <div className="flex h-full flex-col p-5">
          <div className="mb-6 flex items-center justify-between">
            <span className="font-[family-name:var(--font-amiri)] font-bold text-primary">
              {SITE.shortAr}
            </span>
            <button
              type="button"
              onClick={() => setOpen(false)}
              aria-label={t.nav.close}
              className="grid h-10 w-10 place-items-center rounded-lg border border-primary/20 text-primary"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                <path d="M6 6l12 12M18 6L6 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
              </svg>
            </button>
          </div>

          <nav aria-label={t.nav.menu} className="flex-1">
            <ul className="space-y-1">
              {links.map((l) => (
                <li key={l.href}>
                  <Link
                    href={l.href}
                    onClick={() => setOpen(false)}
                    className="block rounded-lg px-3 py-3 font-medium text-gray-800 hover:bg-primary/5 hover:text-primary"
                  >
                    {l.label}
                  </Link>
                </li>
              ))}
            </ul>
          </nav>

          <div className="space-y-2 border-t border-primary/10 pt-4">
            <Link
              href={`/${locale}/register`}
              onClick={() => setOpen(false)}
              className="btn btn-primary w-full"
            >
              {t.common.registerNow}
            </Link>
            <a href={SITE.lmsLogin} className="btn btn-outline w-full">
              {t.nav.login}
            </a>
          </div>
        </div>
      </dialog>
    </div>
  );
}
