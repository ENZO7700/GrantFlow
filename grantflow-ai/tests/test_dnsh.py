"""Unit tests for DNSH aggregation and risk classifier."""

from app.agents.dnsh_graph import run_dnsh_audit
from app.agents.risk_classifier import classify_risks
from app.models.schemas import DnshAuditRequest, DnshStatus, ObjectiveCode


def test_classify_fove_battery():
    risks = classify_risks("Inštalácia fotovoltiky a batériového úložiska na hale")
    assert "fove" in risks[ObjectiveCode.CLIMATE_MITIGATION]
    assert "battery_storage" in risks[ObjectiveCode.CIRCULAR]


def test_dnsh_audit_fove_project():
    req = DnshAuditRequest(
        project_title="FOVE na streche haly",
        project_brief=(
            "Chceme nainštalovať fotovoltickú elektráreň 100 kWp na strechu výrobnej haly "
            "v Banskej Bystrici vrátane batériového úložiska."
        ),
        activities=["montáž FOVE", "batérie", "smart metering"],
        investment_types=["fove", "battery"],
        location_nuts3="SK032",
    )
    result = run_dnsh_audit(req)
    assert result["ok"] is True
    assessment = result["assessment"]
    assert assessment["dnsh_passed"] is True
    assert len(assessment["findings"]) == 6
    codes = {f["objective_code"] for f in assessment["findings"]}
    assert codes == {o.value for o in ObjectiveCode}


def test_dnsh_fossil_without_oze_fails_mitigation_objective():
    req = DnshAuditRequest(
        project_title="Nový diesel generátor",
        project_brief=(
            "Rozšírenie kapacity o diesel generátor pre záložné spaľovanie fosílnych palív "
            "bez opatrení energetickej účinnosti."
        ),
        activities=["diesel backup"],
        investment_types=["diesel"],
    )
    result = run_dnsh_audit(req)
    assert result["ok"] is True
    assessment = result["assessment"]
    assert assessment["overall_status"] == DnshStatus.FAIL.value
    assert assessment["dnsh_passed"] is False
