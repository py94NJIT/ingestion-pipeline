import pandas as pd
import readers.csv_reader as read
from datetime import datetime

def clean_data(df):
    pass

def clean_string(value :str ,casing:str ="title") -> str:
    '''
    formats string into desired case and strips extra spacing and returns string
    '''
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    cleaned = value.strip()
    if casing == "lower":
        cleaned = value.lower()
    else:
        cleaned = value.title()
    return cleaned

def clean_date(date_str : str) -> str:
    if not date_str: return None
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%Y-%m-%dT%H:%M:%S%z"):
        try:
            return datetime.strptime(str(date_str).strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None
    

def transform_customer_record(row: dict) -> dict:
    '''
    function to call all clean functions on data for csv data
    '''
    return {
        "customer_id": int(row["customer_id"]),
        "name": clean_string(row.get("name"), casing = "title"),
        "email": clean_string(row.get("email"), casing = "lower"),
        "signup_date": clean_date(row.get("signup_date)"))

    }
    
def transform_manga_record(rows: dict) -> dict:
    pass
