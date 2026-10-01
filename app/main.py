"""Application entry point."""

from fastapi import FastAPI, File, HTTPException, UploadFile

from app.profiler.loader import load_csv
from app.profiler.profiler import DatasetProfiler


app = FastAPI(
    title="Dataset Doctor",
    description=(
        "AI-powered dataset quality and analysis tool."
    ),
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "name": "Dataset Doctor",
        "version": "0.1.0",
        "status": "running",
    }


@app.post("/profile")
async def profile_dataset(
    file: UploadFile = File(...),
):
    """
    Upload a CSV and generate a dataset profile.
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