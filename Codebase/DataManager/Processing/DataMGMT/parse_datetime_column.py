import pandas as pd

def parse_datetime_column(csv_path: str, df: pd.DataFrame) -> pd.Series:
    """Parse and return a datetime Series from a DataFrame, using multiple rules."""
    cols = [col.strip().lower() for col in df.columns]

    # Option 1: Combine date + time
    if "date (year-mon-day)" in cols and "time (hour-min-sec)" in cols:
        date_col = df.columns[cols.index("date (year-mon-day)")]
        time_col = df.columns[cols.index("time (hour-min-sec)")]
        time_str = df[time_col].astype(str).str.replace("-", ":", regex=False)
        combined = df[date_col].astype(str) + " " + time_str
        parsed = pd.to_datetime(combined, errors="coerce")
        # print(f"[DEBUG] Parsed 'date + time' in {csv_path}: {parsed.dropna().min()} to {parsed.dropna().max()}")
        return parsed

    # Option 2: Simple date
    elif "simple date" in cols:
        col = df.columns[cols.index("simple date")]
        parsed = pd.to_datetime(df[col], errors="coerce")
        # print(f"[DEBUG] Parsed 'simple date' in {csv_path}: {parsed.dropna().min()} to {parsed.dropna().max()}")
        return parsed

    # Option 3: Fallback
    for col in df.columns:
        try:
            parsed = pd.to_datetime(df[col], errors="coerce")
            if parsed.notna().sum() > len(df) * 0.8:
                # print(f"[DEBUG] Parsed fallback '{col}' in {csv_path}: {parsed.dropna().min()} to {parsed.dropna().max()}")
                return parsed
        except Exception:
            continue

    print(f"[ERROR] Failed to parse datetime in {csv_path}")
    return pd.Series(pd.NaT, index=df.index)
