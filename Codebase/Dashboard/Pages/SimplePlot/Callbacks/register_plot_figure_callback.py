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


        State("loader-store", "data"),
        prevent_initial_call=True
    )
    def generate_plot(y1_type, y2_type, y3_type,
                      y1_col, y2_col, y3_col,
                      y1_special, y2_special, y3_special,
                      plot_title, y1_label, y2_label,
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
                instance_id, special_key = parse_special_value(y1_special)
                loader.load_data(csv_category=y1_type, instance_id=instance_id, set_of_columns={y1_col})

            if y2_type and y2_col:
                instance_id, special_key = parse_special_value(y2_special)
                loader.load_data(csv_category=y2_type, instance_id=instance_id, set_of_columns={y2_col})

            if y3_type and y3_col:
                instance_id, special_key = parse_special_value(y3_special)
                loader.load_data(csv_category=y3_type, instance_id=instance_id, set_of_columns={y3_col})

            print(f"[DEBUG] loader.data keys after load: {loader.data.keys()}")
            print(f"[DEBUG] loader.data[{y1_type}] = {loader.data.get(y1_type)}")

        except Exception as e:
            print(f"[ERROR] Loader restoration failed: {e}")
            return f"[ERROR] Failed to restore loader: {e}"

        def extract_df(data_type, col, special):
            if not data_type or not col:
                return None
            if data_type not in loader.data:
                return None

            frames = []
            for instance_id, instance in loader.data[data_type].items():
                # Priority 1: exact match on special key
                if special and special in instance:
                    for df in instance[special]["data"]:
                        if col in df.columns:
                            frames.append(df[["datetime", col]])
                else:
                    # Fallback: use all subkeys (like "unknown")
                    for subkey, subdict in instance.items():
                        for df in subdict["data"]:
                            if col in df.columns:
                                frames.append(df[["datetime", col]])
            return frames

        roles = {
            "y1": (y1_type, y1_col, y1_special),
            "y2": (y2_type, y2_col, y2_special),
            "y3": (y3_type, y3_col, y3_special)
        }

        df_final = None
        for role, (dtype, col, special) in roles.items():
            if dtype and col:
                dfs = extract_df(dtype, col, special)
                if dfs:
                    df_concat = pd.concat(dfs).drop_duplicates(subset="datetime")
                    df_concat = df_concat.set_index("datetime")
                    df_concat.columns = [role]
                    df_final = df_concat if df_final is None else df_final.join(df_concat, how="outer")

        if df_final is None or df_final.empty:
            print("[WARN] Final dataframe is empty after merge")
            return "[WARN] No data found for plotting."

        df_final = df_final.reset_index().sort_values("datetime")
        print(f"[DEBUG] Final dataframe shape: {df_final.shape}")

        fig = format_timeseries_figure(
            df_final,
            y1_col="y1" if "y1" in df_final.columns else None,
            y2_col="y2" if "y2" in df_final.columns else None,
            y3_col="y3" if "y3" in df_final.columns else None,
            x_col="datetime",
            plot_title=plot_title or "Time Series Data",
            y1_label=y1_label or "Y1 Axis",
            y2_label=y2_label or "Y2 Axis"
        )

        return dcc.Graph(figure=fig)
