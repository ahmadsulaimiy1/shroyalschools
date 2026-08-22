/**
 * Country list for the registration router.
 *
 * V1 asked for a full phone number purely to read its country code, then threw
 * the number away (docs/03 §1). That is the highest-friction step in the funnel
 * in exchange for information a country select provides directly — and it
 * collects personal data with no purpose, which cuts against PDPL data
 * minimisation (docs/13 §5). This replaces it.
 *
 * `arab` drives residency routing exactly as V1's arabCountries list did, so the
 * existing routing behaviour is preserved.
 */
export interface Country {
  code: string;
  nameAr: string;
  nameEn: string;
  arab: boolean;
}

export const COUNTRIES: Country[] = [
  { code: "SA", nameAr: "السعودية", nameEn: "Saudi Arabia", arab: true },
  { code: "EG", nameAr: "مصر", nameEn: "Egypt", arab: true },
  { code: "AE", nameAr: "الإمارات", nameEn: "United Arab Emirates", arab: true },
  { code: "KW", nameAr: "الكويت", nameEn: "Kuwait", arab: true },
  { code: "QA", nameAr: "قطر", nameEn: "Qatar", arab: true },
  { code: "BH", nameAr: "البحرين", nameEn: "Bahrain", arab: true },
  { code: "OM", nameAr: "عُمان", nameEn: "Oman", arab: true },
  { code: "YE", nameAr: "اليمن", nameEn: "Yemen", arab: true },
  { code: "JO", nameAr: "الأردن", nameEn: "Jordan", arab: true },
  { code: "LB", nameAr: "لبنان", nameEn: "Lebanon", arab: true },
  { code: "PS", nameAr: "فلسطين", nameEn: "Palestine", arab: true },
  { code: "SY", nameAr: "سوريا", nameEn: "Syria", arab: true },
  { code: "IQ", nameAr: "العراق", nameEn: "Iraq", arab: true },
  { code: "SD", nameAr: "السودان", nameEn: "Sudan", arab: true },
  { code: "LY", nameAr: "ليبيا", nameEn: "Libya", arab: true },
  { code: "TN", nameAr: "تونس", nameEn: "Tunisia", arab: true },
  { code: "DZ", nameAr: "الجزائر", nameEn: "Algeria", arab: true },
  { code: "MA", nameAr: "المغرب", nameEn: "Morocco", arab: true },
  { code: "MR", nameAr: "موريتانيا", nameEn: "Mauritania", arab: true },
  { code: "SO", nameAr: "الصومال", nameEn: "Somalia", arab: true },
  { code: "DJ", nameAr: "جيبوتي", nameEn: "Djibouti", arab: true },
  { code: "KM", nameAr: "جزر القمر", nameEn: "Comoros", arab: true },
  { code: "GB", nameAr: "المملكة المتحدة", nameEn: "United Kingdom", arab: false },
  { code: "US", nameAr: "الولايات المتحدة", nameEn: "United States", arab: false },
  { code: "CA", nameAr: "كندا", nameEn: "Canada", arab: false },
  { code: "AU", nameAr: "أستراليا", nameEn: "Australia", arab: false },
  { code: "FR", nameAr: "فرنسا", nameEn: "France", arab: false },
  { code: "BE", nameAr: "بلجيكا", nameEn: "Belgium", arab: false },
  { code: "DE", nameAr: "ألمانيا", nameEn: "Germany", arab: false },
  { code: "NL", nameAr: "هولندا", nameEn: "Netherlands", arab: false },
  { code: "IT", nameAr: "إيطاليا", nameEn: "Italy", arab: false },
  { code: "ES", nameAr: "إسبانيا", nameEn: "Spain", arab: false },
  { code: "TR", nameAr: "تركيا", nameEn: "Türkiye", arab: false },
  { code: "RU", nameAr: "روسيا", nameEn: "Russia", arab: false },
  { code: "PK", nameAr: "باكستان", nameEn: "Pakistan", arab: false },
  { code: "IN", nameAr: "الهند", nameEn: "India", arab: false },
  { code: "BD", nameAr: "بنغلاديش", nameEn: "Bangladesh", arab: false },
  { code: "ID", nameAr: "إندونيسيا", nameEn: "Indonesia", arab: false },
  { code: "MY", nameAr: "ماليزيا", nameEn: "Malaysia", arab: false },
  { code: "NG", nameAr: "نيجيريا", nameEn: "Nigeria", arab: false },
  { code: "ZA", nameAr: "جنوب أفريقيا", nameEn: "South Africa", arab: false },
  { code: "KE", nameAr: "كينيا", nameEn: "Kenya", arab: false },
  { code: "SN", nameAr: "السنغال", nameEn: "Senegal", arab: false },
  { code: "OTHER", nameAr: "دولة أخرى", nameEn: "Other country", arab: false },
];

export function findCountry(code: string): Country | undefined {
  return COUNTRIES.find((c) => c.code === code);
}

/** Residency drives which track set applies — same rule V1 used. */
export function residencyFor(code: string): "ksa" | "international" {
  return code === "SA" ? "ksa" : "international";
}
