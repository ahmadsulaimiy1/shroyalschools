import Link from "next/link";
import { Section } from "@/components/Section";

export default function NotFound() {
  return (
    <Section>
      <div className="mx-auto max-w-xl text-center">
        <p className="mb-4 text-6xl font-bold text-primary/20">404</p>
        <h1 className="mb-4 text-2xl font-bold text-primary">الصفحة غير موجودة</h1>
        <p className="mb-8 leading-relaxed text-gray-700">
          عذرًا، الصفحة التي تبحث عنها غير متاحة. يمكنك العودة للصفحة الرئيسية أو الانتقال
          مباشرة إلى صفحة التسجيل.
        </p>
        <div className="flex flex-wrap justify-center gap-3">
          <Link href="/ar" className="btn btn-primary">الصفحة الرئيسية</Link>
          <Link href="/ar/register" className="btn btn-outline">التسجيل</Link>
        </div>
      </div>
    </Section>
  );
}
