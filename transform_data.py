import psycopg2
from psycopg2 import sql
from contextlib import closing
from dotenv import load_dotenv
import os
from db_utils import get_db_connection

# load_dotenv()

# DATABASE_NAME = os.getenv("DB_NAME")
# USER = os.getenv("DB_USER")
# PASSWORD = os.getenv("DB_PASSWORD")
# HOST = os.getenv("DB_HOST")
# PORT = os.getenv("DB_PORT")


# def get_db_connection():
#     try:
#         return psycopg2.connect(
#             dbname=DATABASE_NAME,
#             user=USER,
#             password=PASSWORD,
#             host=HOST,
#             port=PORT
#         )
#     except psycopg2.Error as e:
#         print(f"Error connecting to PostgreSQL database '{DATABASE_NAME}': {e}")
#         raise

def clean_data():
    try:
        with get_db_connection() as connection:
            with closing(connection.cursor()) as cursor:
                # Handle missing data
                cursor.execute("""
                    UPDATE employees
                    SET age = COALESCE(age, 0),
                        salary = COALESCE(salary, 0),
                        year_xp = COALESCE(year_xp, '0'),
                        name = COALESCE(name, 'Unknown'),
                        dept = COALESCE(dept, 'Unknown'),
                        country = COALESCE(country, 'Unknown'),
                        performance_rating = COALESCE(performance_rating, 'Unknown');
                """)
                
                # Standardize department names
                cursor.execute("""
                    UPDATE employees
                    SET dept = CASE
                        WHEN dept ILIKE 'RnD' THEN 'R&D'
                        WHEN dept ILIKE 'Oprations' THEN 'Operations'
                        WHEN dept ILIKE 'Marketng' THEN 'Marketing'
                        WHEN dept ILIKE 'Lgistics' THEN 'Logistics'
                        WHEN dept ILIKE 'Hr' OR dept ILIKE 'H R' OR dept ILIKE 'hr' THEN 'HR'
                        WHEN dept ILIKE 'Fin' OR dept ILIKE 'Finanace' THEN 'Finance'
                        WHEN dept ILIKE 'Customer Support' THEN 'Customer Support'
                        WHEN dept ILIKE 'Sales' THEN 'Sales'
                        ELSE dept
                    END;
                """)
                
                # Handle duplicate IDs
                cursor.execute("""
                    WITH duplicates AS (
                        SELECT id, MIN(ctid) AS min_ctid
                        FROM employees
                        GROUP BY id
                        HAVING COUNT(*) > 1
                    )
                    DELETE FROM employees
                    WHERE ctid NOT IN (SELECT min_ctid FROM duplicates);
                """)
                
                # Add primary key constraint
                cursor.execute("""
                    ALTER TABLE employees
                    ADD CONSTRAINT employees_pk PRIMARY KEY (id);
                """)

                cursor.execute("""
                    ALTER TABLE employees
                    ALTER COLUMN year_xp TYPE INTEGER USING year_xp::INTEGER;
                """)
                
                connection.commit()  # Commit the transaction
        print("Data cleaning completed successfully.")
    except Exception as e:
        print(f"Error cleaning data: {e}")
        raise

if __name__ == "__main__":
    clean_data()