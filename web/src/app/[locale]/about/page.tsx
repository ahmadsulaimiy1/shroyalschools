import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { isLocale } from "@/lib/i18n";
import { SITE } from "@/lib/site";
import { Section, SectionHeading } from "@/components/Section";
import { VISION, ADVANTAGES } from "@/content/home";

export const metadata: Metadata = {
  title: "عن المنصة",
  description:
    "مقرأة إتقان الافتراضية منصة قرآنية إلكترونية تحت مظلة جمعية مكنون لتحفيظ القرآن الكريم، تُعنى بتعليم كتاب الله تلاوةً وحفظًا بإشراف معلمين ومعلمات مؤهّلين ومجازين.",
};

export default async function AboutPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();

  return (
    <>
      <Section>
        <SectionHeading title="عن المنصة" as="h1" />
        <div className="mx-auto max-w-3xl space-y-5 text-lg leading-relaxed text-gray-700">
          <p>
            <strong className="text-primary">{SITE.nameAr}</strong> منصة قرآنية إلكترونية
            تُعنى بتعليم كتاب الله تعالى تلاوةً وحفظًا، وفق منهجية علمية رصينة، وبإشراف نخبة
            من المعلمين والمعلمات المؤهّلين، وتحت مظلة {SITE.parentOrgAr}.
          </p>
          <p className="rounded-xl bg-primary/5 p-5 text-base">
            تحت إشراف رسمي من {SITE.parentOrgAr}، وبالشراكة مع {SITE.partnerAr}.
          </p>
        </div>
      </Section>

      <Section alt>
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

      <Section>
        <SectionHeading title="لماذا مِقْرَأَة إتقان؟" />
        <ul className="mx-auto grid max-w-4xl gap-3 sm:grid-cols-2">
          {ADVANTAGES.map((a) => (
            <li key={a} className="flex gap-3 rounded-xl bg-white p-4 shadow-sm">
              <span aria-hidden="true" className="font-bold text-gold-text">✓</span>
              <span className="text-gray-700">{a}</span>
            </li>
          ))}
        </ul>
      </Section>
    </>
  );
}
