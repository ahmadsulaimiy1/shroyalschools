import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { isLocale } from "@/lib/i18n";
import { Section, SectionHeading } from "@/components/Section";
import { FAQ } from "@/content/home";

export const metadata: Metadata = {
  title: "الأسئلة الشائعة",
  description:
    "إجابات عن أكثر الأسئلة تكرارًا حول الدراسة في مقرأة إتقان الافتراضية: آلية الدراسة، التكلفة، المتطلبات التقنية، الشهادات، تسجيل الأطفال، وحالة التسجيل في المسارات.",
};

/**
 * ⚠ This page fixes a live V1 defect: the homepage CTA "عرض كافة الأسئلة"
 * pointed at /الأسئلة-الشائعة/ which returned HTTP 404 (docs/01 §3).
 * V1 also exposed only 4 questions, none answering cost, schedule, technical
 * requirements or certification — the questions prospects actually ask.
 */
export default async function FaqPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: FAQ.map((f) => ({
      "@type": "Question",
      name: f.q,
      acceptedAnswer: { "@type": "Answer", text: f.a },
    })),
  };

  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
      <Section>
        <SectionHeading title="الأسئلة الشائعة" as="h1" />
        <ul className="mx-auto max-w-3xl space-y-3">
          {FAQ.map((f) => (
            <li key={f.q}>
              <details className="card">
                <summary className="cursor-pointer list-none font-bold text-primary marker:content-none">
                  {f.q}
                </summary>
                <p className="mt-3 leading-relaxed text-gray-700">{f.a}</p>
              </details>
            </li>
          ))}
        </ul>
      </Section>
    </>
  );
}
