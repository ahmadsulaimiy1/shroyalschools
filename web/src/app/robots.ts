import type { MetadataRoute } from "next";
import { SITE } from "@/lib/site";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: "*",
        allow: "/",
        // Waitlist confirmations are per-user and carry no SEO value.
        disallow: ["/api/", "/*/waitlist/"],
      },
    ],
    sitemap: `${SITE.url}/sitemap.xml`,
  };
}
