"use client";

import type { ButtonHTMLAttributes, ReactNode } from "react";

type Variant = "filled" | "tonal" | "outlined" | "text";

const VARIANT: Record<Variant, string> = {
  filled:
    "bg-accent text-white shadow-md shadow-accent/25 hover:bg-accent-soft active:scale-[0.98] disabled:bg-accent/40",
  tonal:
    "bg-accent/18 text-sky-200 hover:bg-accent/28 active:scale-[0.98] disabled:opacity-50",
  outlined:
    "border border-line bg-transparent text-foreground hover:border-accent/60 hover:bg-panel/60 active:scale-[0.98]",
  text: "bg-transparent text-muted hover:bg-panel/80 hover:text-foreground active:scale-[0.98]",
};

export function UiButton({
  variant = "filled",
  className = "",
  children,
  ...props
}: ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: Variant;
  children: ReactNode;
}) {
  return (
    <button
      type="button"
      {...props}
      className={[
        "inline-flex items-center justify-center gap-2 rounded-2xl px-5 py-2.5 text-sm font-semibold tracking-wide",
        "transition-[transform,background-color,box-shadow,border-color,color] duration-150 ease-out",
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/70 focus-visible:ring-offset-2 focus-visible:ring-offset-background",
        "disabled:cursor-not-allowed disabled:shadow-none",
        VARIANT[variant],
        className,
      ].join(" ")}
    >
      {children}
    </button>
  );
}
