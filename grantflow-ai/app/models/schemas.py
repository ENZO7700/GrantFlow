"""Pydantic schemas aligned with Blueprint §3.5 / §5."""

from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class DnshStatus(str, Enum):
    PASS = "PASS"
    CONDITIONAL = "CONDITIONAL"
    FAIL = "FAIL"


class Severity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class ObjectiveCode(str, Enum):
    CLIMATE_MITIGATION = "CLIMATE_MITIGATION"
    CLIMATE_ADAPTATION = "CLIMATE_ADAPTATION"
    WATER = "WATER"
    CIRCULAR = "CIRCULAR"
    POLLUTION = "POLLUTION"
    BIODIVERSITY = "BIODIVERSITY"


OBJECTIVE_LABELS_SK: dict[ObjectiveCode, str] = {
    ObjectiveCode.CLIMATE_MITIGATION: "Zmierňovanie zmeny klímy",
    ObjectiveCode.CLIMATE_ADAPTATION: "Adaptácia na zmenu klímy",
    ObjectiveCode.WATER: "Ochrana vodných zdrojov",
    ObjectiveCode.CIRCULAR: "Prechod na obehové hospodárstvo",
    ObjectiveCode.POLLUTION: "Prevencia a kontrola znečisťovania",
    ObjectiveCode.BIODIVERSITY: "Ochrana biodiverzity a ekosystémov",
}


class Citation(BaseModel):
    chunk_id: str
    document: str | None = None
    page: int | None = None
    quote: str | None = None


class DnshFinding(BaseModel):
    objective_code: ObjectiveCode
    objective_name_sk: str
    status: DnshStatus
    severity: Severity | None = None
    rationale: str
    risk_signals: list[str] = Field(default_factory=list)
    mitigations: list[str] = Field(default_factory=list)
    suggested_self_assessment_text: str = ""
    citations: list[Citation] = Field(default_factory=list)


class DnshAuditRequest(BaseModel):
    application_id: UUID | None = None
    organization_id: UUID | None = None
    grant_call_id: UUID | None = None
    project_title: str
    project_brief: str = Field(..., min_length=20, description="Opis zámeru a aktivít")
    activities: list[str] = Field(default_factory=list)
    location_nuts3: str | None = None
    investment_types: list[str] = Field(
        default_factory=list,
        description="napr. fove, battery, cnc, construction, it_hw, chemicals",
    )


class DnshAssessment(BaseModel):
    assessment_id: UUID = Field(default_factory=uuid4)
    application_id: UUID | None = None
    overall_status: DnshStatus
    dnsh_passed: bool
    findings: list[DnshFinding]
    grounding_score: float
    model_name: str
    report: dict[str, Any] = Field(default_factory=dict)
