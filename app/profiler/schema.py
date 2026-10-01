"""Dataset schema definitions."""
from typing import Any

from pydantic import BaseModel, Field


class ColumnProfile(BaseModel):
    name: str
    data_type: str
    inferred_type: str

    total_values: int

    missing_values: int
    missing_percentage: float

    unique_values: int
    unique_percentage: float

    is_constant: bool
    is_high_cardinality: bool

    statistics: dict[str, Any] = Field(default_factory=dict)


class DatasetProfile(BaseModel):
    filename: str

    rows: int
    columns: int

    memory_usage_mb: float

    numerical_columns: list[str]
    categorical_columns: list[str]
    datetime_columns: list[str]

    duplicate_rows: int
    duplicate_percentage: float

    column_profiles: list[ColumnProfile]

    warnings: list[str] = Field(default_factory=list)