from dash import Input, Output, State
from dash.exceptions import PreventUpdate

def ensure_data_is_loaded(app, dropdown_id):
    @app.callback(
        Output("loader-store", "data", allow_duplicate=True),  # allow overwriting loader
        Input(dropdown_id, "value"),
        State("loader-store", "data"),
        prevent_initial_call=True
    )
    def load_data_if_needed(data_type, loader_state):
        if not data_type or data_type.lower() not in {"soil", "tvws"}:
            raise PreventUpdate

        from Codebase.DataManager.data_loader import DataLoader
        try:
            loader = DataLoader.from_cached_state(
                dropdown_blacklist=loader_state.get("dropdown_blacklist", []),
                data_types_available=loader_state.get("data_types_available", []),
                column_list_by_type=loader_state.get("column_list_by_type", {}),
                all_csv_files=loader_state.get("all_csv_files", [])
            )
        except Exception as e:
            print(f"[ERROR] Failed to restore loader: {e}")
            raise PreventUpdate

        # Check if already loaded
        if data_type in loader.data and loader.data[data_type]:
            # print(f"[DEBUG] Data for '{data_type}' already loaded.")
            raise PreventUpdate

        columns = set(loader.column_list_by_type.get(data_type, []))
        if not columns:
            # print(f"[WARN] No columns found for type '{data_type}'")
            raise PreventUpdate

        # print(f"[INFO] Loading data for '{data_type}'...")
        loader.load_data(data_type, instance_id=0, set_of_columns=columns)

        return {
            "dropdown_blacklist": loader.blacklist,
            "data_types_available": sorted(loader.data_types_available),
            "column_list_by_type": loader.column_list_by_type,
            "all_csv_files": [str(p) for p in loader.all_csv_files],
        }
