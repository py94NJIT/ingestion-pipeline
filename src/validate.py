def is_valid_customer(row: dict) -> bool:
    if( not row.get("customer_id") or not row.get("name")):
        return False
    return True

def is_valid_manga(row: dict) -> bool:
    pass