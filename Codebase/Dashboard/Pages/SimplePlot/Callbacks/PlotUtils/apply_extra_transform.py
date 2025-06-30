import pandas as pd

def apply_extra_transform(df: pd.DataFrame, transform_type: str) -> pd.DataFrame:
    col_name = next((col for col in df.columns if col != "datetime"), None)
    if not col_name:
        return df

    if transform_type == "c_to_f":
        df[col_name] = df[col_name] * 9 / 5 + 32
    elif transform_type == "f_to_c":
        df[col_name] = (df[col_name] - 32) * 5 / 9
    elif transform_type == "log10":
        df[col_name] = df[col_name].apply(lambda x: np.log10(x) if x > 0 else np.nan)
    elif transform_type == "invert":
        df[col_name] = df[col_name].apply(lambda x: 1 / x if x != 0 else np.nan)

    return df
