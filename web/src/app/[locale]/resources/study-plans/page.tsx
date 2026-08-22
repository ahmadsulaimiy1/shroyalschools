import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { isLocale } from "@/lib/i18n";
import { Section, SectionHeading } from "@/components/Section";
import { STUDY_PLANS } from "@/lib/site";

export const metadata: Metadata = {
  title: "الجداول والخطط التعليمية",
  description:
    "خطط حفظ القرآن الكريم خلال 5 أو 6 أو 10 أو 14 شهرًا، مع المعدل اليومي ونقطة البداية وحجم الملف لكل خطة.",
};

export default async function StudyPlansPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();

  return (
    <Section>
      <SectionHeading
        title="الجداول والخطط التعليمية"
        subtitle="اختر الخطة التي تناسب وقتك وقدرتك على الإنجاز اليومي."
        as="h1"
      />
      <ul className="mx-auto grid max-w-4xl gap-5 sm:grid-cols-2">
        {STUDY_PLANS.map((p) => (
          <li key={p.id} className="card flex flex-col">
            <h2 className="mb-3 text-lg font-bold text-primary">{p.titleAr}</h2>
            {/* V1 detailed only one of the four plans. All four now state
                daily rate, starting point and file size (docs/06 §8). */}
            <dl className="mb-5 flex-1 space-y-1.5 text-sm text-gray-700">
              <div className="flex gap-2">
                <dt className="font-medium">المعدل اليومي:</dt>
                <dd>{p.dailyRateAr}</dd>
              </div>
              <div className="flex gap-2">
                <dt className="font-medium">نقطة البداية:</dt>
                <dd>{p.startingPointAr}</dd>
              </div>
              <div className="flex gap-2">
                <dt className="font-medium">حجم الملف:</dt>
                <dd>{p.approxSizeMB} ميجابايت تقريبًا</dd>
              </div>
            </dl>
            {/* Served over https. V1's 14-month plan linked over plain http://. */}
            <a href={p.fallback} className="btn btn-primary w-full">
              تحميل الخطة
            </a>
          </li>
        ))}
      </ul>
      <p className="mx-auto mt-8 max-w-4xl text-center text-sm text-gray-600">
        حجم الملفات كبير نسبيًا؛ يُنصح بالتحميل عبر شبكة واي فاي.
      </p>
    </Section>
  );
}
