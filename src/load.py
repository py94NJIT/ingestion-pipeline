import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def get_db_connection():
    conn = psycopg2.connect(
        database=os.getenv("DB_NAME"), 
        user=os.getenv("DB_USER"), 
        password=os.getenv("DB_PASSWORD"), 
        host=os.getenv("DB_HOST"), 
        port = os.getenv("DB_PORT")
    )
    return conn
def load_customer_record(clean_record: dict):
    insert_query = """
        INSERT INTO customers(customer_id, name, email, signup_date)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (customer_id) DO UPDATE SET
            name = EXCLUDED.name,
            email = EXCLUDED.email,
            signup_date = EXCLUDED.signup_date;
    """

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS customers(
                customer_id int PRIMARY KEY, 
                name varchar(50), 
                email varchar(100) , 
                signup_date DATE
            ); 
        """)
        cursor.execute(insert_query, (
            clean_record["customer_id"],
            clean_record["name"],
            clean_record["email"],
            clean_record["signup_date"]
        ))
        conn.commit()
        cursor.close()
    except Exception as e:
        if conn:
            conn.rollback()
            print(f" Database error loading customer ID {clean_record.get('customer_id')}: {e}")
            raise e
    finally:
        if conn:
            conn.close()

def load_manga_record(clean_record: dict):
    pass
    