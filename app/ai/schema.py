from enum import Enum

from pydantic import BaseModel


class AISeverity(str, Enum):
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"


class Confidence(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class FindingExplanation(BaseModel):
    explanation: str
    action: str


class AIFinding(BaseModel):
    type: str
    title: str
    severity: str
    explanation: str
    action: str


class AIAnalysis(BaseModel):
    summary: str
    findings: list[AIFinding]
    next_steps: list[str]