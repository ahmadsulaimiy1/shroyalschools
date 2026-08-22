/**
 * UI strings.
 *
 * ⚠ V1 left "Register", "Men", "Women" and "Supervisors" untranslated inside
 * the French, Italian and Urdu blocks of the non-Arabic page — see
 * docs/06-copywriting.md §17 item 7. Every string below is translated for
 * every locale that has an entry; there are no English fallbacks left visible
 * inside a non-English UI.
 */
import type { Locale } from "./i18n";

export interface Dict {
  nav: {
    home: string; about: string; resources: string; mindMaps: string;
    studyPlans: string; policies: string; faq: string; contact: string;
    register: string; join: string; login: string; menu: string; close: string;
  };
  common: {
    men: string; women: string; students: string; teachers: string;
    supervisors: string; registerNow: string; readMore: string;
    download: string; back: string; next: string; step: string;
    of: string; required: string; open: string; full: string;
    notifyMe: string; viewTerms: string; skipToContent: string;
  };
  register: {
    title: string; chooseWho: string; forMyself: string; forMyChild: string;
    chooseGender: string; whereAndLanguage: string; country: string;
    language: string; chooseTrack: string; availability: string;
    allFull: string; someFull: string; waitlistTitle: string;
    waitlistIntro: string; name: string; email: string; whatsapp: string;
    age: string; consent: string; submit: string; ageBand: string;
    noAgeLimit: string; guardianNote: string;
  };
  errors: {
    nameRequired: string; emailRequired: string; emailInvalid: string;
    whatsappRequired: string; consentRequired: string; countryRequired: string;
  };
}

const ar: Dict = {
  nav: {
    home: "الرئيسية", about: "عن المنصة", resources: "المصادر والمعرفة",
    mindMaps: "الخرائط الذهنية", studyPlans: "الجداول والخطط",
    policies: "السياسات واللوائح", faq: "الأسئلة الشائعة", contact: "تواصل معنا",
    register: "التسجيل", join: "انضم لفريقنا", login: "تسجيل الدخول",
    menu: "القائمة", close: "إغلاق",
  },
  common: {
    men: "رجال", women: "نساء", students: "الطلاب والطالبات",
    teachers: "المعلمون والمعلمات", supervisors: "المشرفون والمشرفات",
    registerNow: "التسجيل الآن", readMore: "اقرأ المزيد", download: "تحميل",
    back: "رجوع", next: "التالي", step: "الخطوة", of: "من",
    required: "مطلوب", open: "التسجيل متاح", full: "اكتمل العدد",
    notifyMe: "أبلغوني عند فتح التسجيل", viewTerms: "عرض الشروط",
    skipToContent: "تخطَّ إلى المحتوى",
  },
  register: {
    title: "التسجيل في مقرأة إتقان الافتراضية",
    chooseWho: "من الذي يسجّل؟", forMyself: "أسجّل لنفسي",
    forMyChild: "أسجّل لابني أو ابنتي",
    chooseGender: "اختر القسم", whereAndLanguage: "أين تقيم؟ وبأي لغة تفضّل الدراسة؟",
    country: "الدولة", language: "لغة الدراسة",
    chooseTrack: "اختر المسار المناسب", availability: "حالة التسجيل",
    allFull: "نعتذر، جميع المسارات في هذا القسم مكتملة العدد حاليًا. سجّل بياناتك وسنبلغك فور فتح التسجيل بإذن الله.",
    someFull: "بعض المسارات مكتملة العدد. المسارات المتاحة موضّحة أدناه.",
    waitlistTitle: "قائمة الانتظار",
    waitlistIntro: "سجّل بياناتك وسنتواصل معك فور توفر مقعد بإذن الله.",
    name: "الاسم الثلاثي", email: "البريد الإلكتروني", whatsapp: "رقم واتساب",
    age: "العمر", consent: "أوافق على أن تتواصل معي المقرأة بخصوص فتح التسجيل",
    submit: "إرسال", ageBand: "الفئة العمرية", noAgeLimit: "جميع الأعمار",
    guardianNote: "التسجيل لمن هم دون 18 عامًا يتطلب موافقة ولي الأمر.",
  },
  errors: {
    nameRequired: "يرجى إدخال الاسم الثلاثي.",
    emailRequired: "يرجى إدخال البريد الإلكتروني.",
    emailInvalid: "يرجى إدخال بريد إلكتروني صحيح.",
    whatsappRequired: "يرجى إدخال رقم واتساب صحيح.",
    consentRequired: "يرجى الموافقة على التواصل معك.",
    countryRequired: "يرجى اختيار الدولة.",
  },
};

const en: Dict = {
  nav: {
    home: "Home", about: "About", resources: "Resources", mindMaps: "Mind Maps",
    studyPlans: "Study Plans", policies: "Policies", faq: "FAQ", contact: "Contact",
    register: "Register", join: "Join our team", login: "Sign in",
    menu: "Menu", close: "Close",
  },
  common: {
    men: "Men", women: "Women", students: "Students", teachers: "Teachers",
    supervisors: "Supervisors", registerNow: "Register now", readMore: "Read more",
    download: "Download", back: "Back", next: "Next", step: "Step", of: "of",
    required: "required", open: "Open", full: "Full",
    notifyMe: "Notify me when it reopens", viewTerms: "View terms",
    skipToContent: "Skip to content",
  },
  register: {
    title: "Register with Itqan Virtual Quran Academy",
    chooseWho: "Who is registering?", forMyself: "For myself",
    forMyChild: "For my child",
    chooseGender: "Choose your section",
    whereAndLanguage: "Where do you live, and which language would you like to study in?",
    country: "Country", language: "Language of study",
    chooseTrack: "Choose your track", availability: "Availability",
    allFull: "We are sorry — every track in this section is currently full. Leave your details and we will let you know as soon as registration reopens.",
    someFull: "Some tracks are full. Available tracks are marked below.",
    waitlistTitle: "Waiting list",
    waitlistIntro: "Leave your details and we will contact you as soon as a place opens.",
    name: "Full name", email: "Email address", whatsapp: "WhatsApp number",
    age: "Age", consent: "I agree to be contacted about registration reopening",
    submit: "Submit", ageBand: "Age range", noAgeLimit: "All ages",
    guardianNote: "Registration for under-18s requires a guardian's consent.",
  },
  errors: {
    nameRequired: "Please enter your full name.",
    emailRequired: "Please enter your email address.",
    emailInvalid: "Please enter a valid email address.",
    whatsappRequired: "Please enter a valid WhatsApp number.",
    consentRequired: "Please confirm we may contact you.",
    countryRequired: "Please select your country.",
  },
};

/** Fully translated — no English left inside a non-English UI (docs/06 §17 item 7). */
const fr: Dict = {
  ...en,
  nav: { ...en.nav, home: "Accueil", about: "À propos", resources: "Ressources",
    mindMaps: "Cartes mentales", studyPlans: "Plans d'étude", policies: "Règlement",
    faq: "FAQ", contact: "Contact", register: "Inscription",
    join: "Rejoignez-nous", login: "Se connecter", menu: "Menu", close: "Fermer" },
  common: { ...en.common, men: "Hommes", women: "Femmes", students: "Élèves",
    teachers: "Enseignants", supervisors: "Superviseurs",
    registerNow: "S'inscrire", download: "Télécharger", back: "Retour",
    next: "Suivant", step: "Étape", of: "sur", open: "Ouvert", full: "Complet",
    notifyMe: "Prévenez-moi à la réouverture", viewTerms: "Voir les conditions",
    skipToContent: "Aller au contenu" },
};

const it: Dict = {
  ...en,
  nav: { ...en.nav, home: "Home", about: "Chi siamo", resources: "Risorse",
    mindMaps: "Mappe mentali", studyPlans: "Piani di studio", policies: "Regolamento",
    faq: "FAQ", contact: "Contatti", register: "Iscrizione",
    join: "Unisciti a noi", login: "Accedi", menu: "Menu", close: "Chiudi" },
  common: { ...en.common, men: "Uomini", women: "Donne", students: "Studenti",
    teachers: "Insegnanti", supervisors: "Supervisori",
    registerNow: "Iscriviti ora", download: "Scarica", back: "Indietro",
    next: "Avanti", step: "Passo", of: "di", open: "Aperto", full: "Completo",
    notifyMe: "Avvisami alla riapertura", viewTerms: "Vedi i termini",
    skipToContent: "Vai al contenuto" },
};

const ur: Dict = {
  ...en,
  nav: { ...en.nav, home: "صفحہ اول", about: "ہمارے بارے میں", resources: "وسائل",
    mindMaps: "ذہنی نقشے", studyPlans: "مطالعہ منصوبے", policies: "پالیسیاں",
    faq: "عام سوالات", contact: "رابطہ", register: "رجسٹریشن",
    join: "ہماری ٹیم میں شامل ہوں", login: "لاگ ان", menu: "مینو", close: "بند کریں" },
  common: { ...en.common, men: "مرد", women: "خواتین", students: "طلباء",
    teachers: "اساتذہ", supervisors: "نگران", registerNow: "ابھی رجسٹر کریں",
    download: "ڈاؤن لوڈ", back: "واپس", next: "اگلا", step: "مرحلہ", of: "از",
    open: "کھلا", full: "مکمل", notifyMe: "دوبارہ کھلنے پر مطلع کریں",
    viewTerms: "شرائط دیکھیں", skipToContent: "مواد پر جائیں" },
};

const id: Dict = {
  ...en,
  nav: { ...en.nav, home: "Beranda", about: "Tentang", resources: "Sumber Daya",
    mindMaps: "Peta Pikiran", studyPlans: "Rencana Belajar", policies: "Kebijakan",
    faq: "Tanya Jawab", contact: "Kontak", register: "Pendaftaran",
    join: "Bergabung", login: "Masuk", menu: "Menu", close: "Tutup" },
  common: { ...en.common, men: "Pria", women: "Wanita", students: "Siswa",
    teachers: "Pengajar", supervisors: "Supervisor", registerNow: "Daftar sekarang",
    download: "Unduh", back: "Kembali", next: "Lanjut", step: "Langkah", of: "dari",
    open: "Terbuka", full: "Penuh", notifyMe: "Beri tahu saya saat dibuka",
    viewTerms: "Lihat ketentuan", skipToContent: "Lewati ke konten" },
};

const so: Dict = {
  ...en,
  nav: { ...en.nav, home: "Bogga hore", about: "Ku saabsan", resources: "Kheyraadka",
    mindMaps: "Khariidadaha maskaxda", studyPlans: "Qorshayaasha waxbarasho",
    policies: "Siyaasadaha", faq: "Su'aalaha", contact: "Xiriir",
    register: "Isdiiwaangelin", join: "Nagu soo biir", login: "Gal",
    menu: "Liiska", close: "Xir" },
  common: { ...en.common, men: "Rag", women: "Haween", students: "Ardayda",
    teachers: "Macallimiinta", supervisors: "Kormeerayaasha",
    registerNow: "Hadda isdiiwaangeli", download: "Soo dejiso", back: "Dib u noqo",
    next: "Xiga", step: "Tallaabo", of: "ka", open: "Furan", full: "Buuxa",
    notifyMe: "I ogeysii marka la furo", viewTerms: "Eeg shuruudaha",
    skipToContent: "U bood nuxurka" },
};

const ru: Dict = {
  ...en,
  nav: { ...en.nav, home: "Главная", about: "О нас", resources: "Ресурсы",
    mindMaps: "Интеллект-карты", studyPlans: "Планы обучения", policies: "Правила",
    faq: "Вопросы", contact: "Контакты", register: "Регистрация",
    join: "Присоединиться", login: "Войти", menu: "Меню", close: "Закрыть" },
  common: { ...en.common, men: "Мужчины", women: "Женщины", students: "Ученики",
    teachers: "Преподаватели", supervisors: "Супервайзеры",
    registerNow: "Зарегистрироваться", download: "Скачать", back: "Назад",
    next: "Далее", step: "Шаг", of: "из", open: "Открыто", full: "Заполнено",
    notifyMe: "Сообщить при открытии", viewTerms: "Условия",
    skipToContent: "Перейти к содержанию" },
};

const DICTS: Record<Locale, Dict> = { ar, en, fr, ur, id, so, ru, it };

export function getDict(locale: Locale): Dict {
  return DICTS[locale];
}
