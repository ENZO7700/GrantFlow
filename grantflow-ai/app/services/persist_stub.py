"""Persistence stub for dnsh_assessments / dnsh_findings (Blueprint §5)."""

from __future__ import annotations

import json
from pathlib import Path

from app.models.schemas import DnshAssessment

_STORE = Path(__file__).resolve().parents[2] / ".data" / "dnsh_assessments.jsonl"


def persist_assessment(assessment: DnshAssessment) -> str:
    """Append assessment JSON to local jsonl store. Returns logical blob URL."""
    _STORE.parent.mkdir(parents=True, exist_ok=True)
    with _STORE.open("a", encoding="utf-8") as f:
        f.write(assessment.model_dump_json() + "\n")
    return f"file://{_STORE.as_posix()}#{assessment.assessment_id}"


def load_recent(limit: int = 20) -> list[dict]:
    if not _STORE.exists():
        return []
    lines = _STORE.read_text(encoding="utf-8").strip().splitlines()
    out: list[dict] = []
    for line in lines[-limit:]:
        out.append(json.loads(line))
    return out
