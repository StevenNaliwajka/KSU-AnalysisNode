from pathlib import Path

from Codebase.DataManager.data_loader import DataLoader
from Codebase.DataManager.Processing.DataMGMT.extract_all_soil_depths import extract_all_soil_depths
from Codebase.DataManager.Processing.DataMGMT.extract_all_tvws_specials import extract_all_tvws_specials

from dash import Input, Output, State
from dash.exceptions import PreventUpdate

def make_special_dropdown(app, dropdown_id, special_id):
    @app.callback(
        Output(special_id, "options"),
        Output(special_id, "style"),
        Input(dropdown_id, "value"),
        Input("loader-store", "data"),
        prevent_initial_call=True,
        allow_missing=True
    )
    def update_special_dropdown(data_type, loader_state):
        if not data_type or data_type not in {"soil", "tvws"}:
            return [], {"display": "none"}

        if not loader_state:
            raise PreventUpdate

        loader = DataLoader.from_cached_state(
            dropdown_blacklist=loader_state.get("dropdown_blacklist", []),
            data_types_available=loader_state.get("data_types_available", []),
            column_list_by_type=loader_state.get("column_list_by_type", {}),
            all_csv_files=loader_state.get("all_csv_files", [])
        )

        all_paths = [Path(p) for p in loader.all_csv_files]
        filtered = [p for p in all_paths if data_type in p.name.lower()]

        # Extract (instance, special) pairs
        if data_type == "soil":
            result = extract_all_soil_depths(filtered)
        elif data_type == "tvws":
            result = extract_all_tvws_specials(filtered)
        else:
            result = []

        # Convert into dropdown options
        options = [
            {"label": f"Instance {i}: {s}", "value": f"{i}|{s}"}
            for i, s in result
        ]

        # print(f"[DEBUG] Refreshed special dropdown for '{data_type}': {options}")
        return options, {"display": "block"}
