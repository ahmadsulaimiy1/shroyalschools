import type { MetadataRoute } from "next";
import { LOCALES } from "@/lib/i18n";
import { SITE } from "@/lib/site";

/**
 * V1's wp-sitemap.xml advertised a page that returned 404 (the WordPress
 * Sample Page), plus the default "Hello World" post and "Uncategorised"
 * category (docs/01 §2). Only real, reachable routes are listed here.
 */
const ROUTES = [
  { path: "", priority: 1.0, changeFrequency: "weekly" as const },
  { path: "/register", priority: 0.9, changeFrequency: "daily" as const },
  { path: "/about", priority: 0.7, changeFrequency: "monthly" as const },
  { path: "/faq", priority: 0.7, changeFrequency: "monthly" as const },
  { path: "/resources", priority: 0.6, changeFrequency: "monthly" as const },
  { path: "/resources/mind-maps", priority: 0.6, changeFrequency: "monthly" as const },
  { path: "/resources/study-plans", priority: 0.6, changeFrequency: "monthly" as const },
  { path: "/policies", priority: 0.5, changeFrequency: "yearly" as const },
  { path: "/contact", priority: 0.5, changeFrequency: "yearly" as const },
  { path: "/join", priority: 0.5, changeFrequency: "monthly" as const },
];

export default function sitemap(): MetadataRoute.Sitemap {
  const now = new Date();
  return LOCALES.flatMap((locale) =>
    ROUTES.map((r) => ({
      url: `${SITE.url}/${locale}${r.path}`,
      lastModified: now,
      changeFrequency: r.changeFrequency,
      priority: r.priority,
      alternates: {
        languages: Object.fromEntries(
          LOCALES.map((l) => [l, `${SITE.url}/${l}${r.path}`]),
        ),
      },
    })),
  );
}
