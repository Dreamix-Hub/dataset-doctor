from fastapi import FastAPI, File, HTTPException, UploadFile

from app.diagnosis.engine import DiagnosisEngine
from app.profiler.loader import load_csv
from app.profiler.profiler import DatasetProfiler


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