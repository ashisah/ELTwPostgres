import psycopg2
from psycopg2 import sql
from contextlib import closing
from dotenv import load_dotenv
import os
from db_utils import get_db_connection


def clean_data():
    try:
        with get_db_connection() as connection:
            with closing(connection.cursor()) as cursor:
                # Handle missing data
                cursor.execute("""
                    UPDATE employees
                    SET 
                        name = NULLIF(name, 'NaN'),
                        year_xp = NULLIF(year_xp, 'NaN'),
                        dept = NULLIF(dept, 'NaN'),
                        country = NULLIF(country, 'NaN'),
                        performance_rating = NULLIF(performance_rating, 'NaN');
                """)
                
                
                cursor.execute("""
                    UPDATE employees
                    SET year_xp = COALESCE(year_xp, '0'),
                        name = COALESCE(name, 'Unknown'),
                        dept = COALESCE(dept, 'Unknown'),
                        country = COALESCE(country, 'Unknown'),
                        performance_rating = COALESCE(performance_rating, 'Unknown');
                """)

                #change year_xp from text to integer column
                cursor.execute("""
                    ALTER TABLE employees
                    ALTER COLUMN year_xp TYPE bigint USING CASE
                        WHEN trim(year_xp) SIMILAR TO '[0-9]+' THEN year_xp::bigint
                        ELSE NULL -- or 0 if you want to convert non-numeric or problematic values to zero
                    END;
                """)
                
                
                # Standardize department names
                cursor.execute("""UPDATE employees SET dept = UPPER(dept);""")
                cursor.execute("""
                    UPDATE employees
                    SET dept = CASE
                        WHEN dept ILIKE 'CUST SUPPORT' OR dept ILIKE 'CUSTOMERSUPPORT' THEN 'CUSTOMER SUPPORT'
                        WHEN dept ILIKE 'FIN' OR dept ILIKE 'FINANACE' THEN 'FINANCE'
                        WHEN dept ILIKE 'H R' OR dept ILIKE 'HR' THEN 'HUMAN RESOURCES'
                        WHEN dept ILIKE 'LEGL' THEN 'LEGAL'
                        WHEN dept ILIKE 'LGISTICS' OR dept ILIKE 'LOGSTICS' THEN 'LOGISTICS'
                        WHEN dept ILIKE 'MARKETNG' THEN 'MARKETING'
                        WHEN dept ILIKE 'OPRATIONS' THEN 'OPERATIONS'
                        WHEN dept ILIKE 'RESEARCH' OR dept ILIKE 'RND' THEN 'R&D'
                        WHEN dept ILIKE 'SLAES' THEN 'SALES'
                        ELSE dept
                    END;
                """)

                #standardize country names
                cursor.execute("UPDATE employees SET country = UPPER(country);")
                
                # Handle duplicate IDs--sufficient to just delete
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