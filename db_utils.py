import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

DATABASE_NAME = os.getenv("DB_NAME")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")

def get_db_connection():
    try:
        return psycopg2.connect(
            dbname=DATABASE_NAME,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT
        )
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL database '{DATABASE_NAME}': {e}")
        raise 