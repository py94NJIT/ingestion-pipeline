import pandas as pd
import logging

logger = logging.getLogger("pipeline.readers.csv")

def extract_csv(filepath: str) -> list:
    """Reads a CSV file and flattens rows into clean dictionaries."""
    try:
        df = pd.read_csv(filepath)
        # Convert Pandas NaN objects to None to avoid floating-point string errors
        df = df.where(pd.notnull(df), None)
        return df.to_dict(orient='records')
    except Exception as e:
        logger.error(f"Failed to extract file at path {filepath}: {e}")
        raise e