import pandas as pd

def compute_shared_yaxis_ranges(df_final, linked_axes):
    y_ranges = {}
    for axis in ["y1", "y2", "y3"]:
        col = next((c for c in df_final.columns if c.startswith(f"{axis}::")), None)
        if col:
            y_ranges[axis] = df_final[col].dropna()

    shared_ranges = {}
    if linked_axes:
        for link_pair in linked_axes:
            if "-" not in link_pair:
                continue  # 🛡️ Skip malformed entry
            a1, a2 = link_pair.split("-")
            if a1 in y_ranges and a2 in y_ranges:
                combined = pd.concat([y_ranges[a1], y_ranges[a2]])
                shared_min = combined.min()
                shared_max = combined.max()
                shared_ranges[a1] = (shared_min, shared_max)
                shared_ranges[a2] = (shared_min, shared_max)

    return shared_ranges
