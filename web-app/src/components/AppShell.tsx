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
    <div className="flex min-h-screen min-h-[100dvh] flex-col">
      <header className="sticky top-0 z-40 shrink-0 border-b border-line/70 bg-background/90 shadow-[var(--elev-1)] backdrop-blur-md">
        <div className="mx-auto flex max-w-6xl items-center gap-4 px-4 py-3 md:px-6">
          <Link href="/" className="flex shrink-0 items-center gap-2.5">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src="/icons/icon-192x192.png"
              alt=""
              width={40}
              height={40}
              className="rounded-2xl shadow-md shadow-accent/20"
            />
            <span className="font-display text-lg font-semibold tracking-tight text-white">
              GrantFlow<span className="text-accent">.sk</span>
            </span>
          </Link>

          <div className="ml-auto hidden max-w-md flex-1 md:block">
            <label className="sr-only" htmlFor="global-search">
              Hľadať výzvu / IČO
            </label>
            <input
              id="global-search"
              type="search"
              placeholder="Hľadať výzvu / IČO…"
              className="w-full rounded-2xl border border-line bg-panel px-4 py-2.5 text-sm text-foreground placeholder:text-muted outline-none transition focus:border-accent focus:ring-2 focus:ring-accent/40"
            />
          </div>

          <div className="flex items-center gap-2.5">
            <span
              className={`hidden rounded-full px-2.5 py-1 text-xs font-medium sm:inline ${
                apiOnline === true
                  ? "bg-ok/15 text-ok"
                  : apiOnline === false
                    ? "bg-bad/15 text-bad"
                    : "bg-panel text-muted"
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
              className="relative flex h-10 w-10 items-center justify-center rounded-full border border-line bg-panel text-sm text-muted transition hover:bg-panel-2 hover:text-foreground active:scale-95"
              aria-label="Notifikácie"
            >
              3
              <span className="absolute right-1 top-1 h-2 w-2 rounded-full bg-accent animate-pulse-soft" />
            </button>
            <div className="flex h-10 items-center rounded-full border border-line bg-panel px-3.5 text-sm font-medium">
              TechMSP
            </div>
          </div>
        </div>

        <nav className="mx-auto flex max-w-6xl gap-1.5 overflow-x-auto px-4 pb-2.5 md:px-6">
          {NAV.map((item) => {
            const active = isActive(pathname, item);
            return (
              <Link
                key={item.label}
                href={item.href}
                className={`whitespace-nowrap rounded-2xl px-3.5 py-2 text-sm font-medium transition active:scale-[0.98] ${
                  active
                    ? "bg-accent text-white shadow-md shadow-accent/25"
                    : "text-muted hover:bg-panel hover:text-foreground"
                }`}
              >
                {item.label}
              </Link>
            );
          })}
        </nav>
      </header>

      <main className="mx-auto flex w-full max-w-6xl flex-1 flex-col px-4 py-6 md:px-6 md:py-8">
        {children}
      </main>
    </div>
  );
}
