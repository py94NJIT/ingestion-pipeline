import csv
import pandas as pd

def extract_csv(filepath: str):
    df = pd.read_csv(filepath)

    df = df.where(pd.notnull(df), None)
    print(df)
    
    return df.to_dict(orient='records')

