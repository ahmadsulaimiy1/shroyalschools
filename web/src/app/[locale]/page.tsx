import Link from "next/link";
import { notFound } from "next/navigation";
import { isLocale, type Locale } from "@/lib/i18n";
import { getDict } from "@/lib/dictionary";
import { SITE } from "@/lib/site";
import { Section, SectionHeading } from "@/components/Section";
import AvailabilityBadge from "@/components/AvailabilityBadge";
import { getTracks, summarise } from "@/lib/tracks";
import { HERO, VISION, SERVICES, ADVANTAGES, SECTIONS_INTRO, PARTNERS, FAQ } from "@/content/home";

export default async function HomePage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();
  const t = getDict(locale as Locale);
  const base = `/${locale}`;

  // Sample the men's KSA set to display the seven sections with real status.
  const sections = getTracks({ gender: "male", residency: "ksa" });
  const all = summarise([
    ...getTracks({ gender: "male", residency: "ksa" }),
    ...getTracks({ gender: "female", residency: "ksa" }),
    ...getTracks({ gender: "male", residency: "international" }),
    ...getTracks({ gender: "female", residency: "international" }),
  ]);

  const orgJsonLd = {
    "@context": "https://schema.org",
    "@type": "EducationalOrganization",
    name: SITE.nameAr,
    alternateName: SITE.nameEn,
    url: SITE.url,
    email: SITE.email,
    telephone: `+${SITE.phone}`,
    parentOrganization: { "@type": "Organization", name: SITE.parentOrgAr },
    address: {
      "@type": "PostalAddress",
      addressCountry: "SA",
      addressLocality: "Riyadh",
    },
    sameAs: [SITE.youtube],
  };

  const faqJsonLd = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: FAQ.slice(0, 8).map((f) => ({
      "@type": "Question",
      name: f.q,
      acceptedAnswer: { "@type": "Answer", text: f.a },
    })),
  };

  return (
    <>
      {/* V1 had no structured data at all (docs/00 defect #5). */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(orgJsonLd) }}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(faqJsonLd) }}
      />

      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-b from-primary-dark to-primary py-20 text-white sm:py-28">
        <div className="container-x text-center">
          <p className="mb-3 text-sm text-gold-on-dark sm:text-base">{HERO.kicker}</p>
          <h1 className="mb-6 text-4xl font-bold leading-tight sm:text-5xl lg:text-6xl">
            {HERO.title}
          </h1>
          <p className="mx-auto mb-9 max-w-3xl text-lg leading-relaxed text-white/85">
            {HERO.body}
          </p>
          <div className="flex flex-wrap justify-center gap-3">
            <Link href={`${base}/register`} className="btn btn-gold">
              {HERO.ctaPrimary}
            </Link>
            <Link
              href={`${base}/contact`}
              className="btn border-2 border-white/40 text-white hover:bg-white/10"
            >
              {HERO.ctaSecondary}
            </Link>
          </div>
          <p className="mt-8 inline-flex items-center gap-2 rounded-full bg-white/10 px-4 py-2 text-sm">
            <span aria-hidden="true">✓</span> {HERO.licence} — {SITE.parentOrgAr}
          </p>
        </div>
      </section>

      {/* Availability summary — surfaced on the homepage so the user knows
          before investing in the flow. V1 revealed this only after redirect. */}
      {all.open < all.total && (
        <div className="bg-warning/5 py-4">
          <div className="container-x text-center text-sm text-gray-700">
            {locale === "ar" ? (
              <>
                التسجيل مفتوح حاليًا في <strong>{all.open}</strong> من {all.total} مسارًا.{" "}
                <Link href={`${base}/register`} className="font-bold text-primary underline">
                  اعرض حالة كل مسار
                </Link>
              </>
            ) : (
              <>
                Registration is currently open in <strong>{all.open}</strong> of {all.total} tracks.{" "}
                <Link href={`${base}/register`} className="font-bold text-primary underline">
                  See the status of each track
                </Link>
              </>
            )}
          </div>
        </div>
      )}

      {/* Vision / Mission / Goals */}
      <Section>
        <SectionHeading title="الرؤية والرسالة والأهداف" />
        <ul className="grid gap-6 md:grid-cols-3">
          {VISION.map((v) => (
            <li key={v.title} className="card">
              <h3 className="mb-3 text-xl font-bold text-primary">{v.title}</h3>
              <p className="leading-relaxed text-gray-700">{v.body}</p>
            </li>
          ))}
        </ul>
      </Section>

      {/* Services */}
      <Section alt>
        <SectionHeading title="ماذا نقدم" />
        <ul className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {SERVICES.map((s) => (
            <li key={s.title} className="card">
              <h3 className="mb-2 text-lg font-bold text-primary">{s.title}</h3>
              <p className="text-gray-700">{s.body}</p>
            </li>
          ))}
        </ul>
      </Section>

      {/* Advantages */}
      <Section>
        <SectionHeading title="مزايا مِقْرَأَة إتقان" />
        <ul className="mx-auto grid max-w-4xl gap-3 sm:grid-cols-2">
          {ADVANTAGES.map((a) => (
            <li key={a} className="flex gap-3 rounded-xl bg-white p-4 shadow-sm">
              <span aria-hidden="true" className="font-bold text-gold-text">✓</span>
              <span className="text-gray-700">{a}</span>
            </li>
          ))}
        </ul>
      </Section>

      {/* Sections with live availability */}
      <Section alt id="sections">
        <SectionHeading title="تقسيم حلقات المقرأة" subtitle={SECTIONS_INTRO} />
        <ul className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {sections.map((s) => (
            <li key={s.token} className="card">
              <div className="mb-2 flex items-start justify-between gap-2">
                <h3 className="text-lg font-bold text-primary">{s.nameAr}</h3>
                <AvailabilityBadge status={s.status} locale={locale as Locale} />
              </div>
              <p className="mb-3 text-sm text-gray-600">
                {s.ageMin === null && s.ageMax === null
                  ? t.register.noAgeLimit
                  : s.ageMax === null
                    ? `${s.ageMin} سنة فأكثر`
                    : `من ${s.ageMin} إلى ${s.ageMax} سنة`}
              </p>
              <ul className="space-y-1.5 text-sm text-gray-700">
                {s.bulletsAr.map((b) => (
                  <li key={b} className="flex gap-2">
                    <span aria-hidden="true" className="text-gold-text">•</span>
                    <span>{b}</span>
                  </li>
                ))}
              </ul>
            </li>
          ))}
        </ul>
        <p className="mt-8 text-center text-sm text-gray-600">
          حالة التسجيل أعلاه لقسم الرجال داخل المملكة.{" "}
          <Link href={`${base}/register`} className="font-bold text-primary underline">
            اعرض جميع الأقسام وحالتها
          </Link>
        </p>
      </Section>

      {/* Partners marquee — pausable on hover/focus, clones hidden from AT */}
      <div className="marquee overflow-hidden border-y border-primary/10 bg-white py-4">
        <div className="marquee-track flex w-max gap-12 whitespace-nowrap text-sm text-gray-600">
          {[0, 1].map((dup) => (
            <div key={dup} className="flex gap-12" aria-hidden={dup === 1 ? "true" : undefined}>
              {PARTNERS.map((p) => (
                <span key={p}>{p}</span>
              ))}
            </div>
          ))}
        </div>
      </div>

      {/* FAQ preview — CTA now points at a page that exists. */}
      <Section>
        <SectionHeading title="الأسئلة الشائعة" />
        <ul className="mx-auto max-w-3xl space-y-3">
          {FAQ.slice(0, 4).map((f) => (
            <li key={f.q}>
              <details className="card group">
                <summary className="cursor-pointer list-none font-bold text-primary marker:content-none">
                  {f.q}
                </summary>
                <p className="mt-3 leading-relaxed text-gray-700">{f.a}</p>
              </details>
            </li>
          ))}
        </ul>
        <p className="mt-8 text-center">
          <Link href={`${base}/faq`} className="btn btn-outline">
            عرض كافة الأسئلة
          </Link>
        </p>
      </Section>

      {/* CTA band */}
      <section className="bg-primary py-14 text-center text-white">
        <div className="container-x">
          <h2 className="mb-5 text-2xl font-bold sm:text-3xl">ابدأ حفظ القرآن اليوم</h2>
          <Link href={`${base}/register`} className="btn btn-gold">
            سجّل الآن
          </Link>
        </div>
      </section>
    </>
  );
}
