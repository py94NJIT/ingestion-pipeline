import logging
import pandas as pd
import readers.csv_reader as read
from datetime import datetime

# Initialize module specific logger
logger = logging.getLogger("pipeline.clean")

class DataTransformationError(Exception):
    """Custom exception raised when transforming or formatting fails"""
    pass

def clean_string(value :str ,casing:str ="title") -> str:
    '''
    formats string into desired case and strips extra spacing and returns string
    '''
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    cleaned = str(value).strip()
    if casing == "lower":
        cleaned = cleaned.lower()
    else:
        cleaned = cleaned.title()
    return cleaned

def clean_date(date_str: str) -> str:
    if not date_str or (isinstance(date_str, float) and pd.isna(date_str)): 
        return None
    
    date_str = str(date_str).strip()
    
    # ADDED "%Y-%m-%dT%H:%M:%S%z" to the front of the tuple to handle standard API timestamps
    for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d", "%Y/%m/%d", "%m-%d-%Y", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
            
    raise DataTransformationError(f"Unable to parse date string format: '{date_str}'")
    

def transform_customer_record(row: dict) -> dict:
    '''
    function to call all clean functions on data for csv data
    '''
    try:
        return {
            "customer_id": int(row["customer_id"]),
            "name": clean_string(row.get("name"), casing = "title"),
            "email": clean_string(row.get("email"), casing = "lower"),
            "signup_date": clean_date(row.get("signup_date"))

        }
    except KeyError as e:
        logger.error(f"Structural column footprint mapping missing: {e}")
        raise DataTransformationError
    except ValueError as e:
        logger.error(f"Data type conversion failed: {e}")
        raise DataTransformationError

    
def transform_manga_record(row: dict) -> dict:
    try:
        published_dict = row.get("published", {}) or {}
        return {
            "manga_id": int(row["mal_id"]),
            "title": clean_string(row.get("title"), casing="title"),
            "status": clean_string(row.get("status"), casing="lower"),
            "score": float(row["score"]) if row.get("score") else None,
            "published_date": clean_date(published_dict.get("from"))
        }
    except Exception as e:
        raise DataTransformationError(f"Manga nested stream parsing failure: {e}")