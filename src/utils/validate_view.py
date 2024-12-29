from datetime import datetime
import os
import pandas as pd
from pydantic import ValidationError


def split_and_handle_invalid_rows_generic(df, model, table_name, batch_dir):
    """
    Split DataFrame into valid and invalid rows, save invalid rows to a Parquet file.

    Args:
        df (pd.DataFrame): DataFrame to split.
        table_name (str): Name of the table (for file naming).
        batch_dir (str): Path to the batch directory where valid data is stored.

    Returns:
        pd.DataFrame: Valid rows for database insertion.
    """
    try:
        valid_rows = []
        invalid_rows = []
        
        # Sanitize column names
        sanitized_columns = {
                            col: col.replace(" ", "_")
                                .replace("(", "")
                                .replace(")", "")
                                .replace("%", "percent").lower()
                            for col in df.columns
                        }
        df = df.rename(columns=sanitized_columns)

        for _, row in df.iterrows():
            try:
                valid_rows.append(model(**row.to_dict()).dict())
            except ValidationError as e:
                invalid_row = row.to_dict()
                invalid_row["errors"] = str(e)
                invalid_rows.append(invalid_row)

        valid_df = pd.DataFrame(valid_rows)
        invalid_df = pd.DataFrame(invalid_rows)

        if not invalid_df.empty:
            invalids_dir = os.path.join(batch_dir, "invalids")
            os.makedirs(invalids_dir, exist_ok=True)
            invalid_file_path = os.path.join(invalids_dir, f"{table_name}_invalids.parquet")
            invalid_df.to_parquet(invalid_file_path, index=False)
            print(f"[ {datetime.now()} ] Invalid rows saved to: {invalid_file_path}")

        return valid_df

    except Exception as e:
        print(f"[ {datetime.now()} ] Error during row validation: {e}")
        raise
