import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { isLocale } from "@/lib/i18n";
import { Section, SectionHeading } from "@/components/Section";

export const metadata: Metadata = {
  title: "المصادر والمعرفة",
  description:
    "مصادر مقرأة إتقان: الخرائط الذهنية لتحفيظ القرآن الكريم، والجداول والخطط التعليمية للحفظ خلال 5 و6 و10 و14 شهرًا.",
};

/**
 * ⚠ Fixes a V1 defect: "المصادر والمعرفة" was a top-level nav item with
 * href="#" on all 14 pages — a dead link in the primary navigation
 * (docs/01 §3). This is the hub it should have pointed at.
 */
export default async function ResourcesPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();
  const base = `/${locale}/resources`;

  const items = [
    {
      href: `${base}/mind-maps`,
      title: "الخرائط الذهنية لتحفيظ القرآن الكريم",
      body: "سبعة ملفات تساعد على تثبيت الحفظ بالربط البصري — جزء عم، تبارك، قد سمع، الذاريات، الجزء الأول والثاني، وملف شامل.",
    },
    {
      href: `${base}/study-plans`,
      title: "الجداول والخطط التعليمية",
      body: "أربع خطط لحفظ القرآن الكريم خلال 5 أو 6 أو 10 أو 14 شهرًا، مع بيان المعدل اليومي ونقطة البداية لكل خطة.",
    },
  ];

  return (
    <Section>
      <SectionHeading
        title="المصادر والمعرفة"
        subtitle="مواد تعليمية مجانية تدعم رحلتك مع كتاب الله."
        as="h1"
      />
      <ul className="mx-auto grid max-w-4xl gap-6 sm:grid-cols-2">
        {items.map((i) => (
          <li key={i.href}>
            <Link href={i.href} className="card block h-full transition-shadow hover:shadow-md">
              <h2 className="mb-2 text-xl font-bold text-primary">{i.title}</h2>
              <p className="leading-relaxed text-gray-700">{i.body}</p>
            </Link>
          </li>
        ))}
      </ul>
    </Section>
  );
}
