import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def load_to_postgres():
    #conninfo= "dbname=postgres user=postgres password=032895 host=localhost port=5432"
    conn = psycopg2.connect(
        database=os.getenv("DB_NAME"), 
        user=os.getenv("DB_USER"), 
        password=os.getenv("DB_PASSWORD"), 
        host=os.getenv("DB_HOST"), 
        port = os.getenv("DB_PORT")
    )

    cursor=conn.cursor()

    cursor.execute(f"""CREATE TABLE IF NOT EXISTS customers(customer_id int PRIMARY KEY, name varchar(30) , email varchar(30) , signup_date varchar(10)); """)
    cursor.execute(f"""INSERT INTO customers(customer_id, name, email, signup_date) VALUES (101, 'alice smith', 'ALICE@example.com', '2026-01-15');""")
    conn.commit()

    cursor.execute(f"""SELECT * from customers""")
    print(cursor.fetchall())
    cursor.close()
    conn.close()

if __name__== "__main__":
    load_to_postgres()
    