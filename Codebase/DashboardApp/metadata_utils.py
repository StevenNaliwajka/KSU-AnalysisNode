import pandas as pd

def extract_all_soil_depths(csv_paths):
    depths = set()
    for path in csv_paths:
        try:
            df = pd.read_csv(path, nrows=2, header=None)
            if df.shape[1] >= 2:
                depths.add(str(df.iloc[1, 1]))
        except Exception:
            continue
    return sorted(depths)

def extract_all_tvws_specials(csv_paths):
    specials = set()
    for path in csv_paths:
        try:
            df = pd.read_csv(path, nrows=2, header=None)
            if df.shape[1] >= 9:
                specials.add(str(df.iloc[1, 8]))
        except Exception:
            continue
    return sorted(specials)
