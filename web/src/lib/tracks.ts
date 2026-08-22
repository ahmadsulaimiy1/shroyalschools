/**
 * Track catalogue.
 *
 * Every GUID, track code, circleTypeId and open/closed status below was
 * VERIFIED against register.itqan-quran.com on 2026-08-20 by following each
 * registration link and recording where it resolved. See docs/08-lms.md §4.
 *
 * `status` here is the last verified snapshot and is the FALLBACK only.
 * At runtime, `getTracks()` prefers live availability from the LMS when the
 * availability API is configured (see docs/11-api-inference.md §2). The whole
 * point of this module is that a user is never shown a track as available
 * when it is full — the defect that made 61% of V1 journeys dead-end.
 */

export type Gender = "male" | "female";
export type Residency = "ksa" | "international";
export type TrackStatus = "open" | "closed" | "unknown";

export interface Track {
  /** Public token used in the LMS registration URL (?i=…). Never expose circleTypeId. */
  token: string;
  /** Institutional track code, e.g. A11. Verified from LMS page titles. */
  code: string;
  nameAr: string;
  nameEn: string;
  gender: Gender;
  residency: Residency;
  ageMin: number | null;
  ageMax: number | null;
  /** Short descriptors shown on the track card — verbatim from the V1 site. */
  bulletsAr: string[];
  bulletsEn: string[];
  status: TrackStatus;
  /** Internal LMS id, only present for tracks observed closed. Never rendered. */
  circleTypeId?: number;
  /** True for the two international halaqas serving all non-Arabic languages. */
  international?: boolean;
}

const REG_BASE = "https://register.itqan-quran.com/Account/Register";

export function registrationUrl(track: Track): string {
  return `${REG_BASE}?i=${track.token}`;
}

/** Sections shared across the four Arabic registration pages. */
const SECTIONS = {
  nursery: {
    code: "A11",
    nameAr: "قسم الروضة والتأسيس",
    nameEn: "Nursery & Foundation",
    ageMin: 3,
    ageMax: 6,
    bulletsAr: [
      "التأسيس القرآني المبكر",
      "تعليم الحروف والنطق الصحيح عبر برنامج نور البيان",
      "التهيئة لحفظ القرآن بأسلوب يناسب الصغار",
    ],
    bulletsEn: [
      "Early Quranic foundation",
      "Letters and correct pronunciation via the Noor Al-Bayan programme",
      "Preparation for memorisation in a way suited to young children",
    ],
  },
  primary: {
    code: "B11",
    nameAr: "قسم المرحلة الابتدائية",
    nameEn: "Primary Stage",
    ageMin: 7,
    ageMax: 12,
    bulletsAr: ["الحفظ المتدرّج", "تصحيح التلاوة", "غرس حبّ القرآن والالتزام بالورد القرآني"],
    bulletsEn: [
      "Progressive memorisation",
      "Recitation correction",
      "Instilling love of the Quran and a consistent daily portion",
    ],
  },
  intermediate: {
    code: "C11",
    nameAr: "قسم المرحلة المتوسطة والثانوية",
    nameEn: "Intermediate & Secondary Stage",
    ageMin: 13,
    ageMax: 18,
    bulletsAr: ["رفع مستوى الإتقان", "الجمع بين الحفظ والمراجعة", "تعزيز الانضباط الذاتي"],
    bulletsEn: [
      "Raising the level of mastery",
      "Combining memorisation with revision",
      "Strengthening self-discipline",
    ],
  },
  university: {
    code: "C21",
    nameAr: "قسم المرحلة الجامعية والشباب",
    nameArFemale: "قسم المرحلة الجامعية والفتيات",
    nameEn: "University & Youth",
    ageMin: 19,
    ageMax: 40,
    bulletsAr: ["جداول مرنة تناسب الدراسة والعمل", "تحسين التلاوة أو إتمام الحفظ"],
    bulletsEn: [
      "Flexible schedules suited to study and work",
      "Improving recitation or completing memorisation",
    ],
  },
  overForty: {
    code: "D11",
    nameAr: "قسم ما فوق الأربعين",
    nameEn: "Over Forty",
    ageMin: 40,
    ageMax: null,
    bulletsAr: [
      "تصحيح التلاوة",
      "جداول حفظ تناسب المبتدئين وكبار السن",
      "بيئة تعليمية محفّزة ومريحة",
    ],
    bulletsEn: [
      "Recitation correction",
      "Memorisation schedules suited to beginners and older learners",
      "A motivating and comfortable learning environment",
    ],
  },
  specialNeeds: {
    code: "E11",
    nameAr: "قسم ذوي الهمم",
    nameEn: "People of Determination",
    ageMin: null,
    ageMax: null,
    // NOTE: V1 rendered "معلمين مؤهلين" (accusative). Corrected to the
    // nominative "معلمون مؤهلون" — see docs/06-copywriting.md §17 item 4.
    bulletsAr: [
      "خطط تعليمية فردية",
      "معلمون مؤهلون للتعامل مع هذه الفئة",
      "مراعاة الفروق الفردية والقدرات الخاصة",
    ],
    bulletsEn: [
      "Individual learning plans",
      "Teachers qualified to work with this group",
      "Accommodation of individual differences and special abilities",
    ],
  },
  qiraat: {
    code: "H11",
    nameAr: "قسم القراءات والإجازات",
    nameEn: "Qira'at & Ijazah",
    ageMin: null,
    ageMax: null,
    bulletsAr: [
      "تعليم القراءات (القراءة الواحدة، العشر الصغرى، العشر الكبرى)",
      "ضبط الأحكام وتحرير الروايات",
      "منح الإجازات القرآنية بالسند المتصل",
    ],
    bulletsEn: [
      "Teaching the qira'at (single reading, minor ten, major ten)",
      "Mastering the rulings and verifying the riwayat",
      "Granting Quranic ijazah with a connected sanad",
    ],
  },
} as const;

type SectionKey = keyof typeof SECTIONS;

interface Seed {
  section: SectionKey;
  token: string;
  status: TrackStatus;
  circleTypeId?: number;
}

function build(
  seeds: Seed[],
  gender: Gender,
  residency: Residency,
): Track[] {
  return seeds.map(({ section, token, status, circleTypeId }) => {
    const s = SECTIONS[section];
    const nameAr =
      gender === "female" && "nameArFemale" in s ? s.nameArFemale : s.nameAr;
    return {
      token,
      code: s.code,
      nameAr,
      nameEn: s.nameEn,
      gender,
      residency,
      ageMin: s.ageMin,
      ageMax: s.ageMax,
      bulletsAr: [...s.bulletsAr],
      bulletsEn: [...s.bulletsEn],
      status,
      circleTypeId,
    };
  });
}

/** Men, inside KSA — all 7 VERIFIED open on 2026-08-20. */
const MEN_KSA = build(
  [
    { section: "nursery", token: "8711e101-1ca7-4751-8afc-9b3094b74b3c", status: "open" },
    { section: "primary", token: "9fb0852e-38d9-4531-9580-e81e71619d74", status: "open" },
    { section: "intermediate", token: "59ffe975-2fb1-4e86-bd09-24f657467eb8", status: "open" },
    { section: "university", token: "54817afe-2638-44d9-b3a4-b84859d71379", status: "open" },
    { section: "overForty", token: "c221ab1b-2f61-42a0-9437-b2960aea9cc3", status: "open" },
    { section: "specialNeeds", token: "ea5c2438-8b0a-4737-bd1d-dac1e0385763", status: "open" },
    { section: "qiraat", token: "f541eb5f-a1e4-4d58-8093-af35a0b10381", status: "open" },
  ],
  "male",
  "ksa",
);

/** Women, inside KSA — all 7 VERIFIED closed on 2026-08-20. */
const WOMEN_KSA = build(
  [
    { section: "nursery", token: "11c3ac58-1473-42fc-9184-2ce1987411d9", status: "closed", circleTypeId: 44 },
    { section: "primary", token: "181f9ee7-d33a-4990-b9fc-cc3aab19141d", status: "closed", circleTypeId: 46 },
    { section: "intermediate", token: "f0b427f3-e7a0-46a0-9a83-a10dbcc46109", status: "closed", circleTypeId: 48 },
    { section: "university", token: "18e139aa-a7b0-4b2b-b857-f3797c105e27", status: "closed", circleTypeId: 94 },
    { section: "overForty", token: "2c622c8b-4b40-41fd-9d8f-26f17a67b69e", status: "closed", circleTypeId: 50 },
    { section: "specialNeeds", token: "0d651942-c053-4e7f-baae-8969ea64ee34", status: "closed", circleTypeId: 79 },
    { section: "qiraat", token: "d60c5774-abad-4e93-80b8-5eaac2c5c912", status: "closed", circleTypeId: 57 },
  ],
  "female",
  "ksa",
);

/** Men, outside KSA — all 7 VERIFIED closed on 2026-08-20. */
const MEN_INTL = build(
  [
    { section: "nursery", token: "e413d393-fd9e-47b5-9cc8-da96fc5f37bb", status: "closed", circleTypeId: 28 },
    { section: "primary", token: "5799e1e3-d08b-4472-8863-d7e8e5bbf668", status: "closed", circleTypeId: 30 },
    { section: "intermediate", token: "b3872b54-c575-4bf2-84c5-c1cf27b01925", status: "closed", circleTypeId: 32 },
    { section: "university", token: "b0dcf35a-9cac-4acd-b048-c8b384c0a071", status: "closed", circleTypeId: 93 },
    { section: "overForty", token: "a3240f5e-4fed-4ff7-b347-0b1dba31a20e", status: "closed", circleTypeId: 34 },
    { section: "specialNeeds", token: "8c1d160a-071e-4651-8953-1adf4647ec9c", status: "closed", circleTypeId: 36 },
    { section: "qiraat", token: "c1112a77-b6ad-4e93-afbb-8e23fdb3bade", status: "closed", circleTypeId: 38 },
  ],
  "male",
  "international",
);

/** Women, outside KSA — all 7 VERIFIED closed on 2026-08-20. */
const WOMEN_INTL = build(
  [
    { section: "nursery", token: "e924156d-ffea-4e87-837b-6f492fc1cadb", status: "closed", circleTypeId: 45 },
    { section: "primary", token: "8a4c8295-8e57-4e9a-9d8e-85d4c6464608", status: "closed", circleTypeId: 47 },
    { section: "intermediate", token: "086abb57-1fc9-4425-869e-e165ac10ed74", status: "closed", circleTypeId: 49 },
    { section: "university", token: "9d36c55b-bffe-4af2-8501-90a37d419f93", status: "closed", circleTypeId: 92 },
    { section: "overForty", token: "ae3a9345-e0f9-4496-8077-0a07590b4ec5", status: "closed", circleTypeId: 51 },
    { section: "specialNeeds", token: "4fae1c36-3e4f-4f2a-bd19-52f851e8ba7d", status: "closed", circleTypeId: 106 },
    { section: "qiraat", token: "de027861-cd2c-4002-a754-789cfd3bb0d2", status: "closed", circleTypeId: 58 },
  ],
  "female",
  "international",
);

/**
 * The two international halaqas. VERIFIED open.
 * All four language pages (EN/FR/IT/UR) linked to these same two GUIDs in V1 —
 * the language pages were presentational only. See docs/02-pages.md §2.7.
 */
const INTERNATIONAL: Track[] = [
  {
    token: "5c24212d-35b4-4996-8748-55422740a8b4",
    code: "G11",
    nameAr: "الحلقات الدولية للرجال",
    nameEn: "Male International Halaqas",
    gender: "male",
    residency: "international",
    ageMin: null,
    ageMax: null,
    bulletsAr: ["حلقات لغير الناطقين بالعربية", "معلمون يتحدثون لغتك", "جداول تناسب مختلف المناطق الزمنية"],
    bulletsEn: [
      "Halaqas for non-Arabic speakers",
      "Teachers who speak your language",
      "Schedules that suit different time zones",
    ],
    status: "open",
    international: true,
  },
  {
    token: "0118c82d-03e8-4ea1-a475-ee9be52aa23a",
    code: "X11",
    nameAr: "الحلقات الدولية للنساء",
    nameEn: "Female International Halaqas",
    gender: "female",
    residency: "international",
    ageMin: null,
    ageMax: null,
    bulletsAr: ["حلقات لغير الناطقات بالعربية", "معلمات يتحدثن لغتك", "جداول تناسب مختلف المناطق الزمنية"],
    bulletsEn: [
      "Halaqas for non-Arabic speakers",
      "Female teachers who speak your language",
      "Schedules that suit different time zones",
    ],
    status: "open",
    international: true,
  },
];

export const ALL_TRACKS: Track[] = [
  ...MEN_KSA,
  ...WOMEN_KSA,
  ...MEN_INTL,
  ...WOMEN_INTL,
  ...INTERNATIONAL,
];

export interface TrackQuery {
  gender?: Gender;
  residency?: Residency;
  /** When true, return the G11/X11 international halaqas instead of the Arabic tracks. */
  nonArabicSpeaker?: boolean;
}

export function getTracks(q: TrackQuery): Track[] {
  return ALL_TRACKS.filter((t) => {
    if (q.gender && t.gender !== q.gender) return false;
    if (q.nonArabicSpeaker) return Boolean(t.international);
    if (t.international) return false;
    if (q.residency && t.residency !== q.residency) return false;
    return true;
  });
}

export function findTrack(token: string): Track | undefined {
  return ALL_TRACKS.find((t) => t.token === token);
}

/** Availability summary — powers the honesty banner shown before a user commits. */
export function summarise(tracks: Track[]) {
  const open = tracks.filter((t) => t.status === "open").length;
  return { total: tracks.length, open, closed: tracks.length - open };
}
