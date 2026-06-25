import pandas as pd

def _is_empty(value) -> bool:
    """Helper asserting if field properties contain blank or NaN variables."""
    if value is None:
        return True
    if isinstance(value, float) and pd.isna(value):
        return True
    if str(value).strip() == "":
        return True
    return False

def is_valid_customer(row: dict) -> bool:
    """Gatekeeper logic validating data completeness for raw customer rows."""
    if _is_empty(row.get("customer_id")) or _is_empty(row.get("name")) or _is_empty(row.get("email")):
        return False
    return True

def is_valid_manga(row: dict) -> bool:
    """Gatekeeper logic validating structural presence for raw manga maps."""
    if _is_empty(row.get("mal_id")) or _is_empty(row.get("title")):
        return False
    return True