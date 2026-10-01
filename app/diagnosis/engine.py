"""Diagnosis engine."""
import pandas as pd

from app.diagnosis.correlation import detect_high_correlations
from app.diagnosis.identifiers import (
    detect_suspicious_identifiers,
)
from app.diagnosis.imbalance import detect_class_imbalance
from app.diagnosis.missing import detect_missing_values
from app.diagnosis.outliers import detect_outliers
from app.diagnosis.schema import (
    DiagnosisReport,
    Finding,
    Severity,
)
from app.profiler.profiler import DatasetProfiler


class DiagnosisEngine:
    """
    Dataset Doctor's Phase 2 diagnosis engine.

    The engine takes a DataFrame, runs multiple
    deterministic checks, and produces a structured
    diagnosis report.
    """

    def __init__(
        self,
        dataframe: pd.DataFrame,
        filename: str = "dataset.csv",
        target_column: str | None = None,
    ):
        self.dataframe = dataframe
        self.filename = filename
        self.target_column = target_column

    def diagnose(self) -> DiagnosisReport:
        """
        Run all available diagnosis checks.
        """

        profile = DatasetProfiler(
            dataframe=self.dataframe,
            filename=self.filename,
        ).profile()

        findings: list[Finding] = []

        findings.extend(
            detect_missing_values(profile)
        )

        findings.extend(
            detect_outliers(self.dataframe)
        )

        findings.extend(
            detect_class_imbalance(
                dataframe=self.dataframe,
                target_column=self.target_column,
            )
        )

        findings.extend(
            detect_high_correlations(
                dataframe=self.dataframe,
            )
        )

        findings.extend(
            detect_suspicious_identifiers(
                dataframe=self.dataframe,
            )
        )

        critical_count = sum(
            finding.severity == Severity.CRITICAL
            for finding in findings
        )

        warning_count = sum(
            finding.severity == Severity.WARNING
            for finding in findings
        )

        info_count = sum(
            finding.severity == Severity.INFO
            for finding in findings
        )

        return DiagnosisReport(
            filename=self.filename,
            rows=len(self.dataframe),
            columns=len(self.dataframe.columns),
            target_column=self.target_column,
            critical_count=critical_count,
            warning_count=warning_count,
            info_count=info_count,
            findings=findings,
        )