"""Hybrid retrieve stub — replace with pgvector + BM25 + RRF."""

from __future__ import annotations

from dataclasses import dataclass

from app.models.schemas import Citation, ObjectiveCode


@dataclass
class RetrievedChunk:
    chunk_id: str
    document: str
    page: int
    content: str
    score: float


# Minimal offline knowledge base for stub mode (SK DNSH guidance snippets)
_STUB_KB: dict[ObjectiveCode, list[RetrievedChunk]] = {
    ObjectiveCode.CLIMATE_MITIGATION: [
        RetrievedChunk(
            "stub-cm-1",
            "DNSH usmernenie RO — Zmierňovanie klímy",
            7,
            "Projekt nesmie významne zvyšovať emisie GHG. OZE a energetická účinnosť majú byť kvantifikované (t CO2e/rok).",
            0.91,
        )
    ],
    ObjectiveCode.CLIMATE_ADAPTATION: [
        RetrievedChunk(
            "stub-ca-1",
            "DNSH usmernenie RO — Adaptácia",
            12,
            "Investície majú zohľadniť klimatické riziká lokality (povodne, sucho, extrémny vietor) a navrhnúť adaptation opatrenia.",
            0.88,
        )
    ],
    ObjectiveCode.WATER: [
        RetrievedChunk(
            "stub-w-1",
            "DNSH usmernenie RO — Vody",
            18,
            "Aktivity nesmú významne zhoršovať kvalitu ani množstvo povrchových a podzemných vôd; vyžaduje sa monitoring / ČOV podľa potreby.",
            0.86,
        )
    ],
    ObjectiveCode.CIRCULAR: [
        RetrievedChunk(
            "stub-c-1",
            "DNSH usmernenie RO — Obehové hospodárstvo",
            22,
            "Odpad z projektu má nasledovať hierarchiu odpadového hospodárstva; EoL batérií a WEEE musia byť popísané.",
            0.9,
        )
    ],
    ObjectiveCode.POLLUTION: [
        RetrievedChunk(
            "stub-p-1",
            "DNSH usmernenie RO — Znečisťovanie",
            27,
            "Emisie do ovzdušia, hluk a nebezpečné látky majú byť riadené BAT a platnými povoleniami.",
            0.87,
        )
    ],
    ObjectiveCode.BIODIVERSITY: [
        RetrievedChunk(
            "stub-b-1",
            "DNSH usmernenie RO — Biodiverzita",
            31,
            "Greenfield a zásahy do NATURA 2000 / biotopov vyžadujú stanovisko / EIA; významné poškodenie je FAIL.",
            0.89,
        )
    ],
}


def retrieve_dnsh_guidance(objective: ObjectiveCode, query: str, top_k: int = 3) -> list[RetrievedChunk]:
    _ = query  # unused in stub
    return _STUB_KB.get(objective, [])[:top_k]


def chunks_to_citations(chunks: list[RetrievedChunk]) -> list[Citation]:
    return [
        Citation(
            chunk_id=c.chunk_id,
            document=c.document,
            page=c.page,
            quote=c.content[:180],
        )
        for c in chunks
    ]
