"""Dataset loading utilities."""
from io import BytesIO

import pandas as pd


def load_csv(file_content: bytes) -> pd.DataFrame:
    """
    Load CSV file content into a pandas DataFrame.
    """

    if not file_content:
        raise ValueError("The uploaded file is empty.")

    try:
        dataframe = pd.read_csv(BytesIO(file_content))
    except Exception as exc:
        raise ValueError(f"Could not read CSV file: {exc}") from exc

    if dataframe.empty:
        raise ValueError("The CSV file contains no rows.")

    if len(dataframe.columns) == 0:
        raise ValueError("The CSV file contains no columns.")

    return dataframe