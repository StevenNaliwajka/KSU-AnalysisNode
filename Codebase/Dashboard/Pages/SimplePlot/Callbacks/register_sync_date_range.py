from dash import Input, Output, State
from dash.exceptions import PreventUpdate
import datetime

def register_sync_date_range(app):
    @app.callback(
        Output("date-range-picker", "start_date"),
        Output("date-range-picker", "end_date"),
        Input("auto-sync-date-range-button", "n_clicks"),
        State("plot-data-store", "data"),
        prevent_initial_call=True
    )
    def sync_date_range(n_clicks, plot_data):
        if not plot_data or "ranges" not in plot_data:
            print("[SYNC] No ranges found in plot-data-store")
            raise PreventUpdate

        try:
            parsed_ranges = []
            for r in plot_data["ranges"]:
                if "min" in r and "max" in r:
                    parsed_ranges.append((
                        datetime.datetime.strptime(r["min"], "%Y-%m-%d"),
                        datetime.datetime.strptime(r["max"], "%Y-%m-%d")
                    ))

            if not parsed_ranges:
                print("[SYNC] No valid timestamp ranges to process")
                raise PreventUpdate

            latest_start = max(start for start, _ in parsed_ranges)
            earliest_end = min(end for _, end in parsed_ranges)

            if latest_start > earliest_end:
                print("[SYNC] No overlapping datetime between plotted series")
                raise PreventUpdate

            print(f"[SYNC] Computed overlap: {latest_start} to {earliest_end}")
            return latest_start.strftime("%Y-%m-%d"), earliest_end.strftime("%Y-%m-%d")

        except Exception as e:
            print(f"[ERROR] Failed to sync date range: {e}")
            raise PreventUpdate
