"""Missing-value diagnosis checks."""
from app.profiler.schema import DatasetProfile
from app.diagnosis.schema import (
    Finding,
    FindingType,
    Severity,
)


def detect_missing_values(
    profile: DatasetProfile,
) -> list[Finding]:
    findings: list[Finding] = []

    for column in profile.column_profiles:

        percentage = column.missing_percentage

        if percentage == 0:
            continue

        if percentage >= 50:
            severity = Severity.CRITICAL
        elif percentage >= 10:
            severity = Severity.WARNING
        else:
            severity = Severity.INFO

        findings.append(
            Finding(
                type=FindingType.MISSING_VALUES,
                severity=severity,
                title=f"Missing values in '{column.name}'",
                message=(
                    f"Column '{column.name}' contains "
                    f"{column.missing_values} missing values "
                    f"out of {column.total_values} rows "
                    f"({percentage}%)."
                ),
                column=column.name,
                evidence={
                    "missing_values": column.missing_values,
                    "total_values": column.total_values,
                    "missing_percentage": percentage,
                },
                recommendation=(
                    "Investigate why values are missing before "
                    "choosing an imputation strategy."
                ),
            )
        )

    return findings