"""Citation / grounding gate (Blueprint §3.3)."""

from __future__ import annotations

from app.config import settings
from app.models.schemas import Citation


def score_grounding(claims: list[str], citations: list[Citation]) -> float:
    """Lightweight stub: score rises with citations and claim coverage.

    Production: replace with NLI / entailment against retrieved chunks.
    """
    if not claims:
        return 1.0
    if not citations:
        return 0.0
    # Heuristic: each citation covers one claim up to 1.0
    return min(1.0, len(citations) / max(1, len(claims)))


def passes_grounding(score: float, threshold: float | None = None) -> bool:
    thr = threshold if threshold is not None else settings.grounding_threshold
    return score >= thr
