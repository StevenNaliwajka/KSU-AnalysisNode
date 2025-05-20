import pandas as pd

def parse_datetime(df):
    cols = [col.strip().lower() for col in df.columns]
    if "date (year-mon-day)" in cols and "time (hour-min-sec)" in cols:
        date_col = df.columns[cols.index("date (year-mon-day)")]
        time_col = df.columns[cols.index("time (hour-min-sec)")]
        time_str = df[time_col].astype(str).str.replace("-", ":", regex=False)
        return pd.to_datetime(df[date_col] + " " + time_str, errors="coerce")
    elif "simple date" in cols:
        simple_col = df.columns[cols.index("simple date")]
        return pd.to_datetime(df[simple_col], errors="coerce")
    return pd.Series(pd.NaT, index=df.index)
