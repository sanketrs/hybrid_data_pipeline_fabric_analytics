import os
import pandas as pd
from datetime import datetime

# Directory to store Parquet files for the Bronze layer
BRONZE_DIR = os.getenv('BRONZE_DIR')

def save_to_parquet(sheet_name: str, dataframe: pd.DataFrame, bronze_dir: str = BRONZE_DIR):
    """
    Save a DataFrame as a Parquet file in the Bronze directory.

    Args:
        sheet_name (str): Name of the sheet to save.
        dataframe (pd.DataFrame): DataFrame to save as a Parquet file.
        bronze_dir (str): Directory to save the Parquet files.
    """
    try:
        # Create a timestamped subdirectory
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        timestamped_dir = os.path.join(bronze_dir, timestamp)
        os.makedirs(timestamped_dir, exist_ok=True)

        # Define the file path
        file_path = os.path.join(timestamped_dir, f"{sheet_name.lower()}.parquet")

        # Save the DataFrame to a Parquet file
        dataframe.to_parquet(file_path, index=False)
        print(f"[ {datetime.now()} ]-------- Saved sheet '{sheet_name}' as Parquet file: {file_path}")
    except Exception as e:
        print(f"[ {datetime.now()} ]-------- Error saving sheet '{sheet_name}' to Parquet: {e}")

def extract_and_store_bronze(file_path: str, bronze_dir: str = BRONZE_DIR):
    """
    Extract all sheets from an Excel file and store them as Parquet files.

    Args:
        file_path (str): Path to the Excel file.
        bronze_dir (str): Directory to save the Parquet files.
    """
    try:
        # Read all sheets into a dictionary of DataFrames
        all_sheets = pd.read_excel(file_path, sheet_name=None)
        print(f"[ {datetime.now()} ]-------- Found {len(all_sheets)} sheet(s) in the Excel file.")

        # Save each sheet as a Parquet file
        for sheet_name, dataframe in all_sheets.items():
            # print(f"[ {datetime.now()} ]-------- Processing sheet: {sheet_name}")
            save_to_parquet(sheet_name, dataframe, bronze_dir)

        print(f"[ {datetime.now()} ]-------- All sheets stored in the Bronze layer as Parquet files.")
    except Exception as e:
        print(f"[ {datetime.now()} ]-------- Error during extraction and storage: {e}")
