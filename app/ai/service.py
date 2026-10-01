from app.ai.gemma import GemmaModel
from app.ai.prompts import (
    SYSTEM_PROMPT,
    build_finding_prompt,
)
from app.ai.schema import (
    AIAnalysis,
    AIFinding,
    FindingExplanation,
)
from app.diagnosis.schema import (
    DiagnosisReport,
    Finding,
)


class GemmaService:
    """
    Uses Gemma to explain deterministic
    Dataset Doctor findings.

    Python remains the source of truth.
    """

    def __init__(
        self,
        model: GemmaModel | None = None,
    ):
        self.model = model or GemmaModel()

    def explain_finding(
        self,
        finding: Finding,
    ) -> FindingExplanation:

        user_prompt = build_finding_prompt(
            finding
        )

        return self.model.explain(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )

    def analyze(
        self,
        diagnosis_report: DiagnosisReport,
        max_findings: int = 3,
    ) -> AIAnalysis:

        # Sort findings by severity.
        ordered_findings = sorted(
            diagnosis_report.findings,
            key=lambda finding: {
                "critical": 0,
                "warning": 1,
                "info": 2,
            }.get(
                finding.severity.value,
                3,
            ),
        )

        selected_findings = ordered_findings[
            :max_findings
        ]

        ai_findings = []

        for finding in selected_findings:

            explanation = self.explain_finding(
                finding
            )

            ai_findings.append(
                AIFinding(
                    type=finding.type.value,
                    title=finding.title,
                    severity=finding.severity.value,
                    explanation=(
                        explanation.explanation
                    ),
                    action=explanation.action,
                )
            )

        summary = self._build_summary(
            diagnosis_report
        )

        next_steps = self._build_next_steps(
            selected_findings
        )

        return AIAnalysis(
            summary=summary,
            findings=ai_findings,
            next_steps=next_steps,
        )

    def _build_summary(
        self,
        report: DiagnosisReport,
    ) -> str:

        total = len(report.findings)

        if total == 0:
            return (
                "No dataset-quality issues were detected."
            )

        if report.critical_count > 0:
            return (
                f"The dataset has {total} detected "
                "issues, including critical problems "
                "that should be addressed before training."
            )

        if report.warning_count > 0:
            return (
                f"The dataset has {total} detected "
                "issues that should be reviewed before "
                "machine-learning training."
            )

        return (
            f"The dataset has {total} informational "
            "findings to review."
        )

    def _build_next_steps(
        self,
        findings: list[Finding],
    ) -> list[str]:

        steps = []

        for finding in findings:
            steps.append(
                finding.recommendation
            )

        # Remove duplicates while preserving order.
        unique_steps = list(
            dict.fromkeys(steps)
        )

        return unique_steps[:3]