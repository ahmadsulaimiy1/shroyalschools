import { NextResponse } from "next/server";
import { ALL_TRACKS, summarise, registrationUrl, type Gender, type Residency } from "@/lib/tracks";

/**
 * Public availability API — the integration specified in
 * docs/11-api-inference.md §2 as "if only one thing is built, build this".
 *
 * Read-only, no PII, cacheable. Exposes the public GUID token only — never the
 * internal circleTypeId, which V1 leaked in its closed-track redirect URL.
 */
export const runtime = "nodejs";
export const revalidate = 300;

export async function GET(req: Request) {
  const url = new URL(req.url);
  const gender = url.searchParams.get("gender") as Gender | null;
  const residency = url.searchParams.get("residency") as Residency | null;

  const data = ALL_TRACKS.filter((t) => {
    if (gender && t.gender !== gender) return false;
    if (residency && t.residency !== residency) return false;
    return true;
  }).map((t) => ({
    token: t.token,
    code: t.code,
    name: { ar: t.nameAr, en: t.nameEn },
    gender: t.gender,
    residency: t.residency,
    ageRange: { min: t.ageMin, max: t.ageMax },
    availability: { status: t.status },
    registerUrl: registrationUrl(t),
  }));

  return NextResponse.json(
    { data, meta: { ...summarise(ALL_TRACKS.filter((t) => data.some((d) => d.token === t.token))) } },
    { headers: { "Cache-Control": "public, s-maxage=300, stale-while-revalidate=600" } },
  );
}
