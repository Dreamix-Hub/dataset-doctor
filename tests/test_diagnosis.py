"""Tests for dataset diagnosis."""
import pandas as pd

from app.diagnosis.engine import DiagnosisEngine
from app.diagnosis.schema import FindingType, Severity


def create_test_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "customer_id": [
                1001,
                1002,
                1003,
                1004,
                1005,
                1006,
            ],
            "age": [
                20,
                21,
                None,
                25,
                26,
                27,
            ],
            "income": [
                30000,
                32000,
                35000,
                40000,
                45000,
                500000,
            ],
            "churn": [
                "yes",
                "yes",
                "yes",
                "no",
                "no",
                "no",
            ],
        }
    )


def test_missing_value_diagnosis():
    dataframe = create_test_dataframe()

    engine = DiagnosisEngine(
        dataframe=dataframe,
        target_column="churn",
    )

    report = engine.diagnose()

    finding_types = [
        finding.type
        for finding in report.findings
    ]

    assert (
        FindingType.MISSING_VALUES
        in finding_types
    )


def test_identifier_detection():
    dataframe = create_test_dataframe()

    engine = DiagnosisEngine(
        dataframe=dataframe,
        target_column="churn",
    )

    report = engine.diagnose()

    identifier_findings = [
        finding
        for finding in report.findings
        if finding.type
        == FindingType.SUSPICIOUS_IDENTIFIER
    ]

    assert len(identifier_findings) >= 1


def test_outlier_detection():
    dataframe = create_test_dataframe()

    engine = DiagnosisEngine(
        dataframe=dataframe,
        target_column="churn",
    )

    report = engine.diagnose()

    outlier_findings = [
        finding
        for finding in report.findings
        if finding.type
        == FindingType.OUTLIERS
    ]

    assert len(outlier_findings) >= 1


def test_report_counts():
    dataframe = create_test_dataframe()

    engine = DiagnosisEngine(
        dataframe=dataframe,
        target_column="churn",
    )

    report = engine.diagnose()

    total_findings = (
        report.critical_count
        + report.warning_count
        + report.info_count
    )

    assert total_findings == len(
        report.findings
    )


def test_invalid_target_is_not_silently_accepted():
    dataframe = create_test_dataframe()

    engine = DiagnosisEngine(
        dataframe=dataframe,
        target_column="does_not_exist",
    )

    report = engine.diagnose()

    assert report.target_column == "does_not_exist"