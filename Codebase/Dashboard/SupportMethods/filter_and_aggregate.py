def filter_and_aggregate(df, y1, y2, y3, time_range, freq):
    # Select columns
    selected_cols = [col for col in [y1, y2, y3] if col != "__none__"]
    df = df[["datetime"] + selected_cols].dropna()

    # Filter by time range
    mask = (df["datetime"] >= time_range[0]) & (df["datetime"] <= time_range[1])
    df = df.loc[mask]

    # Set datetime as index and resample
    df = df.set_index("datetime").resample(freq).mean().reset_index()

    return df