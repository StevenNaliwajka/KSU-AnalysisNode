import pandas as pd
import logging

def scan_unique_headers_by_type(train_dir, loader, files_to_scan=None):
    """
    Scan CSV files and store unique non-time headers grouped by filename
    into loader.header_list_by_type
    """
    loader.header_list_by_type = {}
    files = files_to_scan if files_to_scan is not None else sorted(train_dir.rglob("*.csv"))

    for f in files:
        try:
            header_line = 2 if "ambient-weather" not in f.name.lower() else 1
            df = loader.read_csv(f, header_line=header_line)

            # Normalize datetime column
            if "date" in df.columns and "time" in df.columns:
                df["datetime"] = pd.to_datetime(df["date"] + " " + df["time"], utc=True, errors='coerce')
            elif "date" in df.columns:
                df["datetime"] = pd.to_datetime(df["date"], utc=True, errors='coerce')
            else:
                try:
                    df["datetime"] = pd.to_datetime(df.iloc[:, 0], utc=True, errors='coerce')
                except:
                    df["datetime"] = None

            # Filter columns
            relevant_cols = [
                col for col in df.columns
                if not col.lower().startswith("date")
                and not col.lower().startswith("time")
                and col != "datetime"
            ]

            loader.header_list_by_type[str(f.name)] = sorted(set(relevant_cols))

        except Exception as e:
            logging.exception(f"[Header Scan Error] {f.name}: {e}")
