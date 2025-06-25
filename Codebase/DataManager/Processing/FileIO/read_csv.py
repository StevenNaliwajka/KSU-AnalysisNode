import traceback

import pandas as pd

def read_csv(self, path, header_line=0):
    try:
        # print(f"[DEBUG] Reading {path} with header on line {header_line}")
        df = pd.read_csv(path, header=header_line, low_memory=False)
        df.columns = [col.strip().lower() for col in df.columns]
        # print(f"df colums : {df.columns}")
        return df
    except Exception as e:
        print(f"[ERROR] Failed to read {path}: {e}")
        traceback.print_exc()
        return None