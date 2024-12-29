from datetime import datetime
from .db_param_view import SQL_SERVER_CONNECTION_STRING, PANDAS_TO_SQL_TYPE_MAPPING
import pandas as pd
from sqlalchemy import create_engine, text

def generate_create_table_sql(df, table_name):
    """
    Generate a CREATE TABLE SQL statement from a DataFrame schema.

    Args:
        df (pd.DataFrame): DataFrame to infer schema from.
        table_name (str): Name of the SQL table.

    Returns:
        str: CREATE TABLE SQL statement.
    """
    try:
        # Sanitize column names
        def sanitize_column_name(col):
            return (col.replace(" ", "_")
                       .replace("(", "")
                       .replace(")", "")
                       .replace("%", "percent"))

        columns = []
        for col, dtype in df.dtypes.items():
            sql_type = PANDAS_TO_SQL_TYPE_MAPPING.get(str(dtype), 'NVARCHAR(MAX)')
            sanitized_col = sanitize_column_name(col)
            # Ensure column names are properly quoted
            columns.append(f"[{sanitized_col}] {sql_type}")

        columns_def = ", ".join(columns)
        create_table_sql = f"CREATE TABLE [{table_name}] ({columns_def});"
        # print(f"[ {datetime.now()} ]-------- Generated CREATE TABLE SQL:\n{create_table_sql}")
        return create_table_sql
    except Exception as e:
        print(f"[ {datetime.now()} ]-------- Error generating CREATE TABLE statement: {e}")
        raise


def ensure_table_exists(df, table_name, connection_string=SQL_SERVER_CONNECTION_STRING):
    try:
        engine = create_engine(connection_string)
        create_table_sql = generate_create_table_sql(df, table_name)

        with engine.connect() as conn:
            # Start a transaction
            trans = conn.begin()
            try:
                # Check if the table exists
                query = f"""
                    SELECT 1
                    FROM INFORMATION_SCHEMA.TABLES
                    WHERE TABLE_NAME = '{table_name}' AND TABLE_SCHEMA = 'dbo';
                """
                result = conn.execute(text(query)).fetchone()

                if not result:
                    print(f"[ {datetime.now()} ]-------- Creating table: {table_name}")
                    conn.execute(text(create_table_sql))
                    print(f"[ {datetime.now()} ]-------- Table {table_name} created successfully.")
                else:
                    print(f"[ {datetime.now()} ]-------- Table {table_name} already exists.")
                
                # Commit the transaction
                trans.commit()
            except Exception as e:
                trans.rollback()  # Rollback the transaction on error
                print(f"[ {datetime.now()} ]-------- Error ensuring table exists: {e}")
                raise
    except Exception as e:
        print(f"[ {datetime.now()} ]-------- Error connecting to the database: {e}")
        raise
