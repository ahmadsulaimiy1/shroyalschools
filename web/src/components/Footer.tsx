import Link from "next/link";
import type { Locale } from "@/lib/i18n";
import { getDict } from "@/lib/dictionary";
import { SITE, WHATSAPP_MEN, waLink } from "@/lib/site";

export default function Footer({ locale }: { locale: Locale }) {
  const t = getDict(locale);
  const base = `/${locale}`;

  return (
    <footer className="mt-24 bg-primary-dark text-white/90 no-print">
      <div className="container-x grid gap-10 py-14 md:grid-cols-3">
        <div>
          <p className="mb-3 font-[family-name:var(--font-amiri)] text-xl font-bold text-white">
            {SITE.nameAr}
          </p>
          <p className="text-sm leading-relaxed text-white/70">
            منصة قرآنية إلكترونية لتعليم كتاب الله تلاوةً وحفظًا، تحت مظلة {SITE.parentOrgAr}.
          </p>
        </div>

        <nav aria-labelledby="footer-links">
          <h2 id="footer-links" className="mb-3 font-bold text-gold-on-dark">
            روابط هامة
          </h2>
          <ul className="space-y-2 text-sm">
            <li><Link href={`${base}/about`} className="hover:text-white">{t.nav.about}</Link></li>
            <li><Link href={`${base}/resources`} className="hover:text-white">{t.nav.resources}</Link></li>
            <li><Link href={`${base}/faq`} className="hover:text-white">{t.nav.faq}</Link></li>
            <li><Link href={`${base}/policies`} className="hover:text-white">{t.nav.policies}</Link></li>
            <li><Link href={`${base}/join`} className="hover:text-white">{t.nav.join}</Link></li>
            <li><a href={SITE.lmsLogin} className="hover:text-white">{t.nav.login}</a></li>
          </ul>
        </nav>

        <div>
          <h2 className="mb-3 font-bold text-gold-on-dark">{t.nav.contact}</h2>
          <ul className="space-y-2 text-sm">
            <li>
              <a href={`tel:${SITE.phone}`} className="hover:text-white" dir="ltr">
                +{SITE.phone}
              </a>
            </li>
            <li>
              <a href={`mailto:${SITE.email}`} className="hover:text-white" dir="ltr">
                {SITE.email}
              </a>
            </li>
            <li>
              <a href={waLink(WHATSAPP_MEN)} className="hover:text-white">
                واتساب
              </a>
            </li>
            <li className="text-white/70">{SITE.addressAr}</li>
          </ul>
        </div>
      </div>

      <div className="border-t border-white/10">
        <div className="container-x flex flex-col items-center justify-between gap-2 py-5 text-xs text-white/60 sm:flex-row">
          <p>© {new Date().getFullYear()} جميع الحقوق محفوظة لمقرأة إتقان.</p>
          <p>{SITE.parentOrgAr}</p>
        </div>
      </div>
    </footer>
  );
}
