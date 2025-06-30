def apply_outlier_filter(df, role_filter):
    col_name = next((c for c in df.columns if c != "datetime"), None)
    if not col_name or not role_filter:
        return df
    series = df[col_name]

    if role_filter == "Remove Top 5%":
        return df[series <= series.quantile(0.95)]
    elif role_filter == "Remove Bottom 5%":
        return df[(series >= series.quantile(0.05)) & (series != 0)]
    elif role_filter == "Remove Top & Bottom 5%":
        lower = series.quantile(0.05)
        upper = series.quantile(0.95)
        return df[(series >= lower) & (series <= upper) & (series != 0)]
    return df