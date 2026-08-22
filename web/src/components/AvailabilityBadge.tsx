import type { TrackStatus } from "@/lib/tracks";
import type { Locale } from "@/lib/i18n";
import { getDict } from "@/lib/dictionary";

/**
 * The single highest-value component in this rebuild.
 *
 * V1 gave no indication of whether a track was open. 22 of 36 entry points
 * were full, so 61% of registration journeys ended at a dead end the user
 * only discovered after leaving the site (docs/08 §4.6).
 *
 * Status is conveyed by text and icon, never by colour alone (WCAG 1.4.1).
 */
export default function AvailabilityBadge({
  status,
  locale,
}: {
  status: TrackStatus;
  locale: Locale;
}) {
  const t = getDict(locale);

  if (status === "open") {
    return (
      <span className="inline-flex items-center gap-1.5 rounded-full bg-success/10 px-3 py-1 text-xs font-bold text-success">
        <svg width="12" height="12" viewBox="0 0 16 16" fill="none" aria-hidden="true">
          <path d="M3 8.5l3.5 3.5L13 5" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
        {t.common.open}
      </span>
    );
  }

  if (status === "closed") {
    return (
      <span className="inline-flex items-center gap-1.5 rounded-full bg-warning/10 px-3 py-1 text-xs font-bold text-warning">
        <svg width="12" height="12" viewBox="0 0 16 16" fill="none" aria-hidden="true">
          <circle cx="8" cy="8" r="6.5" stroke="currentColor" strokeWidth="2" />
          <path d="M8 4.5V8l2.5 2" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
        </svg>
        {t.common.full}
      </span>
    );
  }

  return null;
}
