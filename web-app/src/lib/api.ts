export type DnshStatus = "PASS" | "CONDITIONAL" | "FAIL";

export type DnshFinding = {
  objective_code: string;
  objective_name_sk: string;
  status: DnshStatus;
  severity?: string | null;
  rationale: string;
  risk_signals: string[];
  mitigations: string[];
  suggested_self_assessment_text?: string;
};

export type DnshAssessment = {
  assessment_id: string;
  overall_status: DnshStatus;
  dnsh_passed: boolean;
  findings: DnshFinding[];
  grounding_score: number;
  model_name: string;
};

export type DnshAuditResponse = {
  ok: boolean;
  assessment: DnshAssessment;
  report_blob_url?: string;
};

const API_URL =
  process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "") || "http://127.0.0.1:8001";

export function getApiBaseUrl() {
  return API_URL;
}

export async function runDnshAudit(input: {
  project_title: string;
  project_brief: string;
  activities?: string[];
  investment_types?: string[];
  location_nuts3?: string;
}): Promise<DnshAuditResponse> {
  const res = await fetch(`${API_URL}/v1/dnsh/audit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      project_title: input.project_title,
      project_brief: input.project_brief,
      activities: input.activities ?? [],
      investment_types: input.investment_types ?? [],
      location_nuts3: input.location_nuts3,
    }),
  });

  if (!res.ok) {
    const detail = await res.text();
    throw new Error(`DNSH API ${res.status}: ${detail.slice(0, 240)}`);
  }

  return res.json();
}

export async function checkApiHealth(): Promise<boolean> {
  try {
    const res = await fetch(`${API_URL}/health`, { cache: "no-store" });
    if (!res.ok) return false;
    const data = await res.json();
    return data.status === "ok";
  } catch {
    return false;
  }
}
