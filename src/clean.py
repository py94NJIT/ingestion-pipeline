import pandas
import readers.csv_reader as read
from datetime import datetime

def clean_data(df):
    pass

def clean_string(value :str ,casing:str ="title") -> str:
    '''
    formats string into desired case and strips extra spacing and returns string
    '''
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
    

def transform_customer_record(rows: dict) -> dict:
    '''
    function to call all clean functions on data for csv data
    '''
    
    print(clean_string("defAULT"))
    print(clean_date("2024/01/12"))
    pass

