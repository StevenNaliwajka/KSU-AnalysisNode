from dash import Input, Output, State
from dash.exceptions import PreventUpdate

from Codebase.DataManager.Processing.Header.normalize_header import normalize_header
from Codebase.DataManager.data_loader import DataLoader

def make_conditional_dropdown_callback(app, dropdown_id, special_id, conditional_id):
    @app.callback(
        Output(conditional_id, "options"),
        Output(conditional_id, "value"),
        Input(dropdown_id, "value"),
        State("loader-store", "data"),
        prevent_initial_call=True,
        allow_missing=True
    )
    def conditional_display(selected_type, loader_state):
        if not loader_state:
            raise PreventUpdate

        try:
            loader = DataLoader.from_cached_state(
                dropdown_blacklist=loader_state.get("dropdown_blacklist", []),
                data_types_available=loader_state.get("data_types_available", []),
                column_list_by_type=loader_state.get("column_list_by_type", {}),
                all_csv_files=loader_state.get("all_csv_files", [])
            )
        except Exception as e:
            print(f"[ERROR] Failed to rebuild loader: {e}")
            return [], None

        selected_type = (selected_type or "").lower()
        if selected_type not in loader.column_list_by_type:
            return [], None

        options = [
            {"label": col.title(), "value": normalize_header(col)}
            for col in loader.column_list_by_type[selected_type]
        ]

        default_value = options[0]["value"] if options else None
        return options, default_value
