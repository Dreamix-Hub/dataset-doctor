"""Diagnosis result schemas."""
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class Severity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class FindingType(str, Enum):
    MISSING_VALUES = "missing_values"
    DUPLICATES = "duplicates"
    CONSTANT_COLUMN = "constant_column"
    HIGH_CARDINALITY = "high_cardinality"
    OUTLIERS = "outliers"
    CLASS_IMBALANCE = "class_imbalance"
    HIGH_CORRELATION = "high_correlation"
    NEAR_ZERO_VARIANCE = "near_zero_variance"
    SUSPICIOUS_IDENTIFIER = "suspicious_identifier"
    TARGET_ISSUE = "target_issue"


class Finding(BaseModel):
    type: FindingType
    severity: Severity

    title: str
    message: str

    column: str | None = None
    columns: list[str] = Field(default_factory=list)

    evidence: dict[str, Any] = Field(default_factory=dict)

    recommendation: str


class DiagnosisReport(BaseModel):
    filename: str

    rows: int
    columns: int

    target_column: str | None = None

    critical_count: int = 0
    warning_count: int = 0
    info_count: int = 0

    findings: list[Finding] = Field(default_factory=list)