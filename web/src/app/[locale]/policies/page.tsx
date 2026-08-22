import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { isLocale } from "@/lib/i18n";
import { Section, SectionHeading } from "@/components/Section";
import { TERMS } from "@/content/home";

export const metadata: Metadata = {
  title: "السياسات واللوائح",
  description:
    "شروط القبول والتسجيل في مقرأة إتقان الافتراضية: رسالة المقرأة ومنهجها، آلية التسجيل، الضوابط العامة، الالتزام والمتابعة، صحة البيانات، الدعم، والملاحظات.",
};

/** V1 published no "last updated" date on an agreement users must accept,
 *  and had no privacy policy at all despite collecting name, email, phone
 *  and age (docs/02 §2.3). Both addressed here. */
const LAST_UPDATED = "2026-08-20";
const POLICY_VERSION = "2.0";

export default async function PoliciesPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();

  return (
    <Section>
      <SectionHeading title="اللوائح والسياسات" as="h1" />

      <div className="mx-auto max-w-3xl">
        <p className="mb-8 rounded-xl bg-primary/5 p-4 text-sm text-gray-700">
          آخر تحديث: {LAST_UPDATED} · الإصدار {POLICY_VERSION}
        </p>

        <h2 className="mb-6 text-2xl font-bold text-primary">
          شروط القبول والتسجيل (اتفاقية التسجيل)
        </h2>
        <p className="mb-8 rounded-xl border-2 border-gold/30 bg-gold/5 p-4 leading-relaxed text-gray-800">
          الضغط على زر (التسجيل الآن) يُعد إقرارًا بالاطلاع والموافقة على جميع شروط القبول
          والتسجيل.
        </p>

        <div className="space-y-8">
          {TERMS.map((clause) => (
            <section key={clause.title}>
              <h3 className="mb-3 text-lg font-bold text-primary">{clause.title}</h3>
              {clause.body && (
                <p className="mb-3 leading-relaxed text-gray-700">{clause.body}</p>
              )}
              {clause.items.length > 0 && (
                <ul className="space-y-2 ps-5">
                  {clause.items.map((i) => (
                    <li key={i} className="list-disc leading-relaxed text-gray-700">
                      {i}
                    </li>
                  ))}
                </ul>
              )}
              {"note" in clause && clause.note && (
                <p className="mt-3 leading-relaxed text-gray-600">{clause.note}</p>
              )}
            </section>
          ))}
        </div>

        <hr className="my-12 border-primary/10" />

        <section id="privacy">
          <h2 className="mb-4 text-2xl font-bold text-primary">الخصوصية وحماية البيانات</h2>
          <div className="space-y-4 leading-relaxed text-gray-700">
            <p>
              تلتزم المقرأة بحماية البيانات الشخصية وفق نظام حماية البيانات الشخصية في
              المملكة العربية السعودية.
            </p>
            <h3 className="text-lg font-bold text-primary">البيانات التي نجمعها</h3>
            <ul className="space-y-2 ps-5">
              <li className="list-disc">الاسم والبريد الإلكتروني ورقم الجوال.</li>
              <li className="list-disc">العمر والدولة ولغة الدراسة.</li>
              <li className="list-disc">بيانات الحضور والتسميع والتقدم في الحفظ.</li>
            </ul>
            <h3 className="text-lg font-bold text-primary">بيانات القاصرين</h3>
            <p>
              تسجيل من هم دون 18 عامًا يتطلب موافقة ولي الأمر. ويقتصر التواصل بشأن الطالب
              القاصر على ولي أمره، ويُوثَّق كل تواصل داخل المنصة.
            </p>
            <h3 className="text-lg font-bold text-primary">حقوقك</h3>
            <p>
              لك الحق في الاطلاع على بياناتك وتصحيحها وطلب حذفها، وسحب الموافقة في أي وقت،
              عبر التواصل مع إدارة المقرأة.
            </p>
            <p className="rounded-xl bg-warning/5 p-4 text-sm">
              هذه الصفحة مسودة تحتاج مراجعة قانونية مختصة قبل النشر النهائي.
            </p>
          </div>
        </section>
      </div>
    </Section>
  );
}
