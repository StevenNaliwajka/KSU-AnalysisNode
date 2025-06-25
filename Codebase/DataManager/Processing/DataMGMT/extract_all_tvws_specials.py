import pandas as pd
import re

def extract_all_tvws_specials(csv_paths):
    found = []
    for path in csv_paths:
        try:
            instance_match = re.search(r"[-_](\-?\d+)[-_]", path.name)
            if not instance_match:
                continue
            instance_id = int(instance_match.group(1))

            df = pd.read_csv(path, nrows=2, header=None)
            if df.shape[1] >= 9:
                special = str(df.iloc[1, 8]).strip()
                found.append((instance_id, special))
        except Exception:
            continue
    return sorted(set(found))  # remove duplicates
