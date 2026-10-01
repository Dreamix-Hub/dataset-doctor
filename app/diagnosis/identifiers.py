"""Identifier diagnosis checks."""
import pandas as pd

from app.diagnosis.schema import (
    Finding,
    FindingType,
    Severity,
)


ID_NAME_PATTERNS = (
    "id",
    "_id",
    "id_",
    "uuid",
    "identifier",
    "customer_number",
    "customer_no",
    "user_number",
    "user_no",
)


def looks_like_id_name(column_name: str) -> bool:
    normalized = column_name.lower().strip()

    if normalized == "id":
        return True

    return any(
        pattern in normalized
        for pattern in ID_NAME_PATTERNS
    )


def detect_suspicious_identifiers(
    dataframe: pd.DataFrame,
) -> list[Finding]:

    findings: list[Finding] = []

    for column in dataframe.columns:

        series = dataframe[column]

        if len(series) == 0:
            continue

        unique_ratio = (
            series.nunique(dropna=True)
            / len(series)
        )

        name_suggests_id = looks_like_id_name(column)

        is_numeric = pd.api.types.is_numeric_dtype(
            series
        )

        high_uniqueness = unique_ratio >= 0.95

        if not (
            name_suggests_id
            or (is_numeric and high_uniqueness)
        ):
            continue

        findings.append(
            Finding(
                type=FindingType.SUSPICIOUS_IDENTIFIER,
                severity=Severity.WARNING,
                title=f"Potential identifier column '{column}'",
                message=(
                    f"Column '{column}' appears to behave "
                    "like an identifier. It has "
                    f"{unique_ratio * 100:.2f}% unique values."
                ),
                column=column,
                evidence={
                    "unique_ratio": round(
                        unique_ratio,
                        4,
                    ),
                    "unique_percentage": round(
                        unique_ratio * 100,
                        2,
                    ),
                    "name_suggests_identifier": (
                        name_suggests_id
                    ),
                    "numeric": is_numeric,
                },
                recommendation=(
                    "Check whether this column identifies "
                    "individual records rather than representing "
                    "a meaningful predictive feature. Identifier "
                    "columns are often excluded from model training."
                ),
            )
        )

    return findings