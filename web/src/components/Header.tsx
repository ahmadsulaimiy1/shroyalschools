import Link from "next/link";
import type { Locale } from "@/lib/i18n";
import { getDict } from "@/lib/dictionary";
import { SITE } from "@/lib/site";
import MobileNav from "./MobileNav";

/**
 * Site header.
 *
 * Fixes two V1 defects:
 *  - "المصادر والمعرفة" was href="#" — a dead top-level item on all 14 pages.
 *    It now points at a real /resources hub (docs/01 §3).
 *  - There was no login link anywhere, so enrolled students could not reach
 *    the LMS from the marketing site (docs/09 §5).
 */
export default function Header({ locale }: { locale: Locale }) {
  const t = getDict(locale);
  const base = `/${locale}`;

  const links = [
    { href: base, label: t.nav.home },
    { href: `${base}/about`, label: t.nav.about },
    { href: `${base}/resources`, label: t.nav.resources },
    { href: `${base}/faq`, label: t.nav.faq },
    { href: `${base}/policies`, label: t.nav.policies },
    { href: `${base}/contact`, label: t.nav.contact },
  ];

  return (
    <header className="sticky top-0 z-40 bg-white/95 backdrop-blur border-b border-primary/10 no-print">
      <div className="container-x flex items-center justify-between gap-4 py-3">
        <Link
          href={base}
          className="flex items-center gap-3 shrink-0"
          aria-label={SITE.nameAr}
        >
          <span
            aria-hidden="true"
            className="grid h-11 w-11 place-items-center rounded-xl bg-primary text-white font-[family-name:var(--font-amiri)] text-xl font-bold"
          >
            إ
          </span>
          <span className="hidden sm:block leading-tight">
            <span className="block font-[family-name:var(--font-amiri)] font-bold text-primary">
              {SITE.shortAr}
            </span>
            <span className="block text-xs text-gray-600">{SITE.parentOrgAr}</span>
          </span>
        </Link>

        <nav aria-label={t.nav.menu} className="hidden lg:block">
          <ul className="flex items-center gap-1">
            {links.map((l) => (
              <li key={l.href}>
                <Link
                  href={l.href}
                  className="rounded-lg px-3 py-2 text-sm font-medium text-gray-700 transition-colors hover:bg-primary/5 hover:text-primary"
                >
                  {l.label}
                </Link>
              </li>
            ))}
          </ul>
        </nav>

        <div className="hidden lg:flex items-center gap-2">
          <a
            href={SITE.lmsLogin}
            className="rounded-lg px-3 py-2 text-sm font-medium text-primary hover:bg-primary/5"
          >
            {t.nav.login}
          </a>
          <Link href={`${base}/register`} className="btn btn-primary text-sm !px-5 !py-2.5">
            {t.common.registerNow}
          </Link>
        </div>

        <MobileNav locale={locale} links={links} />
      </div>
    </header>
  );
}
