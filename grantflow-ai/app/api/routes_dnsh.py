"""DNSH HTTP API."""

from fastapi import APIRouter, HTTPException

from app.agents.dnsh_graph import run_dnsh_audit
from app.models.schemas import DnshAssessment, DnshAuditRequest
from app.services.persist_stub import load_recent

router = APIRouter()


@router.post("/audit", response_model=dict)
def audit(request: DnshAuditRequest) -> dict:
    """Spustí Agent 2 — DNSH Audit (6 cieľov EÚ taxonómie)."""
    result = run_dnsh_audit(request)
    if not result.get("ok"):
        raise HTTPException(status_code=422, detail=result.get("error", "Grounding failed"))
    return result


@router.get("/assessments/recent")
def recent_assessments(limit: int = 20) -> list[dict]:
    return load_recent(limit=limit)


@router.post("/audit/preview", response_model=DnshAssessment)
def audit_preview(request: DnshAuditRequest) -> DnshAssessment:
    """Audit + typed response model for OpenAPI clients."""
    result = run_dnsh_audit(request)
    if not result.get("ok"):
        raise HTTPException(status_code=422, detail=result.get("error", "Grounding failed"))
    return DnshAssessment.model_validate(result["assessment"])
