import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { isLocale, type Locale } from "@/lib/i18n";
import { getDict } from "@/lib/dictionary";
import { COUNTRIES, findCountry, residencyFor } from "@/lib/countries";
import { getTracks, registrationUrl, summarise, type Gender } from "@/lib/tracks";
import AvailabilityBadge from "@/components/AvailabilityBadge";
import { SectionHeading } from "@/components/Section";

export const metadata: Metadata = {
  title: "التسجيل",
  description:
    "سجّل في مقرأة إتقان الافتراضية. اختر القسم والدولة ولغة الدراسة لعرض المسارات المتاحة وحالة التسجيل في كل مسار.",
};

/**
 * The registration router — rebuilt.
 *
 * V1's version was a client-side wizard: <form onsubmit="return false;"> driving
 * three modals, with window.location.href as the only outcome. With JS disabled
 * or failed, the site had no registration path at all (docs/03 §1).
 *
 * This version is entirely server-rendered. Each step is a plain GET form whose
 * state lives in the URL, so:
 *   - it works with JavaScript disabled
 *   - every step is linkable, shareable and back-button-safe
 *   - no personal data is collected to make a routing decision
 *
 * The step-3 change that matters most: availability is shown BEFORE the user
 * leaves the site. V1 sent 61% of journeys to a closed track discovered only
 * after redirect (docs/08 §4.6).
 */
export default async function RegisterPage({
  params,
  searchParams,
}: {
  params: Promise<{ locale: string }>;
  searchParams: Promise<Record<string, string | string[] | undefined>>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();
  const sp = await searchParams;
  const t = getDict(locale as Locale);
  const base = `/${locale}/register`;

  const str = (k: string) => (typeof sp[k] === "string" ? (sp[k] as string) : undefined);
  const who = str("who");
  const gender = str("gender") as Gender | undefined;
  const country = str("country");
  const speaksArabic = str("arabic");

  const step = !who || !gender ? 1 : !country ? 2 : 3;

  return (
    <div className="py-14">
      <div className="container-x max-w-4xl">
        <SectionHeading title={t.register.title} as="h1" />

        {/* Progress. V1 gave no indication of position and no way back. */}
        <ol className="mb-10 flex items-center justify-center gap-2 text-sm" aria-label={t.common.step}>
          {[1, 2, 3].map((n) => (
            <li key={n} className="flex items-center gap-2">
              <span
                aria-current={step === n ? "step" : undefined}
                className={`grid h-9 w-9 place-items-center rounded-full font-bold ${
                  step >= n ? "bg-primary text-white" : "bg-primary/10 text-primary/60"
                }`}
              >
                {n}
              </span>
              {n < 3 && <span aria-hidden="true" className="h-px w-8 bg-primary/20" />}
            </li>
          ))}
        </ol>

        {step === 1 && <StepOne base={base} t={t} />}
        {step === 2 && <StepTwo base={base} t={t} locale={locale as Locale} who={who!} gender={gender!} />}
        {step === 3 && (
          <StepThree
            base={base}
            t={t}
            locale={locale as Locale}
            who={who!}
            gender={gender!}
            country={country!}
            speaksArabic={speaksArabic}
          />
        )}
      </div>
    </div>
  );
}

/* ---------------------------------------------------------------- Step 1 */

function StepOne({ base, t }: { base: string; t: ReturnType<typeof getDict> }) {
  return (
    <form method="get" action={base} className="space-y-8">
      <fieldset>
        <legend className="mb-4 text-lg font-bold text-primary">{t.register.chooseWho}</legend>
        <div className="grid gap-3 sm:grid-cols-2">
          {[
            { v: "self", label: t.register.forMyself },
            { v: "child", label: t.register.forMyChild },
          ].map((o) => (
            <label key={o.v} className="card flex cursor-pointer items-center gap-3 hover:border-primary/30">
              <input type="radio" name="who" value={o.v} required defaultChecked={o.v === "self"} className="h-5 w-5 accent-[var(--color-primary)]" />
              <span className="font-medium">{o.label}</span>
            </label>
          ))}
        </div>
        {/* V1 had no guardian concept at all despite enrolling from age 3. */}
        <p className="mt-3 text-sm text-gray-600">{t.register.guardianNote}</p>
      </fieldset>

      <fieldset>
        <legend className="mb-4 text-lg font-bold text-primary">{t.register.chooseGender}</legend>
        <div className="grid gap-3 sm:grid-cols-2">
          {[
            { v: "male", label: t.common.men },
            { v: "female", label: t.common.women },
          ].map((o) => (
            <label key={o.v} className="card flex cursor-pointer items-center gap-3 hover:border-primary/30">
              <input type="radio" name="gender" value={o.v} required className="h-5 w-5 accent-[var(--color-primary)]" />
              <span className="font-medium">{o.label}</span>
            </label>
          ))}
        </div>
      </fieldset>

      <button type="submit" className="btn btn-primary w-full sm:w-auto">
        {t.common.next}
      </button>
    </form>
  );
}

/* ---------------------------------------------------------------- Step 2 */

function StepTwo({
  base, t, locale, who, gender,
}: {
  base: string; t: ReturnType<typeof getDict>; locale: Locale; who: string; gender: Gender;
}) {
  const isAr = locale === "ar";
  return (
    <form method="get" action={base} className="space-y-8">
      <input type="hidden" name="who" value={who} />
      <input type="hidden" name="gender" value={gender} />

      <div>
        <h2 className="mb-4 text-lg font-bold text-primary">{t.register.whereAndLanguage}</h2>

        <div className="space-y-5">
          <div>
            {/* Every field labelled. V1 shipped three required fields with no
                <label> at all and "*" as the only error message (docs/07 §3). */}
            <label htmlFor="country" className="mb-2 block font-medium">
              {t.register.country} <span aria-hidden="true" className="text-danger">*</span>
              <span className="sr-only">({t.common.required})</span>
            </label>
            <select
              id="country"
              name="country"
              required
              defaultValue=""
              className="w-full rounded-xl border-2 border-primary/20 bg-white px-4 py-3 focus-visible:border-primary"
            >
              <option value="" disabled>
                — {t.register.country} —
              </option>
              {COUNTRIES.map((c) => (
                <option key={c.code} value={c.code}>
                  {isAr ? c.nameAr : c.nameEn}
                </option>
              ))}
            </select>
          </div>

          {/* Language is asked directly rather than guessed from country.
              V1 inferred language from dialling code, so a Pakistani in Germany
              got the wrong route and "in" → Urdu ignored ~20 Indian languages
              (docs/03 §1). */}
          <fieldset>
            <legend className="mb-2 font-medium">{t.register.language}</legend>
            <div className="grid gap-3 sm:grid-cols-2">
              <label className="card flex cursor-pointer items-center gap-3 hover:border-primary/30">
                <input type="radio" name="arabic" value="yes" defaultChecked className="h-5 w-5 accent-[var(--color-primary)]" />
                <span className="font-medium">العربية</span>
              </label>
              <label className="card flex cursor-pointer items-center gap-3 hover:border-primary/30">
                <input type="radio" name="arabic" value="no" className="h-5 w-5 accent-[var(--color-primary)]" />
                <span className="font-medium">
                  {isAr ? "لغة أخرى" : "Another language"}
                </span>
              </label>
            </div>
          </fieldset>
        </div>
      </div>

      <div className="flex flex-wrap gap-3">
        <button type="submit" className="btn btn-primary">{t.common.next}</button>
        <Link href={base} className="btn btn-outline">{t.common.back}</Link>
      </div>
    </form>
  );
}

/* ---------------------------------------------------------------- Step 3 */

function StepThree({
  base, t, locale, who, gender, country, speaksArabic,
}: {
  base: string; t: ReturnType<typeof getDict>; locale: Locale;
  who: string; gender: Gender; country: string; speaksArabic?: string;
}) {
  const isAr = locale === "ar";
  const nonArabic = speaksArabic === "no";
  const residency = residencyFor(country);
  const c = findCountry(country);

  const tracks = getTracks({
    gender,
    residency,
    nonArabicSpeaker: nonArabic,
  });
  const { open, closed } = summarise(tracks);

  const backHref = `${base}?who=${who}&gender=${gender}`;

  return (
    <div className="space-y-8">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h2 className="text-lg font-bold text-primary">{t.register.chooseTrack}</h2>
        <p className="text-sm text-gray-600">
          {c ? (isAr ? c.nameAr : c.nameEn) : country} ·{" "}
          {gender === "male" ? t.common.men : t.common.women}
        </p>
      </div>

      {/* The honesty banner. This is the fix for the defect that made 61% of
          V1 journeys dead-end without warning. */}
      {open === 0 && (
        <div role="status" className="rounded-2xl border-2 border-warning/30 bg-warning/5 p-5">
          <p className="font-bold text-warning">{t.common.full}</p>
          <p className="mt-2 leading-relaxed text-gray-700">{t.register.allFull}</p>
        </div>
      )}
      {open > 0 && closed > 0 && (
        <div role="status" className="rounded-2xl border border-primary/20 bg-primary/5 p-4 text-sm text-gray-700">
          {t.register.someFull}
        </div>
      )}

      <ul className="grid gap-4 sm:grid-cols-2">
        {tracks.map((track) => {
          const isOpen = track.status === "open";
          const age =
            track.ageMin === null && track.ageMax === null
              ? t.register.noAgeLimit
              : track.ageMax === null
                ? `${track.ageMin}+`
                : `${track.ageMin} – ${track.ageMax}`;

          return (
            <li key={track.token} className="card flex flex-col">
              <div className="mb-3 flex items-start justify-between gap-3">
                <h3 className="text-lg font-bold text-primary">
                  {isAr ? track.nameAr : track.nameEn}
                </h3>
                <AvailabilityBadge status={track.status} locale={locale} />
              </div>

              <p className="mb-3 text-sm text-gray-600">
                <span className="font-medium">{t.register.ageBand}:</span> {age}
              </p>

              <ul className="mb-5 flex-1 space-y-1.5 text-sm text-gray-700">
                {(isAr ? track.bulletsAr : track.bulletsEn).map((b) => (
                  <li key={b} className="flex gap-2">
                    <span aria-hidden="true" className="text-gold-text">•</span>
                    <span>{b}</span>
                  </li>
                ))}
              </ul>

              {isOpen ? (
                <a href={registrationUrl(track)} className="btn btn-primary w-full">
                  {t.common.registerNow}
                </a>
              ) : (
                /* Closed tracks offer the waitlist inline rather than sending
                   the user to a dead end and discovering it after redirect. */
                <Link
                  href={`/${locale}/waitlist/${track.token}`}
                  className="btn btn-outline w-full"
                >
                  {t.common.notifyMe}
                </Link>
              )}
            </li>
          );
        })}
      </ul>

      <div className="flex flex-wrap gap-3">
        <Link href={backHref} className="btn btn-outline">{t.common.back}</Link>
        <Link href={`/${locale}/policies`} className="btn btn-outline">
          {t.common.viewTerms}
        </Link>
      </div>
    </div>
  );
}
