import type { ReactNode } from "react";
import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { LOCALES, isLocale, meta, type Locale } from "@/lib/i18n";
import { getDict } from "@/lib/dictionary";
import { SITE } from "@/lib/site";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import WhatsAppButton from "@/components/WhatsAppButton";

export function generateStaticParams() {
  return LOCALES.map((locale) => ({ locale }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}): Promise<Metadata> {
  const { locale } = await params;
  if (!isLocale(locale)) return {};
  const m = meta(locale);
  const isAr = locale === "ar";

  const title = isAr ? SITE.nameAr : SITE.nameEn;
  // V1 had NO meta description on any of its 14 pages (docs/00 defect #5).
  const description = isAr
    ? "منصة قرآنية إلكترونية تُعنى بتعليم كتاب الله تعالى تلاوةً وحفظًا، وفق منهجية علمية رصينة، وبإشراف نخبة من المعلمين والمعلمات المؤهّلين، تحت مظلة جمعية مكنون لتحفيظ القرآن الكريم."
    : "An online Quran academy teaching recitation and memorisation with a rigorous methodology, under the supervision of qualified teachers and the Maknoon Association for Quran Memorisation.";

  return {
    metadataBase: new URL(SITE.url),
    title: { default: title, template: `%s — ${title}` },
    description,
    alternates: {
      canonical: `/${locale}`,
      languages: Object.fromEntries(LOCALES.map((l) => [meta(l).lang, `/${l}`])),
    },
    // V1 had no Open Graph at all, yet WhatsApp is the academy's main channel,
    // so every share rendered as a bare URL (docs/00 defect #5).
    openGraph: {
      type: "website",
      siteName: title,
      title,
      description,
      locale: m.lang,
      url: `${SITE.url}/${locale}`,
    },
    twitter: { card: "summary_large_image", title, description },
    robots: { index: true, follow: true },
  };
}

export default async function LocaleLayout({
  children,
  params,
}: {
  children: ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();

  const m = meta(locale as Locale);
  const t = getDict(locale as Locale);

  return (
    <html lang={m.lang} dir={m.dir}>
      <body>
        <a href="#main" className="skip-link">
          {t.common.skipToContent}
        </a>
        <Header locale={locale as Locale} />
        <main id="main">{children}</main>
        <Footer locale={locale as Locale} />
        <WhatsAppButton locale={locale as Locale} />
      </body>
    </html>
  );
}
