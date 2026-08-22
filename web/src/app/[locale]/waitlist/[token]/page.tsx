import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { isLocale, type Locale } from "@/lib/i18n";
import { getDict } from "@/lib/dictionary";
import { findTrack } from "@/lib/tracks";
import { SectionHeading } from "@/components/Section";
import WaitlistForm from "@/components/WaitlistForm";

export const metadata: Metadata = {
  title: "قائمة الانتظار",
  description: "سجّل بياناتك في قائمة الانتظار وسنبلغك فور فتح التسجيل في المسار الذي اخترته.",
  robots: { index: false, follow: true },
};

/**
 * Waitlist capture.
 *
 * This page exists because of the single most damaging finding in the audit:
 * 22 of 36 V1 entry points were closed, and the waitlist they redirected to
 * captured ONLY a name and a WhatsApp number — no email — so the academy had
 * no way to contact anyone when a track reopened (docs/07 §4).
 *
 * Adding the email field is, per docs/12, the highest-ROI change on the site.
 */
export default async function WaitlistPage({
  params,
}: {
  params: Promise<{ locale: string; token: string }>;
}) {
  const { locale, token } = await params;
  if (!isLocale(locale)) notFound();
  const track = findTrack(token);
  if (!track) notFound();

  const t = getDict(locale as Locale);
  const isAr = locale === "ar";

  return (
    <div className="py-14">
      <div className="container-x max-w-2xl">
        <SectionHeading
          title={t.register.waitlistTitle}
          subtitle={t.register.waitlistIntro}
          as="h1"
        />

        <div className="card mb-8 border-warning/30 bg-warning/5">
          <p className="font-bold text-primary">
            {isAr ? track.nameAr : track.nameEn}
          </p>
          <p className="mt-1 text-sm text-gray-700">{t.common.full}</p>
        </div>

        <WaitlistForm locale={locale as Locale} token={track.token} />

        <p className="mt-8">
          <Link href={`/${locale}/register`} className="btn btn-outline">
            {t.common.back}
          </Link>
        </p>
      </div>
    </div>
  );
}
