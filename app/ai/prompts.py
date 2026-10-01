import json

from app.diagnosis.schema import Finding


SYSTEM_PROMPT = """
You are Dataset Doctor.

Python has already analyzed the dataset.

Your job is ONLY to explain the provided finding.

Python is the source of truth.

DO NOT:
- create new findings
- change the severity
- change the finding type
- invent statistics
- invent columns
- invent evidence
- question whether the finding exists

Use ONLY the information provided.

Keep the response concise.

Return JSON with exactly:

{
  "explanation": "one short sentence",
  "action": "one short sentence"
}

Return JSON only.
"""


def build_finding_prompt(
    finding: Finding,
) -> str:

    data = {
        "type": finding.type.value,
        "severity": finding.severity.value,
        "title": finding.title,
        "message": finding.message,
        "column": finding.column,
        "columns": finding.columns,
        "evidence": finding.evidence,
        "recommendation": finding.recommendation,
    }

    return f"""
Explain this Python-generated dataset finding.

{json.dumps(data, indent=2)}

Remember:

Only explain this finding.

Do not create any additional findings.

Return JSON only.
"""