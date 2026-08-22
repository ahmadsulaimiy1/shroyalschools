import type { Locale } from "@/lib/i18n";
import { WHATSAPP_MEN, waLink } from "@/lib/site";

const LABEL: Record<string, string> = {
  ar: "تواصل معنا عبر واتساب",
  en: "Contact us on WhatsApp",
  fr: "Contactez-nous sur WhatsApp",
  it: "Contattaci su WhatsApp",
  ur: "واٹس ایپ پر رابطہ کریں",
  id: "Hubungi kami di WhatsApp",
  so: "Nagala soo xiriir WhatsApp",
  ru: "Написать нам в WhatsApp",
};

export default function WhatsAppButton({ locale }: { locale: Locale }) {
  const label = LABEL[locale] ?? LABEL.en;
  return (
    <a
      href={waLink(WHATSAPP_MEN)}
      aria-label={label}
      title={label}
      className="no-print fixed bottom-5 end-5 z-30 grid h-14 w-14 place-items-center rounded-full bg-[#25D366] text-white shadow-lg transition-transform hover:scale-105"
    >
      <svg width="26" height="26" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
        <path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38a9.9 9.9 0 004.79 1.22h.01c5.46 0 9.9-4.45 9.9-9.91C21.95 6.45 17.5 2 12.04 2zm5.8 14.16c-.24.68-1.2 1.26-1.97 1.42-.53.11-1.21.2-3.51-.75-2.95-1.22-4.85-4.21-5-4.4-.14-.2-1.19-1.58-1.19-3.02s.75-2.14 1.02-2.43c.27-.29.59-.37.78-.37h.56c.18 0 .42-.07.66.5.24.58.83 2.01.9 2.16.07.14.12.31.02.51-.1.2-.15.32-.29.49-.15.17-.31.38-.44.51-.15.14-.3.3-.13.59.17.29.76 1.25 1.63 2.03 1.12 1 2.06 1.31 2.35 1.46.29.14.46.12.63-.07.17-.2.73-.85.92-1.14.2-.29.39-.24.66-.14.27.1 1.7.8 1.99.95.29.14.48.22.55.34.07.12.07.7-.17 1.38z" />
      </svg>
    </a>
  );
}
