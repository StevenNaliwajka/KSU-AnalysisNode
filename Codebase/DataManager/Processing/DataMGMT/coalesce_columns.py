def coalesce_columns(df):
    """
    Merge columns like 'drssi_x', 'drssi_y' into a single 'drssi',
    and drop the original suffixed columns.
    """
    from collections import defaultdict
    import re

    # Group columns by base name (without _x, _y, _z...)
    col_groups = defaultdict(list)
    for col in df.columns:
        match = re.match(r"^(.*?)(?:_[xyz])?$", col)
        if match:
            base = match.group(1)
            col_groups[base].append(col)

    for base_col, variants in col_groups.items():
        if len(variants) > 1:
            # Coalesce into one column
            df[base_col] = df[variants].bfill(axis=1).iloc[:, 0]
            df.drop(columns=[v for v in variants if v != base_col], inplace=True)

    return df