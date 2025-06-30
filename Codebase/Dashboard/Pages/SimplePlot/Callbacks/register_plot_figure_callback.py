from dash import Input, Output, State, dcc, ctx, no_update
from dash.exceptions import PreventUpdate
from Codebase.Dashboard.Pages.SimplePlot.Formating.format_timeseries_figure import format_timeseries_figure
from Codebase.Dashboard.SupportMethods.parse_special_value import parse_special_value
from Codebase.DataManager.data_loader import DataLoader
import pandas as pd
from functools import reduce

from Codebase.Dashboard.Pages.SimplePlot.Callbacks.PlotUtils.restore_loader import restore_loader
from Codebase.Dashboard.Pages.SimplePlot.Callbacks.PlotUtils.extract_df import extract_df
from Codebase.Dashboard.Pages.SimplePlot.Callbacks.PlotUtils.resample_grouping import resample_grouping
from Codebase.Dashboard.Pages.SimplePlot.Callbacks.PlotUtils.detect_lcd_groupings import detect_lcd_groupings
from Codebase.Dashboard.Pages.SimplePlot.Callbacks.PlotUtils.compute_time_range import compute_time_range
from Codebase.Dashboard.Pages.SimplePlot.Callbacks.PlotUtils.apply_outlier_filter import apply_outlier_filter
from Codebase.Dashboard.Pages.SimplePlot.Callbacks.PlotUtils.compute_shared_y_axis_ranges import compute_shared_yaxis_ranges
from Codebase.Dashboard.Pages.SimplePlot.Callbacks.PlotUtils.apply_extra_transform import apply_extra_transform


def register_plot_figure_callback(app):
    @app.callback(
        Output("plot-container", "children"),
        Output("plot-data-store", "data"),
        Output("time-grouping-y1", "value"),
        Output("time-grouping-y2", "value"),
        Output("time-grouping-y3", "value"),
        Input("dropdown-1", "value"),
        Input("dropdown-2", "value"),
        Input("dropdown-3", "value"),
        Input("conditional-1", "value"),
        Input("conditional-2", "value"),
        Input("conditional-3", "value"),
        Input("dropdown-special-1", "value"),
        Input("dropdown-special-2", "value"),
        Input("dropdown-special-3", "value"),
        Input("plot-title-input", "value"),
        Input("y1-axis-input", "value"),
        Input("y2-axis-input", "value"),
        Input("y3-axis-input", "value"),
        Input("date-range-picker", "start_date"),
        Input("date-range-picker", "end_date"),
        Input("time-grouping-y1", "value"),
        Input("time-grouping-y2", "value"),
        Input("time-grouping-y3", "value"),
        # ✅ Moved these up
        Input("extra-transform-y1", "value"),
        Input("extra-transform-y2", "value"),
        Input("extra-transform-y3", "value"),
        Input("outlier-filter-y1", "value"),
        Input("outlier-filter-y2", "value"),
        Input("outlier-filter-y3", "value"),
        Input("lcd-sync-button", "n_clicks"),
        Input("link-axes-dropdown", "value"),
        State("loader-store", "data"),
        prevent_initial_call=True
    )
    def generate_plot(
            y1_type, y2_type, y3_type,
            y1_col, y2_col, y3_col,
            y1_special, y2_special, y3_special,
            plot_title, y1_label, y2_label, y3_label,
            start_date, end_date,
            tg_y1, tg_y2, tg_y3,
            y1_extra, y2_extra, y3_extra,  # ✅ Corrected order
            f_y1, f_y2, f_y3,
            lcd_clicks, linked_axes,
            loader_state
    ):
        triggered_id = ctx.triggered_id
        roles = {
            "y1": (y1_type, y1_col, y1_special),
            "y2": (y2_type, y2_col, y2_special),
            "y3": (y3_type, y3_col, y3_special),
        }
        filters = {"y1": f_y1, "y2": f_y2, "y3": f_y3}
        time_groupings = {"y1": tg_y1, "y2": tg_y2, "y3": tg_y3}
        grouping_metadata = {}

        if not any([(y1_type and y1_col), (y2_type and y2_col), (y3_type and y3_col)]):
            raise PreventUpdate

        try:
            loader = restore_loader(loader_state, list(roles.values()))
        except Exception as e:
            return f"[ERROR] Failed to restore loader: {e}", no_update, no_update, no_update, no_update

        if triggered_id == "lcd-sync-button":
            base_by_role, lcd = detect_lcd_groupings(roles, loader)
            grouping_map = {
                1: "1S", 5: "5S", 10: "10S", 30: "30S",
                60: "1min", 300: "5min", 900: "15min",
                3600: "1H", 86400: "1D"
            }
            closest_grouping = next((v for k, v in grouping_map.items() if lcd and lcd <= k), "raw")
            for role in base_by_role:
                time_groupings[role] = closest_grouping
                grouping_metadata[role] = {
                    "base": f"{base_by_role[role]}s",
                    "blocked": closest_grouping
                }

        for role, (dtype, col, special) in roles.items():
            dfs = extract_df(loader, dtype, col, special, role_label=role)
            if not dfs:
                continue
            df = pd.concat(dfs)
            df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce").dt.tz_localize(None)
            df = df.dropna(subset=["datetime"]).sort_values("datetime")

            if len(df) >= 2:
                diffs = df["datetime"].diff().dt.total_seconds().dropna()
                diffs = diffs[diffs > 0.1]
                if not diffs.empty:
                    base = int(round(diffs.min()))
                    grouping_metadata[role] = {
                        "base": f"{base}s",
                        "blocked": time_groupings[role]
                    }

        df_final = None
        timestamp_ranges = []

        for role, (dtype, col, special) in roles.items():
            if not dtype or not col:
                continue

            dfs = extract_df(loader, dtype, col, special, role_label=role)
            if not dfs:
                continue

            df = pd.concat(dfs)
            df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce").dt.tz_localize(None)
            df = df.dropna(subset=["datetime"])

            # ✅ Apply filters and transforms in correct order
            df = apply_outlier_filter(df, filters[role])
            transform_type = {"y1": y1_extra, "y2": y2_extra, "y3": y3_extra}[role]
            print(f"[DEBUG] Transform type for {role}: {transform_type}")
            if transform_type and transform_type.lower() != "none":
                df = apply_extra_transform(df, transform_type)

            df = resample_grouping(df, time_groupings[role])
            trange = compute_time_range(df)
            if trange:
                timestamp_ranges.append(trange)

            if df_final is None:
                df_final = df
            else:
                df_final = pd.merge(df_final, df, how="outer", on="datetime")

        if df_final is None or df_final.empty:
            return "[WARN] No data found for plotting.", no_update, no_update, no_update, no_update

        df_final = df_final.sort_values("datetime")
        if start_date and end_date:
            start_dt = pd.to_datetime(start_date)
            end_dt = pd.to_datetime(end_date)
            df_final = df_final[
                (df_final["datetime"] >= start_dt) &
                (df_final["datetime"] <= end_dt)
            ]

        shared_ranges = compute_shared_yaxis_ranges(df_final, linked_axes)

        fig = format_timeseries_figure(
            df_final,
            y1_col=next((col for col in df_final.columns if col.startswith("y1::")), None),
            y2_col=next((col for col in df_final.columns if col.startswith("y2::")), None),
            y3_col=next((col for col in df_final.columns if col.startswith("y3::")), None),
            x_col="datetime",
            plot_title=plot_title or "Time Series Data",
            y1_label=y1_label or "Y1 Axis",
            y2_label=y2_label or "Y2 Axis",
            y3_label=y3_label or "Y3 Axis",
            grouping_info=grouping_metadata,
            shared_ranges=shared_ranges
        )

        return (
            dcc.Graph(figure=fig),
            {"ranges": timestamp_ranges},
            time_groupings["y1"],
            time_groupings["y2"],
            time_groupings["y3"]
        )
