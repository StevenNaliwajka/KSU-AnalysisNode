from dash import Input, Output, State, dcc
from dash.exceptions import PreventUpdate
from Codebase.Dashboard.Pages.SimplePlot.Formating.format_timeseries_figure import format_timeseries_figure
from Codebase.Dashboard.SupportMethods.parse_special_value import parse_special_value
from Codebase.DataManager.data_loader import DataLoader
import pandas as pd

def register_plot_figure_callback(app):
    @app.callback(
        Output("plot-container", "children"),
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
        Input("time-grouping-dropdown", "value"),
        State("loader-store", "data"),
        prevent_initial_call=True
    )
    def generate_plot(y1_type, y2_type, y3_type,
                      y1_col, y2_col, y3_col,
                      y1_special, y2_special, y3_special,
                      plot_title, y1_label, y2_label,
                      time_grouping,
                      loader_state):

        print("[DEBUG] Plot Triggered with Inputs:")
        for label, val in zip(
            ["y1_type", "y2_type", "y3_type", "y1_col", "y2_col", "y3_col", "y1_special", "y2_special", "y3_special"],
            [y1_type, y2_type, y3_type, y1_col, y2_col, y3_col, y1_special, y2_special, y3_special]
        ):
            print(f"    {label} = {val}")
        print(f"    loader keys = {list(loader_state.keys()) if loader_state else 'None'}")

        if not any([(y1_type and y1_col), (y2_type and y2_col), (y3_type and y3_col)]):
            raise PreventUpdate

        try:
            loader = DataLoader.from_cached_state(
                dropdown_blacklist=loader_state.get("dropdown_blacklist", []),
                data_types_available=loader_state.get("data_types_available", []),
                column_list_by_type=loader_state.get("column_list_by_type", {}),
                all_csv_files=loader_state.get("all_csv_files", [])
            )
            print("[DEBUG] Loader restored successfully")

            if y1_type and y1_col:
                instance_id, _ = parse_special_value(y1_special)
                loader.load_data(csv_category=y1_type, instance_id=instance_id, set_of_columns={y1_col})

            if y2_type and y2_col:
                instance_id, _ = parse_special_value(y2_special)
                loader.load_data(csv_category=y2_type, instance_id=instance_id, set_of_columns={y2_col})

            if y3_type and y3_col:
                instance_id, _ = parse_special_value(y3_special)
                loader.load_data(csv_category=y3_type, instance_id=instance_id, set_of_columns={y3_col})

            print(f"[DEBUG] loader.data keys after load: {loader.data.keys()}")
            print(f"[DEBUG] loader.data[{y1_type}] = {loader.data.get(y1_type)}")

        except Exception as e:
            print(f"[ERROR] Loader restoration failed: {e}")
            return f"[ERROR] Failed to restore loader: {e}"

        def extract_df(data_type, col, special, role_label=None):
            if not data_type or not col:
                return None
            if data_type not in loader.data:
                return None
            if data_type in ["tvws", "soil"] and not special:
                return None

            special_instance_id, _ = parse_special_value(special)
            frames = []

            for instance_id, instance in loader.data[data_type].items():
                if data_type in ["tvws", "soil"] and str(special_instance_id) not in str(instance_id):
                    continue

                for subkey, subdict in instance.items():
                    for df in subdict["data"]:
                        if col in df.columns:
                            safe_label = f"{role_label}::{col}::{instance_id or 'unknown'}"
                            temp = df[["datetime", col]].copy()
                            temp = temp.rename(columns={col: safe_label})
                            frames.append(temp)

            return frames if frames else None

        roles = {
            "y1": (y1_type, y1_col, y1_special),
            "y2": (y2_type, y2_col, y2_special),
            "y3": (y3_type, y3_col, y3_special)
        }

        df_final = None
        for role, (dtype, col, special) in roles.items():
            if not dtype or not col:
                continue

            dfs = extract_df(dtype, col, special, role_label=role)
            if not dfs or len(dfs) == 0:
                print(f"[WARN] No dataframes returned for {role} (type: {dtype}, col: {col}, special: {special})")
                continue

            df_concat = pd.concat(dfs)
            df_concat = df_concat.dropna(subset=["datetime"])
            df_concat = df_concat.drop_duplicates(subset=["datetime", *df_concat.columns.difference(["datetime"])])
            if df_final is None:
                df_final = df_concat
            else:
                df_final = pd.merge(df_final, df_concat, how="outer", on="datetime")

            print(f"[DEBUG] After merging {role}: {df_concat.columns.tolist()}")

        if df_final is None or df_final.empty:
            print("[WARN] Final dataframe is empty after merge")
            return "[WARN] No data found for plotting."

        df_final = df_final.reset_index().sort_values("datetime")

        if time_grouping and time_grouping != "raw":
            try:
                df_final = df_final.set_index("datetime")
                df_final = df_final.resample(time_grouping).mean().dropna(how="all")
                df_final = df_final.reset_index()
                print(f"[DEBUG] Applied time grouping: {time_grouping}")
            except Exception as e:
                print(f"[ERROR] Failed to apply time grouping '{time_grouping}': {e}")
                return f"[ERROR] Time grouping error: {e}"

        print(f"[DEBUG] Final dataframe shape: {df_final.shape}")

        fig = format_timeseries_figure(
            df_final,
            y1_col=next((col for col in df_final.columns if col.startswith("y1::")), None),
            y2_col=next((col for col in df_final.columns if col.startswith("y2::")), None),
            y3_col=next((col for col in df_final.columns if col.startswith("y3::")), None),
            x_col="datetime",
            plot_title=plot_title or "Time Series Data",
            y1_label=y1_label or "Y1 Axis",
            y2_label=y2_label or "Y2 Axis"
        )

        return dcc.Graph(figure=fig)
