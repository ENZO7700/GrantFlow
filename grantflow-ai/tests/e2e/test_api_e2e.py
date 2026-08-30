"""
E2E tests for GrantFlow AI API.

Default: in-process ASGI (no uvicorn needed).
Optional live server: set GRANTFLOW_E2E_LIVE=1 (expects :8001).

  pytest tests/e2e -m e2e -q
"""

from __future__ import annotations

import os
from collections.abc import Iterator

import httpx
import pytest
from fastapi.testclient import TestClient

from app.main import app

BASE_URL = os.getenv("GRANTFLOW_API_URL", "http://127.0.0.1:8001")
LIVE = os.getenv("GRANTFLOW_E2E_LIVE", "").strip() in {"1", "true", "yes"}
TIMEOUT = 30.0

pytestmark = pytest.mark.e2e


@pytest.fixture(scope="session")
def client() -> Iterator[httpx.Client | TestClient]:
    if LIVE:
        with httpx.Client(base_url=BASE_URL, timeout=TIMEOUT, follow_redirects=False) as c:
            try:
                r = c.get("/health")
            except httpx.ConnectError as exc:
                pytest.skip(f"Live API nie je dostupná na {BASE_URL}: {exc}")
            if r.status_code != 200:
                pytest.skip(f"Health check zlyhal: {r.status_code}")
            yield c
        return

    with TestClient(app, raise_server_exceptions=True) as c:
        # staršie starlette: follow_redirects; novšie: follow_redirects via request
        yield c


def test_health_ok(client: httpx.Client | TestClient) -> None:
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["service"] == "grantflow-ai"
    assert "mode" in body


def test_root_redirects_to_docs(client: httpx.Client | TestClient) -> None:
    r = client.get("/", follow_redirects=False)
    assert r.status_code in (301, 302, 307, 308)
    assert "/docs" in r.headers.get("location", "")


def test_openapi_and_docs(client: httpx.Client) -> None:
    docs = client.get("/docs")
    assert docs.status_code == 200
    assert "text/html" in docs.headers.get("content-type", "")

    openapi = client.get("/openapi.json")
    assert openapi.status_code == 200
    spec = openapi.json()
    assert "paths" in spec
    assert "/v1/dnsh/audit" in spec["paths"]
    assert "/health" in spec["paths"]


def test_dnsh_audit_get_method_not_allowed(client: httpx.Client) -> None:
    r = client.get("/v1/dnsh/audit")
    assert r.status_code == 405


def test_dnsh_audit_validation_error(client: httpx.Client) -> None:
    r = client.post("/v1/dnsh/audit", json={"project_title": "X", "project_brief": "too short"})
    assert r.status_code == 422


def test_dnsh_audit_fove_e2e(client: httpx.Client) -> None:
    payload = {
        "project_title": "FOVE E2E test",
        "project_brief": (
            "Inštalácia fotovoltickej elektrárne 120 kWp na strechu výrobnej haly "
            "v Banskej Bystrici vrátane batériového úložiska a merania spotreby."
        ),
        "activities": ["montáž FOVE", "batérie", "smart metering"],
        "investment_types": ["fove", "battery"],
        "location_nuts3": "SK032",
    }
    r = client.post("/v1/dnsh/audit", json=payload)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["ok"] is True
    assessment = data["assessment"]
    assert assessment["dnsh_passed"] is True
    assert len(assessment["findings"]) == 6
    codes = {f["objective_code"] for f in assessment["findings"]}
    assert codes == {
        "CLIMATE_MITIGATION",
        "CLIMATE_ADAPTATION",
        "WATER",
        "CIRCULAR",
        "POLLUTION",
        "BIODIVERSITY",
    }
    assert assessment["grounding_score"] >= 0.72
    assert data.get("report_blob_url")


def test_dnsh_audit_diesel_fails_e2e(client: httpx.Client) -> None:
    payload = {
        "project_title": "Diesel E2E",
        "project_brief": (
            "Rozšírenie kapacity o diesel generátor pre záložné spaľovanie fosílnych palív "
            "bez opatrení energetickej účinnosti a bez OZE."
        ),
        "activities": ["diesel backup"],
        "investment_types": ["diesel"],
    }
    r = client.post("/v1/dnsh/audit", json=payload)
    assert r.status_code == 200, r.text
    assessment = r.json()["assessment"]
    assert assessment["overall_status"] == "FAIL"
    assert assessment["dnsh_passed"] is False
    mitigation = next(
        f for f in assessment["findings"] if f["objective_code"] == "CLIMATE_MITIGATION"
    )
    assert mitigation["status"] == "FAIL"


def test_dnsh_audit_preview_typed(client: httpx.Client) -> None:
    payload = {
        "project_title": "Preview E2E CNC",
        "project_brief": (
            "Nákup CNC stroja a robotickej linky pre MSP s plánom EoL recyklácie "
            "a meraním spotreby energie vo výrobnej hale."
        ),
        "activities": ["CNC", "robot"],
        "investment_types": ["cnc"],
    }
    r = client.post("/v1/dnsh/audit/preview", json=payload)
    assert r.status_code == 200, r.text
    body = r.json()
    assert "assessment_id" in body
    assert "findings" in body
    assert len(body["findings"]) == 6


def test_dnsh_recent_assessments(client: httpx.Client) -> None:
    client.post(
        "/v1/dnsh/audit",
        json={
            "project_title": "Seed recent",
            "project_brief": "Fotovoltika na streche skladu pre úsporu energie a meranie CO2.",
            "investment_types": ["fove"],
        },
    )
    r = client.get("/v1/dnsh/assessments/recent", params={"limit": 5})
    assert r.status_code == 200
    items = r.json()
    assert isinstance(items, list)
    assert len(items) >= 1
    assert "overall_status" in items[-1] or "findings" in items[-1]


def test_full_user_journey_e2e(client: httpx.Client) -> None:
    """Simulácia UI flow: health → docs → audit → recent."""
    assert client.get("/health").json()["status"] == "ok"
    assert client.get("/docs").status_code == 200

    audit = client.post(
        "/v1/dnsh/audit",
        json={
            "project_title": "Journey FOVE + výstavba",
            "project_brief": (
                "Greenfield výstavba malej haly s fotovoltikou na streche, "
                "batériovým úložiskom a monitoringom spotreby v Trenčíne."
            ),
            "activities": ["výstavba haly", "FOVE", "batérie"],
            "investment_types": ["construction", "fove", "battery"],
            "location_nuts3": "SK022",
        },
    )
    assert audit.status_code == 200
    assessment = audit.json()["assessment"]
    assert len(assessment["findings"]) == 6
    flagged = [f for f in assessment["findings"] if f["status"] != "PASS"]
    assert flagged, "očakávané riziká pri greenfield + batérie"

    recent = client.get("/v1/dnsh/assessments/recent?limit=10")
    assert recent.status_code == 200
    assert any(item.get("overall_status") or item.get("findings") for item in recent.json())


def test_favicon_served(client: httpx.Client) -> None:
    r = client.get("/favicon.ico")
    assert r.status_code == 200
    assert len(r.content) > 100
