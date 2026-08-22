import { NextResponse } from "next/server";
import { findTrack } from "@/lib/tracks";

/**
 * Waitlist intake.
 *
 * Server-side validation MIRRORS the client rules — the client checks are a
 * convenience, never the enforcement point.
 *
 * ⚠ Deliberately does NOT persist yet. Per docs/18 §3, Saudi PDPL expects
 * children's personal data to remain inside the Kingdom, and this track's
 * waitlist can carry a minor's details. Wiring a store before the hosting
 * decision is made would create exactly the cross-border exposure the audit
 * flagged in V1 (which routed registrations through Google Forms).
 *
 * To activate: set WAITLIST_ENDPOINT to an in-Kingdom endpoint. Until then the
 * route validates, logs nothing sensitive, and returns success shape so the UI
 * contract is stable.
 */

export const runtime = "nodejs";

interface Body {
  trackToken?: string;
  name?: string;
  email?: string;
  whatsapp?: string;
  age?: string | number | null;
  locale?: string;
  consent?: boolean;
}

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

export async function POST(req: Request) {
  let body: Body;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: "invalid_json" }, { status: 400 });
  }

  const errors: Record<string, string> = {};

  const track = body.trackToken ? findTrack(body.trackToken) : undefined;
  if (!track) errors.trackToken = "unknown_track";

  const name = (body.name ?? "").trim();
  if (name.length < 2) errors.name = "name_required";

  const email = (body.email ?? "").trim();
  if (!email) errors.email = "email_required";
  else if (!EMAIL_RE.test(email)) errors.email = "email_invalid";

  const whatsapp = (body.whatsapp ?? "").replace(/\D/g, "");
  if (whatsapp.length < 8) errors.whatsapp = "whatsapp_required";

  if (body.consent !== true) errors.consent = "consent_required";

  if (Object.keys(errors).length > 0) {
    return NextResponse.json({ error: "validation_failed", fields: errors }, { status: 422 });
  }

  const endpoint = process.env.WAITLIST_ENDPOINT;
  if (!endpoint) {
    // No in-Kingdom store configured — accept and instruct, do not persist.
    return NextResponse.json(
      { ok: true, stored: false, note: "WAITLIST_ENDPOINT not configured" },
      { status: 202 },
    );
  }

  try {
    const res = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(process.env.WAITLIST_TOKEN
          ? { Authorization: `Bearer ${process.env.WAITLIST_TOKEN}` }
          : {}),
      },
      body: JSON.stringify({
        trackToken: track!.token,
        trackCode: track!.code,
        name, email, whatsapp,
        age: body.age ?? null,
        locale: body.locale ?? null,
        consentAt: new Date().toISOString(),
      }),
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    return NextResponse.json({ ok: true, stored: true });
  } catch {
    return NextResponse.json({ error: "upstream_unavailable" }, { status: 502 });
  }
}
