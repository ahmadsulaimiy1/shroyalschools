/**
 * Locale definitions.
 *
 * ⚠ V1 rendered the English, French and Italian pages inside
 * <html dir="rtl" lang="ar"> — LTR content in an RTL document declared as
 * Arabic. See docs/02-pages.md §2.7. Every locale here carries its own dir
 * and lang, applied at the <html> element.
 *
 * The locale set reconciles the three inconsistent sets found in the audit:
 *   V1 marketing site : ar en fr it ur
 *   V1 LMS interface  : ar en fr id so ur ru
 * See docs/09-user-flows.md §6. Locales the LMS supports but the site did not
 * (id, so, ru) are included; Italian is retained because the site had it.
 */

export const LOCALES = ["ar", "en", "fr", "ur", "id", "so", "ru", "it"] as const;
export type Locale = (typeof LOCALES)[number];
export const DEFAULT_LOCALE: Locale = "ar";

export interface LocaleMeta {
  code: Locale;
  dir: "rtl" | "ltr";
  /** BCP-47 tag for the lang attribute. */
  lang: string;
  nativeName: string;
  englishName: string;
  /** Whether full page copy exists. Others fall back to Arabic/English content. */
  hasFullContent: boolean;
}

export const LOCALE_META: Record<Locale, LocaleMeta> = {
  ar: { code: "ar", dir: "rtl", lang: "ar-SA", nativeName: "العربية", englishName: "Arabic", hasFullContent: true },
  en: { code: "en", dir: "ltr", lang: "en", nativeName: "English", englishName: "English", hasFullContent: true },
  fr: { code: "fr", dir: "ltr", lang: "fr", nativeName: "Français", englishName: "French", hasFullContent: false },
  ur: { code: "ur", dir: "rtl", lang: "ur", nativeName: "اردو", englishName: "Urdu", hasFullContent: false },
  // V1's LMS switcher misspelled this as "bahasa Indonesi" — see docs/06 §17 item 3.
  id: { code: "id", dir: "ltr", lang: "id", nativeName: "Bahasa Indonesia", englishName: "Indonesian", hasFullContent: false },
  so: { code: "so", dir: "ltr", lang: "so", nativeName: "Soomaali", englishName: "Somali", hasFullContent: false },
  ru: { code: "ru", dir: "ltr", lang: "ru", nativeName: "Русский", englishName: "Russian", hasFullContent: false },
  it: { code: "it", dir: "ltr", lang: "it", nativeName: "Italiano", englishName: "Italian", hasFullContent: false },
};

export function isLocale(v: string): v is Locale {
  return (LOCALES as readonly string[]).includes(v);
}

export function meta(locale: Locale): LocaleMeta {
  return LOCALE_META[locale];
}

/** True for locales whose speakers route to the international halaqas. */
export function isNonArabicLocale(locale: Locale): boolean {
  return locale !== "ar";
}
