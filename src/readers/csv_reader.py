import csv
import pandas as pd

def extract_csv(filepath: str):
    df = pd.read_csv(filepath)
    df.to_dict(orient='records')
    print(df)
    
    return df

