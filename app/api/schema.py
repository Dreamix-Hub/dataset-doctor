"""API request and response schemas."""
from typing import Any

from pydantic import BaseModel, Field


class APIFinding(BaseModel):
    type: str
    severity: str
    title: str
    message: str
    column: str | None = None
    columns: list[str] = Field(default_factory=list)
    evidence: dict[str, Any] = Field(default_factory=dict)
    recommendation: str


class APIAIExplanation(BaseModel):
    type: str
    title: str
    severity: str
    explanation: str
    action: str


class APIAnalysis(BaseModel):
    summary: str
    findings: list[APIAIExplanation]
    next_steps: list[str]


class AnalyzeResponse(BaseModel):
    filename: str
    rows: int
    columns: int
    target_column: str | None = None

    status: str = "completed"

    critical_count: int
    warning_count: int
    info_count: int

    findings: list[APIFinding]

    ai_analysis: APIAnalysis