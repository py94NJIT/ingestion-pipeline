import pandas as pd

def is_empty(value) -> bool:
    if value is None:
        return True
    if isinstance(value, float) and pd.isna(value):
        return True
    if str(value).strip() == "":
        return True
    return False
    
def is_valid_customer(row: dict) -> bool:
    id = row.get("customer_id")
    name = row.get("name")
    email = row.get("email")
    if is_empty(id):
        return False
    if is_empty(name):
        return False
    if is_empty(email):
        return False
    
    return True

def is_valid_manga(row: dict) -> bool:
    pass