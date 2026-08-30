"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const NAV = [
  { href: "/", label: "Dashboard", match: "/" },
  { href: "/#vyzvy", label: "Moje Výzvy", match: "/#vyzvy" },
  { href: "/#ziadosti", label: "AI Žiadosti", match: "/#ziadosti" },
  { href: "/#profil", label: "Finančný Profil", match: "/#profil" },
  { href: "/#konzultanti", label: "Konzultanti", match: "/#konzultanti" },
  { href: "/o-nas", label: "O nás", match: "/o-nas" },
];

function isActive(pathname: string, item: (typeof NAV)[number]) {
  if (item.match === "/o-nas") return pathname === "/o-nas";
  if (item.match === "/") return pathname === "/";
  return false;
}

export function AppShell({
  children,
  apiOnline,
}: {
  children: React.ReactNode;
  apiOnline?: boolean | null;
}) {
  const pathname = usePathname();

  return (
    <div className="min-h-screen">
      <header className="sticky top-0 z-40 border-b border-line/70 bg-background/85 backdrop-blur-md">
        <div className="mx-auto flex max-w-6xl items-center gap-4 px-4 py-3 md:px-6">
          <Link href="/" className="flex items-center gap-2.5 shrink-0">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src="/icons/icon-192x192.png"
              alt=""
              width={36}
              height={36}
              className="rounded-lg"
            />
            <span className="font-display text-lg font-semibold tracking-tight text-white">
              GrantFlow<span className="text-accent">.sk</span>
            </span>
          </Link>

          <div className="ml-auto hidden flex-1 max-w-md md:block">
            <label className="sr-only" htmlFor="global-search">
              Hľadať výzvu / IČO
            </label>
            <input
              id="global-search"
              type="search"
              placeholder="Hľadať výzvu / IČO…"
              className="w-full rounded-xl border border-line bg-panel px-3 py-2 text-sm text-foreground placeholder:text-muted outline-none focus:border-accent"
            />
          </div>

          <div className="flex items-center gap-3">
            <span
              className={`hidden text-xs sm:inline ${
                apiOnline === true
                  ? "text-ok"
                  : apiOnline === false
                    ? "text-bad"
                    : "text-muted"
              }`}
              title="AI API health"
            >
              {apiOnline === true
                ? "API online"
                : apiOnline === false
                  ? "API offline"
                  : "API…"}
            </span>
            <button
              type="button"
              className="relative rounded-full border border-line bg-panel px-2.5 py-1.5 text-sm text-muted hover:text-foreground"
              aria-label="Notifikácie"
            >
              3
              <span className="absolute -right-0.5 -top-0.5 h-2 w-2 rounded-full bg-accent animate-pulse-soft" />
            </button>
            <div className="rounded-full border border-line bg-panel px-3 py-1.5 text-sm">
              TechMSP
            </div>
          </div>
        </div>

        <nav className="mx-auto flex max-w-6xl gap-1 overflow-x-auto px-4 pb-2 md:px-6">
          {NAV.map((item) => {
            const active = isActive(pathname, item);
            return (
              <Link
                key={item.label}
                href={item.href}
                className={`whitespace-nowrap rounded-lg px-3 py-1.5 text-sm transition ${
                  active
                    ? "bg-accent/20 text-white"
                    : "text-muted hover:bg-panel hover:text-foreground"
                }`}
              >
                {item.label}
              </Link>
            );
          })}
        </nav>
      </header>

      <main className="mx-auto max-w-6xl px-4 py-6 md:px-6 md:py-8">{children}</main>
    </div>
  );
}
