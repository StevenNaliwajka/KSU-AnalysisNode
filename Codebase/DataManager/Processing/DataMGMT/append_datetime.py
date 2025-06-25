import pandas as pd

def append_datetime(csv_path: str, df: pd.DataFrame) -> pd.DataFrame:
    """Ensure a 'datetime' column exists in df, filling missing values if it already exists."""
    existing_datetime = df["datetime"] if "datetime" in df.columns else pd.Series(pd.NaT, index=df.index)
    cols = [col.strip().lower() for col in df.columns]

    new_datetime = pd.Series(pd.NaT, index=df.index)  # Default fallback

    # Option 1: Combine 'date + time' columns
    if "date (year-mon-day)" in cols and "time (hour-min-sec)" in cols:
        date_col = df.columns[cols.index("date (year-mon-day)")]
        time_col = df.columns[cols.index("time (hour-min-sec)")]
        time_str = df[time_col].astype(str).str.replace("-", ":", regex=False)
        combined = df[date_col].astype(str) + " " + time_str
        new_datetime = pd.to_datetime(combined, errors="coerce")
        print(f"[DEBUG] Parsed 'date + time' into datetime in {csv_path}: {new_datetime.dropna().min()} to {new_datetime.dropna().max()}")

    # Option 2: Use 'simple date'
    elif "simple date" in cols:
        simple_col = df.columns[cols.index("simple date")]
        new_datetime = pd.to_datetime(df[simple_col], errors="coerce")
        print(f"[DEBUG] Parsed 'simple date' into datetime in {csv_path}: {new_datetime.dropna().min()} to {new_datetime.dropna().max()}")

    # Option 3: Fallback auto-detect
    else:
        for col in df.columns:
            try:
                parsed = pd.to_datetime(df[col], errors="coerce")
                if parsed.notna().sum() > len(df) * 0.8:
                    new_datetime = parsed
                    print(f"[DEBUG] Fallback parsed '{col}' into datetime in {csv_path}: {parsed.dropna().min()} to {parsed.dropna().max()}")
                    break
            except Exception:
                continue

    # Merge new_datetime into existing_datetime where missing
    combined_datetime = existing_datetime.combine_first(new_datetime)
    df["datetime"] = combined_datetime

    if combined_datetime.isna().any():
        print(f"[WARNING] Some rows in {csv_path} still have NaT in 'datetime'")
    return df
