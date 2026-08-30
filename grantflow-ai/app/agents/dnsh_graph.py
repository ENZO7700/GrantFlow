"""LangGraph DNSH Auditor — Agent 2 (Blueprint §3.2 / §3.5).

Flow: classify → retrieve → evaluate_6_objectives → ground → aggregate → persist
"""

from __future__ import annotations

from typing import Any, TypedDict

from langgraph.graph import END, StateGraph

from app.agents.grounding import passes_grounding, score_grounding
from app.agents.risk_classifier import classify_risks
from app.config import settings
from app.models.schemas import (
    OBJECTIVE_LABELS_SK,
    DnshAssessment,
    DnshAuditRequest,
    DnshFinding,
    DnshStatus,
    ObjectiveCode,
    Severity,
)
from app.services.persist_stub import persist_assessment
from app.services.retrieve_stub import chunks_to_citations, retrieve_dnsh_guidance


class DnshState(TypedDict, total=False):
    request: dict[str, Any]
    risks: dict[str, list[str]]
    findings: list[dict[str, Any]]
    grounding_score: float
    overall_status: str
    dnsh_passed: bool
    assessment: dict[str, Any]
    report_blob_url: str
    error: str


STATUS_RANK = {DnshStatus.PASS: 0, DnshStatus.CONDITIONAL: 1, DnshStatus.FAIL: 2}


def _decide_status(signals: list[str], objective: ObjectiveCode) -> tuple[DnshStatus, Severity | None, list[str]]:
    """Heuristic status from risk signals — replaceable by LLM structured output."""
    if not signals:
        return DnshStatus.PASS, None, []

    mitigations: list[str] = []
    status = DnshStatus.CONDITIONAL
    severity = Severity.MEDIUM

    hard_fail = {
        ObjectiveCode.CLIMATE_MITIGATION: {"fossil_fuel"},
        ObjectiveCode.BIODIVERSITY: {"biodiversity_pressure"},
        ObjectiveCode.WATER: set(),
        ObjectiveCode.CIRCULAR: set(),
        ObjectiveCode.POLLUTION: set(),
        ObjectiveCode.CLIMATE_ADAPTATION: set(),
    }

    if hard_fail.get(objective, set()) & set(signals) and objective == ObjectiveCode.CLIMATE_MITIGATION:
        # Fossil expansion without mitigation narrative → FAIL in stub
        if "fossil_fuel" in signals and "fove" not in signals:
            return (
                DnshStatus.FAIL,
                Severity.HIGH,
                ["Nahradiť fosílny zdroj OZE / účinnosťou a vyčísliť emisie t CO2e/rok"],
            )

    if "battery_storage" in signals:
        mitigations.append("Popísať recykláciu batérií na konci životnosti podľa zákona o odpadoch")
        mitigations.append("Uviesť predpokladanú úsporu t CO2e/rok")
    if "fove" in signals:
        mitigations.append("Zdôvodniť kotvenie a odolnosť voči extrémnemu vetru (adaptácia)")
    if "construction" in signals:
        mitigations.append("Overiť klimatické riziká lokality a energetický štandard budovy")
    if "flood_zone" in signals:
        status = DnshStatus.CONDITIONAL
        severity = Severity.HIGH
        mitigations.append("Doplniť flood-resilience opatrenia a poisťovacie / technické bariéry")
    if "water_process" in signals:
        mitigations.append("Navrhnúť monitoring vôd / ČOV a chemický manažment")
    if "machinery" in signals or "it_hw" in signals:
        mitigations.append("Doplniť EoL / WEEE plán pre technológie")
    if "polluting_process" in signals:
        mitigations.append("Uviesť BAT, odsávanie a platné environmentálne povolenia")
    if "biodiversity_pressure" in signals:
        status = DnshStatus.CONDITIONAL
        severity = Severity.HIGH
        mitigations.append("Zabezpečiť stanovisko / EIA voči NATURA 2000 a biotopom")

    if not mitigations:
        mitigations.append("Doplniť krátke DNSH zdôvodnenie voči tomuto cieľu podľa usmernenia RO")

    return status, severity, mitigations


def node_classify(state: DnshState) -> DnshState:
    req = DnshAuditRequest.model_validate(state["request"])
    text = " ".join([req.project_brief, *req.activities])
    risks = classify_risks(text, req.investment_types)
    return {"risks": {k.value: v for k, v in risks.items()}}


def node_evaluate(state: DnshState) -> DnshState:
    req = DnshAuditRequest.model_validate(state["request"])
    risks_raw = state.get("risks", {})
    findings: list[DnshFinding] = []
    claim_texts: list[str] = []
    all_citations = []

    for objective in ObjectiveCode:
        signals = risks_raw.get(objective.value, [])
        chunks = retrieve_dnsh_guidance(objective, req.project_brief)
        citations = chunks_to_citations(chunks)
        all_citations.extend(citations)

        status, severity, mitigations = _decide_status(signals, objective)
        rationale = (
            f"Signály: {', '.join(signals) if signals else 'žiadne kritické'}. "
            f"Kontext metodiky: {chunks[0].content if chunks else 'nedostupný'}."
        )
        claim_texts.append(rationale)

        suggested = (
            f"Projekt „{req.project_title}“ voči cieľu „{OBJECTIVE_LABELS_SK[objective]}“ "
            f"vyhodnocujeme ako {status.value}. "
            + (" ".join(mitigations) if mitigations else "Významné poškodenie sa neočakáva.")
        )

        findings.append(
            DnshFinding(
                objective_code=objective,
                objective_name_sk=OBJECTIVE_LABELS_SK[objective],
                status=status,
                severity=severity,
                rationale=rationale,
                risk_signals=signals,
                mitigations=mitigations if status != DnshStatus.PASS else [],
                suggested_self_assessment_text=suggested,
                citations=citations,
            )
        )

    g_score = score_grounding(claim_texts, all_citations)
    return {
        "findings": [f.model_dump(mode="json") for f in findings],
        "grounding_score": g_score,
    }


def node_ground_or_refuse(state: DnshState) -> DnshState:
    score = float(state.get("grounding_score", 0.0))
    if not passes_grounding(score):
        return {
            "error": (
                f"Grounding score {score:.2f} < {settings.grounding_threshold}. "
                "V dostupnej metodike nie je dostatok podkladov — doplňte dokumenty výzvy."
            )
        }
    return {}


def node_aggregate(state: DnshState) -> DnshState:
    if state.get("error"):
        return {}

    findings = [DnshFinding.model_validate(f) for f in state.get("findings", [])]
    worst = DnshStatus.PASS
    for f in findings:
        if STATUS_RANK[f.status] > STATUS_RANK[worst]:
            worst = f.status

    # dnsh_passed only if no FAIL (CONDITIONAL allowed if mitigations present — stub accepts)
    dnsh_passed = worst != DnshStatus.FAIL
    return {"overall_status": worst.value, "dnsh_passed": dnsh_passed}


def node_persist(state: DnshState) -> DnshState:
    if state.get("error"):
        return {}

    req = DnshAuditRequest.model_validate(state["request"])
    findings = [DnshFinding.model_validate(f) for f in state.get("findings", [])]
    assessment = DnshAssessment(
        application_id=req.application_id,
        overall_status=DnshStatus(state["overall_status"]),
        dnsh_passed=bool(state["dnsh_passed"]),
        findings=findings,
        grounding_score=float(state.get("grounding_score", 0.0)),
        model_name=f"stub-dnsh@{settings.llm_mode}",
        report={
            "project_title": req.project_title,
            "objectives": [f.objective_code.value for f in findings],
        },
    )
    blob = persist_assessment(assessment)
    return {"assessment": assessment.model_dump(mode="json"), "report_blob_url": blob}


def build_dnsh_graph():
    g = StateGraph(DnshState)
    g.add_node("classify", node_classify)
    g.add_node("evaluate", node_evaluate)
    g.add_node("ground", node_ground_or_refuse)
    g.add_node("aggregate", node_aggregate)
    g.add_node("persist", node_persist)

    g.set_entry_point("classify")
    g.add_edge("classify", "evaluate")
    g.add_edge("evaluate", "ground")
    g.add_edge("ground", "aggregate")
    g.add_edge("aggregate", "persist")
    g.add_edge("persist", END)
    return g.compile()


_GRAPH = None


def get_dnsh_graph():
    global _GRAPH
    if _GRAPH is None:
        _GRAPH = build_dnsh_graph()
    return _GRAPH


def run_dnsh_audit(request: DnshAuditRequest) -> dict[str, Any]:
    graph = get_dnsh_graph()
    result = graph.invoke({"request": request.model_dump(mode="json")})
    if result.get("error"):
        return {"ok": False, "error": result["error"], "grounding_score": result.get("grounding_score")}
    return {
        "ok": True,
        "assessment": result.get("assessment"),
        "report_blob_url": result.get("report_blob_url"),
    }
