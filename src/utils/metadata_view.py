from datetime import datetime
from sqlalchemy import create_engine, text
from .db_param_view import SQL_SERVER_CONNECTION_STRING

def is_sheet_processed(parent_file_path, sheet_name, row_count, connection_string=SQL_SERVER_CONNECTION_STRING):
    """
    Check if a file and sheet have already been processed.

    Args:
        file_name (str): Name of the file.
        sheet_name (str): Name of the sheet.
        row_count (int): Number of rows in the sheet.
        connection_string (str): SQL Server connection string.

    Returns:
        bool: True if the sheet has been processed, False otherwise.
    """
    try:
        engine = create_engine(connection_string)

        # Construct query using string interpolation to avoid parameterized queries
        query = f"""
            SELECT 1
            FROM DataProcessingMetadata
            WHERE file_name = '{parent_file_path}'
              AND sheet_name = '{sheet_name}'
              AND row_count = {row_count};
        """

        with engine.connect() as conn:
            # Execute the query
            result = conn.execute(text(query)).fetchone()
            return result is not None

    except Exception as e:
        print(f"[ {datetime.now()} ]-------- Error checking metadata: {e}")
        raise


def update_metadata(file_name, sheet_name, row_count, connection_string=SQL_SERVER_CONNECTION_STRING):
    """
    Update the metadata table with processed file and sheet information.

    Args:
        file_name (str): Name of the file.
        sheet_name (str): Name of the sheet.
        row_count (int): Number of rows in the sheet.
        connection_string (str): SQL Server connection string.
    """
    try:
        current_time = datetime.now()

        # Use parameterized query
        query = text("""
            INSERT INTO DataProcessingMetadata (file_name, sheet_name, row_count, last_processed_time)
            VALUES (:file_name, :sheet_name, :row_count, :last_processed_time);
        """)

        engine = create_engine(connection_string)

        with engine.connect() as conn:
            # Debug the query being executed
            print(f"[ {datetime.now()} ]-------- Executing query: INSERT INTO DataProcessingMetadata")
            
            # Execute the query with Python datetime object
            conn.execute(query, {
                "file_name": file_name,
                "sheet_name": sheet_name,
                "row_count": row_count,
                "last_processed_time": current_time
            })
            conn.commit()  # Ensure transaction is committed if autocommit is off
        print(f"[ {datetime.now()} ]-------- Metadata updated successfully for file '{file_name}'.")
    except Exception as e:
        print(f"[ {datetime.now()} ]-------- Error updating metadata: {e}")
        raise