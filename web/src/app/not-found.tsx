import Link from "next/link";

export default function RootNotFound() {
  return (
    <html lang="ar" dir="rtl">
      <body>
        <main style={{ display: "grid", placeItems: "center", minHeight: "100vh", padding: "2rem", textAlign: "center", fontFamily: "system-ui, sans-serif" }}>
          <div>
            <h1 style={{ color: "#027043", marginBottom: "1rem" }}>الصفحة غير موجودة</h1>
            <Link href="/ar" style={{ color: "#027043", textDecoration: "underline" }}>
              العودة للصفحة الرئيسية
            </Link>
          </div>
        </main>
      </body>
    </html>
  );
}
