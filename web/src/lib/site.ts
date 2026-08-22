/**
 * Site-wide constants and contact details.
 * Copy is verbatim from the V1 site except where a docs/06 §17 defect is fixed.
 */

export const SITE = {
  nameAr: "مِقْرَأَة إِتْقَان الِافْتِرَاضِيَّةُ",
  nameEn: "Itqan Virtual Quran Academy",
  /** Standardised spelling. V1 used three variants across site and LMS. */
  shortAr: "مقرأة إتقان",
  parentOrgAr: "جمعية مكنون لتحفيظ القرآن الكريم",
  parentOrgEn: "Maknoon Association for Quran Memorisation",
  partnerAr: "جمعية إقرأ بالخرمة",
  url: "https://itqan-quran.com",
  email: "info@itqan-quran.com",
  phone: "966539065696",
  addressAr: "المملكة العربية السعودية، الرياض",
  addressEn: "Riyadh, Kingdom of Saudi Arabia",
  youtube: "https://youtube.com/@-Itqan-quran01",
  lmsUrl: "https://register.itqan-quran.com",
  lmsLogin: "https://register.itqan-quran.com/Account/Login",
} as const;

/**
 * Support channels.
 *
 * ⚠ V1 pointed BOTH the men's and women's WhatsApp buttons at the same number
 * (966539065696), defeating the gender segregation the institution is built on.
 * See docs/00 defect #6.
 *
 * We cannot invent a second number. These are intentionally driven by env vars
 * so the academy can set the correct women's line without a code change; until
 * NEXT_PUBLIC_WHATSAPP_WOMEN is set, the UI shows ONE general channel rather
 * than mislabelling a single number as two gendered ones.
 */
export const WHATSAPP_MEN = process.env.NEXT_PUBLIC_WHATSAPP_MEN ?? SITE.phone;
export const WHATSAPP_WOMEN = process.env.NEXT_PUBLIC_WHATSAPP_WOMEN ?? null;
export const HAS_SEPARATE_WHATSAPP = WHATSAPP_WOMEN !== null;

export function waLink(number: string) {
  return `https://wa.me/${number}`;
}

/**
 * Staff recruitment.
 * V1 used four Google Forms — two on the retired goo.gl shortener, and all
 * outside the platform, contradicting terms clause 2. See docs/07 §6.
 * Retained here as the current destination, but surfaced through one /join
 * hub so they can be swapped for in-platform forms without touching the UI.
 */
export const STAFF_FORMS = {
  teachersMen: "https://goo.gl/forms/FO4dBRij0buhezgF3",
  teachersWomen: "https://goo.gl/forms/artmNJBAb9yE9OJ42",
  supervisorsMen:
    "https://docs.google.com/forms/d/e/1FAIpQLSeNrT2BJ2M3WDlUK_AzRwbgewlmeTDp-m1Po71Bn0V1FYKahw/viewform",
  supervisorsWomen: "https://forms.gle/xUm7QUnc37q1HpHD7",
} as const;

/**
 * Study plans.
 * ⚠ V1 served these from quranlives.com — a third-party domain — at ~10 MB each,
 * one over plain http://. See docs/05 §2. Paths below are relative so the files
 * can be self-hosted; `fallback` preserves the current source until they are.
 */
export interface StudyPlan {
  id: string;
  titleAr: string;
  titleEn: string;
  months: number;
  dailyRateAr: string;
  startingPointAr: string;
  approxSizeMB: number;
  href: string;
  fallback: string;
}

export const STUDY_PLANS: StudyPlan[] = [
  {
    id: "5-months",
    titleAr: "خطة حفظ القرآن الكريم خلال 5 أشهُر",
    titleEn: "Memorise the Quran in 5 months",
    months: 5,
    dailyRateAr: "خمسة أوجه يوميًا",
    startingPointAr: "بداية من سورة البقرة",
    approxSizeMB: 9.9,
    href: "/downloads/plan-5-months.pdf",
    fallback:
      "https://quranlives.com/wp-content/uploads/2024/03/%D8%AE%D9%85%D8%B3%D8%A9-%D8%A3%D9%88%D8%AC%D9%87-%D9%85%D9%86-%D8%A7%D9%84%D8%A8%D9%82%D8%B1%D8%A9-5-%D8%A3%D8%B4%D9%87%D8%B1.pdf",
  },
  {
    id: "6-months",
    titleAr: "خطة حفظ القرآن الكريم خلال 6 أشهُر",
    titleEn: "Memorise the Quran in 6 months",
    months: 6,
    dailyRateAr: "ثلاثة أوجه وربع يوميًا",
    startingPointAr: "بداية من سورة الناس",
    approxSizeMB: 10.0,
    href: "/downloads/plan-6-months.pdf",
    fallback:
      "https://quranlives.com/wp-content/uploads/2024/03/%D8%AB%D9%84%D8%A7%D8%AB%D8%A9-%D8%A3%D9%88%D8%AC%D9%87-%D9%88%D8%B1%D8%A8%D8%B9-%D9%85%D9%86-%D8%A7%D9%84%D9%86%D8%A7%D8%B3-6-%D8%A3%D8%B4%D9%87%D8%B1.pdf",
  },
  {
    id: "10-months",
    titleAr: "خطة حفظ القرآن الكريم خلال 10 أشهُر",
    titleEn: "Memorise the Quran in 10 months",
    months: 10,
    dailyRateAr: "وجهان يوميًا",
    startingPointAr: "بداية من سورة الناس",
    approxSizeMB: 10.2,
    href: "/downloads/plan-10-months.pdf",
    fallback:
      "https://quranlives.com/wp-content/uploads/2024/03/%D9%88%D8%AC%D9%87%D8%A7%D9%86-%D9%85%D9%86-%D8%A7%D9%84%D9%86%D8%A7%D8%B3-_-10-%D8%A3%D8%B4%D9%87%D8%B1.pdf",
  },
  {
    id: "14-months",
    titleAr: "خطة حفظ القرآن الكريم خلال 14 شهرًا",
    titleEn: "Memorise the Quran in 14 months",
    months: 14,
    dailyRateAr: "وجه ونصف يوميًا",
    startingPointAr: "بداية من سورة الناس",
    approxSizeMB: 10.4,
    // ⚠ V1 served this one over plain http:// — upgraded to https here.
    href: "/downloads/plan-14-months.pdf",
    fallback:
      "https://quranlives.com/wp-content/uploads/2024/03/%D9%88%D8%AC%D9%87-%D9%88%D9%86%D8%B5%D9%81-%D9%8A%D9%88%D9%85%D9%8A%D8%A7-_-14-%D8%B4%D9%87%D8%B1%D8%A7.pdf",
  },
];

/** Mind maps. V1 used Google Drive /view links — see docs/05 §3. */
export interface MindMap {
  id: string;
  titleAr: string;
  titleEn: string;
  driveId: string;
}

export const MIND_MAPS: MindMap[] = [
  { id: "juz-30", titleAr: "جزء عم", titleEn: "Juz' Amma", driveId: "1YQ7KGkAfoCpoh4iyvbM517WqTbCap9Nr" },
  { id: "juz-29", titleAr: "جزء تبارك", titleEn: "Juz' Tabarak", driveId: "1RX82zZlw-0N2IaJFYiGllbRqrhGDua8_" },
  { id: "juz-28", titleAr: "جزء قد سمع", titleEn: "Juz' Qad Sami'a", driveId: "1x6EGatntygV_nVBzkDndQtBm4alMJsI9" },
  { id: "juz-27", titleAr: "جزء الذاريات", titleEn: "Juz' Adh-Dhariyat", driveId: "1SS1hiDMigiTjlrcMdrmwiLG1xJ0lGNnk" },
  { id: "juz-1", titleAr: "الجزء الأول", titleEn: "Juz' 1", driveId: "1FQJOymTyZPwdsFkSAg1zwBqmecz_9y3E" },
  { id: "juz-2", titleAr: "الجزء الثاني", titleEn: "Juz' 2", driveId: "1I00pIibr2RpwKEX8I-LJufGqX3uGL074" },
  { id: "complete", titleAr: "ملف شامل", titleEn: "Complete file", driveId: "10hqQTtn3nGyu9qS3Q9w300Q7-P95vyJT" },
];

export function drivePreview(id: string) {
  return `https://drive.google.com/file/d/${id}/view`;
}
/** Direct download rather than V1's /view preview page. */
export function driveDownload(id: string) {
  return `https://drive.google.com/uc?export=download&id=${id}`;
}
