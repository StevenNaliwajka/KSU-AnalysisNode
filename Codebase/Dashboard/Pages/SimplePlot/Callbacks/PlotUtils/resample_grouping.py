def resample_grouping(df, grouping):
    if grouping == "raw":
        return df
    try:
        df = df.set_index("datetime").resample(grouping).mean().dropna(how="all").reset_index()
    except Exception:
        pass
    return df