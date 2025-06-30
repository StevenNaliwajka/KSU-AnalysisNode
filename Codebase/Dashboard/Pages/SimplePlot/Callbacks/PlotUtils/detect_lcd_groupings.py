import pandas as pd

from functools import reduce

from Codebase.Dashboard.Pages.SimplePlot.Callbacks.PlotUtils.extract_df import extract_df


def detect_lcd_groupings(roles, loader):
    base_by_role = {}
    detected_intervals = []

    for role, (dtype, col, special) in roles.items():
        dfs = extract_df(loader, dtype, col, special, role_label=role)
        if not dfs:
            continue
        df = pd.concat(dfs).dropna()
        df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce").dt.tz_localize(None)
        df = df.sort_values("datetime")
        if len(df) >= 2:
            diffs = df["datetime"].diff().dt.total_seconds().dropna()
            diffs = diffs[diffs > 0.1]
            if not diffs.empty:
                sec = int(round(diffs.min()))
                base_by_role[role] = sec
                detected_intervals.append(sec)

    def compute_lcd(values):
        def gcd_pair(x, y): return x if y == 0 else gcd_pair(y, x % y)
        def lcm_pair(x, y): return x * y // gcd_pair(x, y)
        return reduce(lcm_pair, values)

    lcd = compute_lcd(detected_intervals) if detected_intervals else None
    return base_by_role, lcd