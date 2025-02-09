import sqlite3
import pandas as pd
from contextlib import closing
from sqlite3 import Connection

DATABASE_NAME = "test.db"  # SQLite database name
INPUT_CSV = "employee_data_source.csv"  # Input CSV file path

# Establish and return a SQLite database connection.
# Raises an exception if the connection fails.
def get_db_connection() -> Connection:
    try:
        return sqlite3.connect(DATABASE_NAME)
    except sqlite3.Error as e:
        print(f"Error connecting to database '{DATABASE_NAME}': {e}")
        raise

# Ensures that the 'users' table exists in the database.
# Creates the table if it does not already exist.
def ensure_table_exists():
    create_table_query = """
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER,
        name TEXT,
        age INTEGER,
        join_date TIMESTAMP NOT NULL,
        year_xp INTEGER,
        country TEXT,
        salary BIGINT,
        performance_rating TEXT
    );
    """
    try:
        with get_db_connection() as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute(create_table_query)
        print(f"Table 'users' exists in the database '{DATABASE_NAME}'.")
    except sqlite3.Error as e:
        print(f"Error ensuring table exists in database '{DATABASE_NAME}': {e}")
        raise

# Loads data from a CSV file and inserts it into the SQLite database using a batch approach.
def insert_data_from_csv(csv_file: str):
    try:
        df = pd.read_csv(csv_file)
        with get_db_connection() as connection:
            df.to_sql("users", connection, if_exists="append", index=False, dtype={"created_date": "TIMESTAMP"})
        print(f"Inserted {len(df)} records from '{csv_file}' into the database '{DATABASE_NAME}'.")
    except Exception as e:
        print(f"Error inserting data from CSV '{csv_file}': {e}")

# Queries and displays all records from the 'users' table in the SQLite database.
def query_and_display_data():
    try:
        with get_db_connection() as connection:
            with closing(connection.cursor()) as cursor:
                print("\nData in the 'users' table:")
                rows = cursor.execute("SELECT * FROM users").fetchall()
                for row in rows:
                    print(row)
    except Exception as e:
        print(f"Error querying database '{DATABASE_NAME}': {e}")

if __name__ == "__main__":
    ensure_table_exists()
    insert_data_from_csv(INPUT_CSV)
    query_and_display_data()
