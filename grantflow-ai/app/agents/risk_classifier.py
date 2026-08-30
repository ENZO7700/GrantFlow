"""Deterministic activity risk classifier (no LLM)."""

from __future__ import annotations

import re

from app.models.schemas import ObjectiveCode

# Keyword → risk signals mapped to DNSH objectives (Blueprint §3.5)
SIGNAL_PATTERNS: list[tuple[str, str, list[ObjectiveCode]]] = [
    (r"diesel|fosíl|spaľovan|plynov\w* kotol", "fossil_fuel", [ObjectiveCode.CLIMATE_MITIGATION, ObjectiveCode.POLLUTION]),
    (r"fove|fotovolt|pv\b|solár", "fove", [ObjectiveCode.CLIMATE_MITIGATION, ObjectiveCode.CLIMATE_ADAPTATION]),
    (r"batéri|battery|úložisk", "battery_storage", [ObjectiveCode.CLIMATE_MITIGATION, ObjectiveCode.CIRCULAR]),
    (r"hala|výstavb|stavebn|greenfield|nová budov", "construction", [ObjectiveCode.CLIMATE_ADAPTATION, ObjectiveCode.BIODIVERSITY, ObjectiveCode.POLLUTION]),
    (r"záplav|povodň|flood", "flood_zone", [ObjectiveCode.CLIMATE_ADAPTATION]),
    (r"odpadov\w* vod|chemik|chladiac|čistenie povrch", "water_process", [ObjectiveCode.WATER, ObjectiveCode.POLLUTION]),
    (r"cnc|robot|stroj|výrobn\w* link", "machinery", [ObjectiveCode.CIRCULAR, ObjectiveCode.CLIMATE_MITIGATION]),
    (r"it\b|server|hardvér|notebook|počítač", "it_hw", [ObjectiveCode.CIRCULAR]),
    (r"lakov|zváran|farby|reach|nebezpečn", "polluting_process", [ObjectiveCode.POLLUTION]),
    (r"natura|biotop|chránen|odlesn|orn\w* pôd", "biodiversity_pressure", [ObjectiveCode.BIODIVERSITY]),
]


def classify_risks(text: str, investment_types: list[str] | None = None) -> dict[ObjectiveCode, list[str]]:
    """Return risk signals per DNSH objective from free text + typed tags."""
    blob = (text or "").lower()
    if investment_types:
        blob += " " + " ".join(investment_types).lower()

    per_obj: dict[ObjectiveCode, list[str]] = {o: [] for o in ObjectiveCode}

    for pattern, signal, objectives in SIGNAL_PATTERNS:
        if re.search(pattern, blob, flags=re.IGNORECASE):
            for obj in objectives:
                if signal not in per_obj[obj]:
                    per_obj[obj].append(signal)

    return per_obj
