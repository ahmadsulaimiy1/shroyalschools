import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { isLocale } from "@/lib/i18n";
import { SITE, WHATSAPP_MEN, WHATSAPP_WOMEN, HAS_SEPARATE_WHATSAPP, waLink } from "@/lib/site";
import { Section, SectionHeading } from "@/components/Section";

export const metadata: Metadata = {
  title: "تواصل معنا",
  description:
    "تواصل مع إدارة مقرأة إتقان الافتراضية عبر واتساب أو الهاتف أو البريد الإلكتروني. فريقنا جاهز لخدمتكم.",
};

/** V1 had no contact page — only an anchor on the homepage (docs/09 §5). */
export default async function ContactPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();

  return (
    <Section>
      <SectionHeading
        title="تواصل معنا"
        subtitle="يسعدنا تواصلكم معنا عبر قنواتنا الرسمية، فريقنا جاهز لخدمتكم."
        as="h1"
      />

      <div className="mx-auto grid max-w-3xl gap-5 sm:grid-cols-2">
        {/*
          ⚠ V1 rendered two cards — "واتساب (رجال)" and "واتساب (نساء)" — both
          pointing at the SAME number, defeating the gender segregation the
          institution is built on (docs/00 defect #6).
          We will not reproduce that. Until a second number is configured via
          NEXT_PUBLIC_WHATSAPP_WOMEN, one honest general channel is shown.
        */}
        {HAS_SEPARATE_WHATSAPP ? (
          <>
            <ContactCard title="واتساب (رجال)" href={waLink(WHATSAPP_MEN)} value={WHATSAPP_MEN} />
            <ContactCard title="واتساب (نساء)" href={waLink(WHATSAPP_WOMEN!)} value={WHATSAPP_WOMEN!} />
          </>
        ) : (
          <ContactCard title="واتساب" href={waLink(WHATSAPP_MEN)} value={WHATSAPP_MEN} />
        )}

        <ContactCard title="الهاتف" href={`tel:${SITE.phone}`} value={`+${SITE.phone}`} />
        <ContactCard title="البريد الإلكتروني" href={`mailto:${SITE.email}`} value={SITE.email} />
        <ContactCard title="قناة يوتيوب" href={SITE.youtube} value="@-Itqan-quran01" />
      </div>

      <p className="mx-auto mt-10 max-w-3xl rounded-xl bg-primary/5 p-5 text-center text-gray-700">
        {SITE.addressAr}
      </p>
    </Section>
  );
}

function ContactCard({ title, href, value }: { title: string; href: string; value: string }) {
  return (
    <a href={href} className="card block transition-shadow hover:shadow-md">
      <h2 className="mb-2 font-bold text-primary">{title}</h2>
      <p className="text-gray-700" dir="ltr">
        {value}
      </p>
    </a>
  );
}
