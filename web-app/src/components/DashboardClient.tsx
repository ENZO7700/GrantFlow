"use client";

import { useMemo, useState } from "react";
import {
  type DnshAssessment,
  type DnshStatus,
  runDnshAudit,
} from "@/lib/api";

const DEMO_BRIEF =
  "Zavedenie AI prediktívnej údržby do výroby: fotovoltika 100 kWp na streche haly, batériové úložisko, CNC modernizácia a monitoring spotreby energie v Banskej Bystrici.";

function statusColor(status: DnshStatus) {
  if (status === "PASS") return "text-ok border-ok/40 bg-ok/10";
  if (status === "CONDITIONAL") return "text-warn border-warn/40 bg-warn/10";
  return "text-bad border-bad/40 bg-bad/10";
}

export function DashboardClient({ apiOnline }: { apiOnline: boolean | null }) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [assessment, setAssessment] = useState<DnshAssessment | null>(null);

  const progress = 52;
  const compliance = assessment
    ? assessment.dnsh_passed
      ? 88
      : 42
    : 88;

  const matches = useMemo(
    () => [
      { code: "PSK-SIEA-Inovácie", score: 94 },
      { code: "Horizon STEP Scale", score: 88 },
      { code: "Zelené technológie", score: 81 },
    ],
    [],
  );

  async function onDnshAudit() {
    setBusy(true);
    setError(null);
    try {
      const res = await runDnshAudit({
        project_title: "Zavedenie AI do výroby",
        project_brief: DEMO_BRIEF,
        activities: ["FOVE", "batérie", "CNC", "AI údržba"],
        investment_types: ["fove", "battery", "cnc", "construction"],
        location_nuts3: "SK032",
      });
      setAssessment(res.assessment);
    } catch (e) {
      setError(e instanceof Error ? e.message : "DNSH audit zlyhal");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="space-y-6">
      <section className="animate-fade-up rounded-2xl border border-line bg-panel-2/80 p-5 md:p-6">
        <p className="text-xs uppercase tracking-[0.18em] text-muted">Profil spoločnosti</p>
        <h1 className="mt-1 font-display text-2xl font-semibold text-white md:text-3xl">
          InnoTech Slovakia s.r.o.
        </h1>
        <p className="mt-2 text-sm text-muted">
          IČO: 52 123 456 · Malý podnik (24 zamestnancov) · Banskobystrický kraj · NACE: 62.01
        </p>
      </section>

      <div className="grid gap-4 md:grid-cols-2">
        <section
          id="vyzvy"
          className="animate-fade-up-delay rounded-2xl border border-line bg-panel/80 p-5"
        >
          <h2 className="font-display text-lg font-semibold text-white">
            3 nové top zhody pre vás
          </h2>
          <ul className="mt-4 space-y-3">
            {matches.map((m) => (
              <li
                key={m.code}
                className="flex items-center justify-between gap-3 border-b border-line/60 pb-3 last:border-0"
              >
                <span className="text-sm text-foreground">{m.code}</span>
                <span className="rounded-full bg-accent/15 px-2.5 py-1 text-xs font-medium text-sky-300">
                  Zhoda {m.score}%
                </span>
              </li>
            ))}
          </ul>
        </section>

        <section className="animate-fade-up-delay rounded-2xl border border-line bg-panel/80 p-5">
          <h2 className="font-display text-lg font-semibold text-white">
            Blížiace sa uzávierky
          </h2>
          <ul className="mt-4 space-y-3 text-sm">
            <li className="flex justify-between gap-3 border-b border-line/60 pb-3">
              <span>Digitálny Reštart</span>
              <span className="text-warn">za 14 dní</span>
            </li>
            <li className="flex justify-between gap-3">
              <span>EIC Accelerator</span>
              <span className="text-muted">za 32 dní</span>
            </li>
          </ul>
        </section>
      </div>

      <section
        id="ziadosti"
        className="animate-fade-up rounded-2xl border border-accent/30 bg-gradient-to-br from-panel to-panel-2 p-5 md:p-6"
      >
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div>
            <p className="text-xs uppercase tracking-[0.16em] text-sky-300/90">Rozpracovaný projekt</p>
            <h2 className="mt-1 font-display text-xl font-semibold text-white">
              Zavedenie AI do výroby
            </h2>
            <p className="mt-1 text-sm text-muted">Výzva: PSK-SIEA-004</p>
          </div>
          <div className="text-right">
            <p className="text-xs text-muted">AI Compliance Skóre</p>
            <p className="font-display text-2xl font-semibold text-white">
              {compliance}
              <span className="text-base text-muted">/100</span>
            </p>
          </div>
        </div>

        <div className="mt-5">
          <div className="mb-1 flex justify-between text-xs text-muted">
            <span>Progres</span>
            <span>{progress}%</span>
          </div>
          <div className="h-2 overflow-hidden rounded-full bg-line/80">
            <div
              className="h-full rounded-full bg-accent transition-all duration-700"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>

        <div className="mt-5 flex flex-wrap gap-3">
          <button
            type="button"
            className="rounded-xl border border-line bg-background/40 px-4 py-2.5 text-sm font-medium text-foreground hover:border-accent/50"
            onClick={() =>
              alert(
                "Proposal Drafter (Agent 3) príde v ďalšom kroku — zatiaľ použite DNSH Audit.",
              )
            }
          >
            Pokračovať v písaní s AI
          </button>
          <button
            type="button"
            disabled={busy || apiOnline === false}
            onClick={onDnshAudit}
            className="rounded-xl bg-accent px-4 py-2.5 text-sm font-semibold text-white shadow-lg shadow-accent/20 hover:bg-accent-soft disabled:cursor-not-allowed disabled:opacity-50"
          >
            {busy ? "Prebieha DNSH audit…" : "Spustiť DNSH Audit"}
          </button>
          <button
            type="button"
            className="rounded-xl border border-line px-4 py-2.5 text-sm text-muted hover:text-foreground"
            onClick={() => alert("ITMS2021+ export — plánované (US 6.2)")}
          >
            Exportovať do ITMS2021+
          </button>
        </div>

        {apiOnline === false && (
          <p className="mt-3 text-sm text-bad">
            AI API nie je dostupné. Spustite{" "}
            <code className="text-sky-300">uvicorn</code> na porte 8001.
          </p>
        )}
        {error && <p className="mt-3 text-sm text-bad">{error}</p>}
      </section>

      {assessment && (
        <section className="animate-fade-up rounded-2xl border border-line bg-panel/90 p-5 md:p-6">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <h2 className="font-display text-lg font-semibold text-white">
              DNSH Audit — 6 cieľov
            </h2>
            <span
              className={`rounded-full border px-3 py-1 text-xs font-semibold ${statusColor(
                assessment.overall_status,
              )}`}
            >
              {assessment.overall_status}
              {assessment.dnsh_passed ? " · passed" : " · blocked"}
            </span>
          </div>
          <p className="mt-2 text-xs text-muted">
            Grounding {assessment.grounding_score.toFixed(2)} · {assessment.model_name}
          </p>
          <div className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {assessment.findings.map((f) => (
              <article
                key={f.objective_code}
                className="rounded-xl border border-line bg-background/35 p-3"
              >
                <div className="flex items-start justify-between gap-2">
                  <h3 className="text-sm font-medium text-foreground">{f.objective_name_sk}</h3>
                  <span className={`shrink-0 rounded-md border px-1.5 py-0.5 text-[10px] ${statusColor(f.status)}`}>
                    {f.status}
                  </span>
                </div>
                <p className="mt-2 line-clamp-3 text-xs text-muted">{f.rationale}</p>
                {f.mitigations.length > 0 && (
                  <ul className="mt-2 space-y-1 text-xs text-sky-200/90">
                    {f.mitigations.slice(0, 2).map((m) => (
                      <li key={m}>• {m}</li>
                    ))}
                  </ul>
                )}
              </article>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
