"use client";

import { useState } from "react";
import type { Locale } from "@/lib/i18n";
import { getDict } from "@/lib/dictionary";

/**
 * Waitlist form.
 *
 * Every field is labelled and every error message is specific and localised.
 * V1's LMS forms used data-val-required="*" — an asterisk as the entire error
 * message, on 13 required fields (docs/07 §3).
 *
 * Errors are announced via role="alert" and linked with aria-describedby, so
 * screen-reader users are told what failed and why.
 */
export default function WaitlistForm({
  locale,
  token,
}: {
  locale: Locale;
  token: string;
}) {
  const t = getDict(locale);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [submitted, setSubmitted] = useState(false);
  const [pending, setPending] = useState(false);

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const fd = new FormData(e.currentTarget);
    const next: Record<string, string> = {};

    const name = String(fd.get("name") ?? "").trim();
    const email = String(fd.get("email") ?? "").trim();
    const whatsapp = String(fd.get("whatsapp") ?? "").trim();
    const consent = fd.get("consent");

    if (!name) next.name = t.errors.nameRequired;
    if (!email) next.email = t.errors.emailRequired;
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) next.email = t.errors.emailInvalid;
    if (!whatsapp || whatsapp.replace(/\D/g, "").length < 8) next.whatsapp = t.errors.whatsappRequired;
    if (!consent) next.consent = t.errors.consentRequired;

    setErrors(next);
    if (Object.keys(next).length > 0) {
      document.getElementById(`field-${Object.keys(next)[0]}`)?.focus();
      return;
    }

    setPending(true);
    try {
      await fetch("/api/waitlist", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          trackToken: token,
          name, email, whatsapp,
          age: fd.get("age") || null,
          locale,
          consent: true,
        }),
      });
      setSubmitted(true);
    } finally {
      setPending(false);
    }
  }

  if (submitted) {
    return (
      <div role="status" className="card border-success/30 bg-success/5">
        <p className="text-lg font-bold text-success">
          {locale === "ar" ? "تم تسجيل بياناتك بنجاح" : "You are on the list"}
        </p>
        <p className="mt-2 leading-relaxed text-gray-700">
          {locale === "ar"
            ? "سنتواصل معك عبر البريد الإلكتروني وواتساب فور فتح التسجيل في هذا المسار بإذن الله."
            : "We will contact you by email and WhatsApp as soon as registration reopens for this track, God willing."}
        </p>
      </div>
    );
  }

  const field = (name: string, label: string, type = "text", required = true) => (
    <div>
      <label htmlFor={`field-${name}`} className="mb-2 block font-medium">
        {label}{" "}
        {required && (
          <>
            <span aria-hidden="true" className="text-danger">*</span>
            <span className="sr-only">({t.common.required})</span>
          </>
        )}
      </label>
      <input
        id={`field-${name}`}
        name={name}
        type={type}
        required={required}
        dir={type === "email" || name === "whatsapp" ? "ltr" : undefined}
        aria-invalid={errors[name] ? true : undefined}
        aria-describedby={errors[name] ? `err-${name}` : undefined}
        className={`w-full rounded-xl border-2 bg-white px-4 py-3 ${
          errors[name] ? "border-danger" : "border-primary/20"
        }`}
      />
      {errors[name] && (
        <p id={`err-${name}`} role="alert" className="mt-1.5 text-sm font-medium text-danger">
          {errors[name]}
        </p>
      )}
    </div>
  );

  return (
    <form onSubmit={onSubmit} noValidate className="space-y-5">
      {field("name", t.register.name)}
      {/* The field V1 never collected — without it a reopening cannot be announced. */}
      {field("email", t.register.email, "email")}
      {field("whatsapp", t.register.whatsapp, "tel")}
      {field("age", t.register.age, "number", false)}

      <div>
        <label className="flex cursor-pointer items-start gap-3">
          <input
            id="field-consent"
            name="consent"
            type="checkbox"
            aria-invalid={errors.consent ? true : undefined}
            aria-describedby={errors.consent ? "err-consent" : undefined}
            className="mt-1 h-5 w-5 accent-[var(--color-primary)]"
          />
          <span className="text-sm leading-relaxed">{t.register.consent}</span>
        </label>
        {errors.consent && (
          <p id="err-consent" role="alert" className="mt-1.5 text-sm font-medium text-danger">
            {errors.consent}
          </p>
        )}
      </div>

      <button type="submit" disabled={pending} className="btn btn-primary w-full">
        {pending ? "…" : t.register.submit}
      </button>
    </form>
  );
}
