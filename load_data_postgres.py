import psycopg2
import pandas as pd
from contextlib import closing
from psycopg2 import sql
from psycopg2.extras import execute_values
import os
from dotenv import load_dotenv
import json

load_dotenv()

DATABASE_NAME = os.getenv("DB_NAME")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")

INPUT_CSV = "employee_data_source.csv" 

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


def ensure_table_exists():
    create_table_query = """
    CREATE TABLE IF NOT EXISTS employees (
        id INT,
        name TEXT,
        age INT,
        dept TEXT,
        join_date TIMESTAMP NOT NULL,
        year_xp TEXT,
        country TEXT,
        salary BIGINT,
        performance_rating TEXT
    );
    """
    try:
        with get_db_connection() as connection:
            with closing(connection.cursor()) as cursor:
                #cursor.execute("DROP TABLE employees;")
                cursor.execute(create_table_query)
                connection.commit()  # Commit the transaction
        print(f"Table 'employees' exists in the database '{DATABASE_NAME}'.")
    except psycopg2.Error as e:
        print(f"Error ensuring table exists in database '{DATABASE_NAME}': {e}")
        raise


# def validate_bigint_range(value, column_name):
#     """
#     Validates if a value is within the range of a PostgreSQL BIGINT.
#     Raises an exception if the value is out of range.
#     """
#     min_bigint = -9223372036854775808
#     max_bigint = 9223372036854775807
    
#     if not (min_bigint <= value <= max_bigint):
#         raise ValueError(
#             f"Value '{value}' in column '{column_name}' is out of range for BIGINT. "
#             f"Allowed range: {min_bigint} to {max_bigint}."
#         )
    
def insert_data_from_csv(csv_file: str):
    try:
        df = pd.read_csv(csv_file, header=0)
        print(df)
        with get_db_connection() as connection:
            with closing(connection.cursor()) as cursor:
                # Convert DataFrame to a list of tuples for batch insertion
                data_tuples = [tuple(row) for row in df.to_numpy()]
                f = open('csv_to_db_column_mapping.json')
                column_mapping = json.load(f)
                df.rename(columns=column_mapping, inplace=True)
                columns = df.columns.tolist()

                # bigint_columns = ["id", "age", "year_xp", "salary"]
                # for index, row in df.iterrows():
                #     for column in bigint_columns:
                #         value = row[column]
                #         try:
                #             validate_bigint_range(value, column)
                #         except ValueError as e:
                #             print(f"Row {index + 1}: {e}")
                #             raise
                
                # Use execute_values for efficient batch insertion
                execute_values(
                    cursor,
                    sql.SQL("INSERT INTO employees ({}) VALUES %s").format(
                        sql.SQL(', ').join(map(sql.Identifier, columns))
                    ),
                    data_tuples
                )
                connection.commit()  # Commit the transaction
        print(f"Inserted {len(df)} records from '{csv_file}' into the database '{DATABASE_NAME}'.")
    except Exception as e:
        print(f"Error inserting data from CSV '{csv_file}': {e}")

def query_and_display_data():
    try:
        with get_db_connection() as connection:
            with closing(connection.cursor()) as cursor:
                pass
                #print("\nData in the 'employees' table:")
                #cursor.execute("SELECT * FROM employees")
                #rows = cursor.fetchall()
                #for row in rows:
                #    print(row)
    except Exception as e:
        print(f"Error querying database '{DATABASE_NAME}': {e}")

if __name__ == "__main__":
    ensure_table_exists()
    insert_data_from_csv(INPUT_CSV)
    query_and_display_data()