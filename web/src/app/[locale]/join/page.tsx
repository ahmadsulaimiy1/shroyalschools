import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { isLocale } from "@/lib/i18n";
import { STAFF_FORMS } from "@/lib/site";
import { Section, SectionHeading } from "@/components/Section";

export const metadata: Metadata = {
  title: "انضم لفريقنا",
  description:
    "فرص الانضمام لمقرأة إتقان الافتراضية كمعلم أو معلمة أو مشرف أو مشرفة لتعليم القرآن الكريم عن بُعد.",
};

/**
 * Staff recruitment hub.
 *
 * V1 scattered four Google Forms across a header dropdown and the footer,
 * two of them on the retired goo.gl shortener (docs/07 §6). This gathers them
 * behind one route so they can later be swapped for in-platform forms — which
 * terms clause 2 arguably already requires — without changing any navigation.
 */
export default async function JoinPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();

  const roles = [
    { title: "تسجيل المعلمين", href: STAFF_FORMS.teachersMen },
    { title: "تسجيل المعلمات", href: STAFF_FORMS.teachersWomen },
    { title: "تسجيل المشرفين", href: STAFF_FORMS.supervisorsMen },
    { title: "تسجيل المشرفات", href: STAFF_FORMS.supervisorsWomen },
  ];

  return (
    <Section>
      <SectionHeading
        title="انضم لفريقنا"
        subtitle="نبحث عن معلمين ومعلمات ومشرفين ومشرفات مؤهّلين ومجازين لتعليم كتاب الله عن بُعد."
        as="h1"
      />
      <ul className="mx-auto grid max-w-3xl gap-5 sm:grid-cols-2">
        {roles.map((r) => (
          <li key={r.title} className="card flex flex-col">
            <h2 className="mb-4 flex-1 text-lg font-bold text-primary">{r.title}</h2>
            <a href={r.href} className="btn btn-primary w-full" rel="noopener">
              تعبئة النموذج
            </a>
          </li>
        ))}
      </ul>
      <p className="mx-auto mt-8 max-w-3xl text-center text-sm text-gray-600">
        يُشترط لتقديم طلب التدريس إتقان التلاوة وأحكام التجويد، ويُفضَّل وجود إجازة بسند متصل.
      </p>
    </Section>
  );
}
