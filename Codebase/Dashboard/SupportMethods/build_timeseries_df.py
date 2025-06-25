from pandas import concat

def build_timeseries_df(loader, selected_settings: list):
    """
    Args:
        loader: DataLoader instance
        selected_settings: list of dicts like:
            [{"type": "soil", "special": "-3", "column": "soil moisture value"}]
    """
    dfs = []
    for setting in selected_settings:
        dtype = setting["type"]
        special = setting["special"]
        col = setting["column"]

        for df in loader.data.get(dtype, {}).get(special, {}).get("data", []):
            if col in df.columns:
                temp = df[["datetime", col]].copy()
                temp = temp.rename(columns={col: f"{dtype}::{col}::{special}"})
                dfs.append(temp)

    if not dfs:
        return None

    merged_df = dfs[0]
    for df in dfs[1:]:
        merged_df = merged_df.merge(df, on="datetime", how="outer")

    return merged_df
