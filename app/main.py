from fastapi import FastAPI, File, HTTPException, UploadFile

from app.diagnosis.engine import DiagnosisEngine
from app.profiler.loader import load_csv
from app.profiler.profiler import DatasetProfiler

from app.ai.service import GemmaService
from app.api.schema import AnalyzeResponse
import io

import pandas as pd

from fastapi import (
    FastAPI,
    File,
    Form,
    HTTPException,
    UploadFile,
)



app = FastAPI(
    title="Dataset Doctor",
    description=(
        "AI-powered dataset quality and analysis tool."
    ),
    version="0.2.0",
)


@app.get("/")
def root():
    return {
        "name": "Dataset Doctor",
        "version": "0.2.0",
        "phase": 2,
        "status": "running",
    }


@app.post("/profile")
async def profile_dataset(
    file: UploadFile = File(...),
):
    """
    Phase 1:
    Generate a raw dataset profile.
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing.",
        )

    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are supported.",
        )

    try:
        file_content = await file.read()

        dataframe = load_csv(file_content)

        profiler = DatasetProfiler(
            dataframe=dataframe,
            filename=file.filename,
        )

        profile = profiler.profile()

        return profile.model_dump()

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {exc}",
        ) from exc


@app.post("/diagnose")
async def diagnose_dataset(
    file: UploadFile = File(...),
    target_column: str | None = None,
):
    """
    Phase 2:
    Analyze a dataset and generate structured diagnoses.
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing.",
        )

    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are supported.",
        )

    try:
        file_content = await file.read()

        dataframe = load_csv(file_content)

        if (
            target_column
            and target_column not in dataframe.columns
        ):
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Target column '{target_column}' "
                    "does not exist in the dataset."
                ),
            )

        engine = DiagnosisEngine(
            dataframe=dataframe,
            filename=file.filename,
            target_column=target_column,
        )

        report = engine.diagnose()

        return report.model_dump()

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {exc}",
        ) from exc
        
@app.post("/analyze",   response_model=AnalyzeResponse)
async def analyze_dataset(
    file: UploadFile = File(...),
    target_column: str | None = Form(None),
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required.",
        )

    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are supported.",
        )

    try:
        contents = await file.read()

        dataframe = pd.read_csv(
            io.BytesIO(contents)
        )

    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Could not read CSV file: {exc}",
        ) from exc

    if dataframe.empty:
        raise HTTPException(
            status_code=400,
            detail="The uploaded dataset is empty.",
        )

    if target_column is not None:
        if target_column not in dataframe.columns:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Target column '{target_column}' "
                    "does not exist in the dataset."
                ),
            )

    diagnosis_engine = DiagnosisEngine(
        dataframe=dataframe,
        filename=file.filename,
        target_column=target_column,
    )

    diagnosis = diagnosis_engine.diagnose()

    try:
        gemma_service = GemmaService()

        ai_analysis = gemma_service.analyze(
            diagnosis
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Gemma API request failed: {exc}",
        ) from exc

    return AnalyzeResponse(
    filename=diagnosis.filename,
    rows=diagnosis.rows,
    columns=diagnosis.columns,
    target_column=diagnosis.target_column,
    status="completed",
    critical_count=diagnosis.critical_count,
    warning_count=diagnosis.warning_count,
    info_count=diagnosis.info_count,
    findings=[
        {
            "type": finding.type.value,
            "severity": finding.severity.value,
            "title": finding.title,
            "message": finding.message,
            "column": finding.column,
            "columns": finding.columns,
            "evidence": finding.evidence,
            "recommendation": finding.recommendation,
        }
        for finding in diagnosis.findings
    ],
    ai_analysis={
        "summary": ai_analysis.summary,
        "findings": [
            {
                "type": finding.type,
                "title": finding.title,
                "severity": finding.severity,
                "explanation": finding.explanation,
                "action": finding.action,
            }
            for finding in ai_analysis.findings
        ],
        "next_steps": ai_analysis.next_steps,
    },
)