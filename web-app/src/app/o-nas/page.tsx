import type { Metadata } from "next";
import { AppShell } from "@/components/AppShell";
import { checkApiHealth } from "@/lib/api";

export const metadata: Metadata = {
  title: "O nás",
  description:
    "Čo je GrantFlow.sk — digitálny pomocník pre európske a štátne dotácie pre slovenské firmy.",
};

const BENEFITS = [
  {
    title: "Nájde vhodné výzvy",
    text: "Podľa profilu firmy (napríklad IČO) ukáže, na ktoré výzvy máte reálnu šancu — bez prehľadávania desiatok webov.",
  },
  {
    title: "Pomôže napísať žiadosť",
    text: "AI asistent navrhne texty podľa pravidiel výziev a skráti čas, ktorý by ste inak strávili písaním od nuly.",
  },
  {
    title: "Skontroluje environmentálne požiadavky (DNSH)",
    text: "Pred odoslaním overí, či projekt spĺňa povinné „zelené“ kritériá EÚ, a upozorní na riziká.",
  },
  {
    title: "Upozorní na termíny",
    text: "Dostanete signál pri novej výzve, zmene alokácie alebo blížiacom sa termíne uzávierky.",
  },
];

export default async function AboutPage() {
  const apiOnline = await checkApiHealth();

  return (
    <AppShell apiOnline={apiOnline}>
      <article className="mx-auto max-w-3xl space-y-8">
        <header className="animate-fade-up space-y-3">
          <p className="text-xs uppercase tracking-[0.18em] text-muted">O GrantFlow.sk</p>
          <h1 className="font-display text-3xl font-semibold text-white md:text-4xl">
            Dotácie zrozumiteľne — pre firmu, nie pre úrad
          </h1>
          <p className="text-base leading-relaxed text-muted md:text-lg">
            GrantFlow.sk je online nástroj pre slovenské firmy, ktoré chcú získať európske
            alebo štátne dotácie — bez toho, aby museli prečítať stovky stránok príručiek.
          </p>
        </header>

        <section className="animate-fade-up-delay space-y-3 gf-card p-5 md:p-6">
          <h2 className="font-display text-xl font-semibold text-white">
            Na čo slúži?
          </h2>
          <p className="leading-relaxed text-foreground/90">
            Dotácie sú často ťažko pochopiteľné: výzvy sú roztrúsené po viacerých weboch,
            formuláre sú zložité a chyba v žiadosti môže znamenať zamietnutie. GrantFlow
            vám pomôže prejsť celý proces — od nájdenia vhodnej výzvy až po prípravu
            dokumentov.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="font-display text-xl font-semibold text-white">
            Čo vám uľahčí
          </h2>
          <ol className="grid gap-3 sm:grid-cols-2">
            {BENEFITS.map((item, i) => (
              <li
                key={item.title}
                className="gf-card p-4"
              >
                <p className="text-xs font-medium text-accent">
                  {String(i + 1).padStart(2, "0")}
                </p>
                <h3 className="mt-1 font-display text-base font-semibold text-white">
                  {item.title}
                </h3>
                <p className="mt-2 text-sm leading-relaxed text-muted">{item.text}</p>
              </li>
            ))}
          </ol>
        </section>

        <section className="space-y-3 gf-card p-5 md:p-6">
          <h2 className="font-display text-xl font-semibold text-white">
            Pre koho je
          </h2>
          <p className="leading-relaxed text-foreground/90">
            Pre malé a stredné podniky, startupy aj dotačné a účtovné kancelárie, ktoré
            chcú menej papierovania a vyššiu šancu na úspech.
          </p>
        </section>

        <aside className="gf-card-elevated p-5 md:p-6">
          <p className="font-display text-lg font-medium leading-snug text-white">
            Jednou vetou: GrantFlow.sk je digitálny pomocník, ktorý robí európske dotácie
            pre slovenskú firmu zrozumiteľnejšie, rýchlejšie a bezpečnejšie.
          </p>
        </aside>
      </article>
    </AppShell>
  );
}
