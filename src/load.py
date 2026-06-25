import os
import json
import logging
import psycopg2
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("pipeline.load")

def get_db_connection():
    return psycopg2.connect(
        database=os.getenv("DB_NAME"), 
        user=os.getenv("DB_USER"), 
        password=os.getenv("DB_PASSWORD"), 
        host=os.getenv("DB_HOST"), 
        port=os.getenv("DB_PORT")
    )

def load_clean_batch(batch_data: list, table_name: str, primary_key: str):
    """Dynamically updates or creates targets using dictionary keys."""
    if not batch_data:
        return

    columns = batch_data[0].keys()
    columns_str = ", ".join(columns)
    placeholders = ", ".join(["%s"] * len(columns))
    update_assignments = ", ".join([f"{col} = EXCLUDED.{col}" for col in columns if col != primary_key])

    insert_query = f"""
        INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})
        ON CONFLICT ({primary_key}) DO UPDATE SET {update_assignments};
    """

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verify tracking target table exists prior to looping values
        if table_name == "stg_customers":
            cursor.execute("CREATE TABLE IF NOT EXISTS stg_customers (customer_id INT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100), signup_date DATE);")
        elif table_name == "stg_manga":
            cursor.execute("CREATE TABLE IF NOT EXISTS stg_manga (manga_id INT PRIMARY KEY, title VARCHAR(255), status VARCHAR(50), score NUMERIC(4,2), published_date DATE);")

        for record in batch_data:
            cursor.execute(insert_query, tuple(record[col] for col in columns))
            
        conn.commit()
        logger.info(f"Loaded {len(batch_data)} rows successfully into table '{table_name}'.")
    except Exception as e:
        if conn: conn.rollback()
        logger.error(f"Failed loading metrics target to DB table {table_name}: {e}")
        raise e
    finally:
        if conn: conn.close()

def _sanitize_payload(payload: dict) -> dict:
    """Recursively replaces invalid JSON tokens like float 'NaN' with None."""
    sanitized = {}
    for key, val in payload.items():
        if val is None or (isinstance(val, float) and pd.isna(val)):
            sanitized[key] = None
        else:
            sanitized[key] = val
    return sanitized

def load_rejected_record(source_name: str, raw_payload: dict, reason: str):
    """Ensures audit rejections drop down inside the 'stg_rejects' table blueprint."""
    insert_query = "INSERT INTO stg_rejects (source_name, raw_payload, reason) VALUES (%s, %s, %s);"
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stg_rejects (
                source_name TEXT, 
                raw_payload JSONB, 
                reason TEXT, 
                rejected_at TIMESTAMP DEFAULT NOW()
            );
        """)
        
        clean_payload = _sanitize_payload(raw_payload)
        json_payload = json.dumps(clean_payload)
        
        cursor.execute(insert_query, (source_name, json_payload, reason))
        conn.commit()
    except Exception as e:
        if conn: conn.rollback()
        logger.critical(f"Database logging subsystem unavailable. Dropped fallback metrics: {e}")
    finally:
        if conn: conn.close()