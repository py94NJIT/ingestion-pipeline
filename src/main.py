from readers import csv_reader
from readers import api_reader
from validate import is_valid_customer, is_valid_manga
from clean import transform_customer_record, transform_manga_record


if __name__ == "__main__":
    raw_csv_rows=csv_reader.extract_csv("data/dummy.csv")
    for r in raw_csv_rows:
        if is_valid_customer(r):
            clean_record = transform_customer_record(r)
            print(f"  ✓ Validated & Cleaned ID {clean_record['customer_id']}: '{r.get('name')}' -> '{clean_record['name']}'")
        else:
            print( "Row Skipped (Failed Validation)")