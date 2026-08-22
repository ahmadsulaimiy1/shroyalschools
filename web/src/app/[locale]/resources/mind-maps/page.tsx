import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { isLocale } from "@/lib/i18n";
import { Section, SectionHeading } from "@/components/Section";
import { MIND_MAPS, driveDownload, drivePreview } from "@/lib/site";

export const metadata: Metadata = {
  // ⚠ V1 misspelled القرآن as القرأن here — in the title, nav, H1, footer AND
  // the URL slug (docs/06 §17 item 1). Corrected throughout.
  title: "الخرائط الذهنية لتحفيظ القرآن الكريم",
  description:
    "حمّل الخرائط الذهنية المجانية لتحفيظ القرآن الكريم: جزء عم، جزء تبارك، جزء قد سمع، جزء الذاريات، الجزء الأول والثاني، وملف شامل.",
};

export default async function MindMapsPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();

  return (
    <Section>
      <SectionHeading
        title="الخرائط الذهنية لتحفيظ القرآن الكريم"
        subtitle="ملفات مجانية تساعد على تثبيت الحفظ بالربط البصري."
        as="h1"
      />
      <ul className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {MIND_MAPS.map((m) => (
          <li key={m.id} className="card flex flex-col">
            <h2 className="mb-2 text-lg font-bold text-primary">{m.titleAr}</h2>
            <p className="mb-5 flex-1 text-sm text-gray-600">ملف PDF</p>
            <div className="flex gap-2">
              {/* Direct download rather than V1's Drive /view preview page,
                  which added a click and a possible Google sign-in wall. */}
              <a href={driveDownload(m.driveId)} className="btn btn-primary flex-1 text-sm">
                تحميل
              </a>
              <a href={drivePreview(m.driveId)} className="btn btn-outline text-sm">
                معاينة
              </a>
            </div>
          </li>
        ))}
      </ul>
    </Section>
  );
}
