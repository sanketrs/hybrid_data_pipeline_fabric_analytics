from datetime import datetime
import os
import pandas as pd
from sqlalchemy import create_engine, text
from ..utils.db_param_view import SQL_SERVER_CONNECTION_STRING
from ..utils.manage_schema_view import ensure_table_exists
from ..utils.metadata_view import is_sheet_processed, update_metadata
from ..utils.validate_view import split_and_handle_invalid_rows_generic
from ..utils.validation_models import get_pydantic_model_for_table


def bulk_insert(df, table_name, connection_string):
    """
    Perform a bulk insert into SQL Server using raw SQL with sanitized column names.

    Args:
        df (pd.DataFrame): DataFrame to insert.
        table_name (str): Target SQL Server table name.
        connection_string (str): SQLAlchemy connection string.
    """
    try:
        # Sanitize column names
        sanitized_columns = {
            col: col.replace(" ", "_")
                   .replace("(", "")
                   .replace(")", "")
                   .replace("%", "percent")
            for col in df.columns
        }
        sanitized_df = df.rename(columns=sanitized_columns)

        # Properly quote column names
        columns = ", ".join([f"[{col}]" for col in sanitized_columns.values()])
        placeholders = ", ".join([f":{col}" for col in sanitized_columns.values()])
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        # Convert sanitized DataFrame to a list of dictionaries (rows)
        rows = [
            {sanitized_columns[col]: value for col, value in row.items()}
            for row in df.to_dict(orient="records")
        ]

        # Debug: Print the generated query and rows
        # print(f"[ {datetime.now()} ]-------- Executing bulk insert:\n{insert_query}")
        # print(f"Rows to insert: {rows}")

        # Perform the bulk insert
        engine = create_engine(connection_string)
        with engine.connect() as conn:
            conn.execute(text(insert_query), rows)
            conn.commit()
        print(f"[ {datetime.now()} ]-------- Data inserted successfully into '{table_name}'.")
    except Exception as e:
        print(f"[ {datetime.now()} ]-------- Error during bulk insert: {e}")
        raise


def get_highest_timestamp(connection_string):
    """
    Retrieve the highest `last_processed_time` from the metadata table.

    Args:
        connection_string (str): SQL Server connection string.

    Returns:
        str: The highest timestamp in `YYYYMMDD_HHMMSS` format or None if no records exist.
    """
    try:
        engine = create_engine(connection_string)
        query = text("""
            SELECT MAX(last_processed_time) AS max_timestamp
            FROM DataProcessingMetadata;
        """)
        with engine.connect() as conn:
            result = conn.execute(query).scalar()
            if result:
                # Convert timestamp to directory format: 'YYYYMMDD_HHMMSS'
                return result.strftime('%Y%m%d_%H%M%S')
            return None
    except Exception as e:
        print(f"[ {datetime.now()} ]-------- Error retrieving highest timestamp: {e}")
        raise
    

def transform_bronze_to_silver_with_metadata(bronze_dir, parent_file_path, connection_string=SQL_SERVER_CONNECTION_STRING):
    """
    Process data from the Bronze layer to the Silver layer using metadata for incremental loading,
    and handle invalid rows by saving them in an 'invalids' subdirectory.

    Args:
        bronze_dir (str): Path to the Bronze directory containing Parquet files.
        parent_file_path (str): Path to the original Excel file.
        connection_string (str): SQL Server connection string.
    """
    try:
        # Get the highest timestamp from metadata
        highest_timestamp = get_highest_timestamp(connection_string)
        print(f"[ {datetime.now()} ]-------- Highest processed timestamp: {highest_timestamp}")

        timestamped_dirs = os.listdir(bronze_dir)

        # Filter directories by timestamp
        if highest_timestamp:
            timestamped_dirs = [
                dir_name for dir_name in timestamped_dirs
                if dir_name > highest_timestamp and os.path.isdir(os.path.join(bronze_dir, dir_name))
            ]

        for timestamp_dir in timestamped_dirs:
            dir_path = os.path.join(bronze_dir, timestamp_dir)
            print(f"[ {datetime.now()} ]-------- Processing directory: {dir_path}")

            for file_name in os.listdir(dir_path):
                if file_name.endswith('.parquet'):
                    try:
                        file_path = os.path.join(dir_path, file_name)
                        table_name = os.path.splitext(file_name)[0].replace(" ", "_").lower()

                        # Load data
                        df = pd.read_parquet(file_path)
                        model = get_pydantic_model_for_table(table_name)                
                        valid_rows = split_and_handle_invalid_rows_generic(df, model, table_name, dir_path)

                        if valid_rows.empty:
                            print(f"[ {datetime.now()} ]-------- All rows in '{file_name}' are invalid. Skipping table '{table_name}'.")
                            continue

                        # Load data row count
                        row_count = len(valid_rows)

                        # Check if already processed
                        if is_sheet_processed(parent_file_path, table_name, row_count, connection_string):
                            print(f"[ {datetime.now()} ]------------------- Skipping {table_name} from {file_name}: already processed.")
                            continue

                        # Ensure the table exists
                        ensure_table_exists(valid_rows, table_name, connection_string)

                        # Insert valid data
                        bulk_insert(valid_rows, table_name, connection_string)

                        # Update metadata
                        update_metadata(parent_file_path, table_name, row_count, connection_string)

                    except Exception as file_error:
                        print(f"[ {datetime.now()} ]-------- Error processing file {file_name}: {file_error}")
                        continue

    except Exception as e:
        print(f"[ {datetime.now()} ]-------- Error processing Bronze to Silver: {e}")
        raise
