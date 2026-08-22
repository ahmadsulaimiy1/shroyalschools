import type { ReactNode } from "react";

export function Section({
  children,
  className = "",
  alt = false,
  id,
}: {
  children: ReactNode;
  className?: string;
  alt?: boolean;
  id?: string;
}) {
  return (
    <section
      id={id}
      className={`py-16 sm:py-20 ${alt ? "bg-surface-alt" : ""} ${className}`}
    >
      <div className="container-x">{children}</div>
    </section>
  );
}

export function SectionHeading({
  title,
  subtitle,
  as: As = "h2",
}: {
  title: string;
  subtitle?: string;
  as?: "h1" | "h2" | "h3";
}) {
  return (
    <div className="mb-12 text-center">
      {/* Real text in the DOM. V1 left headings empty until JS typed them in
          (docs/03 §6), so crawlers and screen readers could see nothing. */}
      <As className="mb-4 text-3xl font-bold text-primary lg:text-4xl">{title}</As>
      <div className="divider-gold" aria-hidden="true" />
      {subtitle ? (
        <p className="mx-auto mt-5 max-w-2xl leading-relaxed text-gray-600">{subtitle}</p>
      ) : null}
    </div>
  );
}
