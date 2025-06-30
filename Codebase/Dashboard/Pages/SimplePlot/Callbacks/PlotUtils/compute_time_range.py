import pandas as pd

def compute_time_range(df):
    dt_min = df["datetime"].min()
    dt_max = df["datetime"].max()
    if pd.notna(dt_min) and pd.notna(dt_max):
        return {
            "min": dt_min.strftime("%Y-%m-%d"),
            "max": dt_max.strftime("%Y-%m-%d")
        }
    return None