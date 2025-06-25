from dash import Input, Output, State, dcc, no_update, html
from dash.exceptions import PreventUpdate

def populate_inital_dropdowns(app):
    @app.callback(
        Output("dropdown-1", "options"),
        Output("dropdown-2", "options"),
        Output("dropdown-3", "options"),
        Input("loader-store", "data")
    )
    def populate_dropdowns(loader_state):
        if not loader_state:
            raise PreventUpdate

        data_types = loader_state.get("data_types_available", [])
        options = [{"label": "None", "value": "none"}] + [
            {"label": t.title(), "value": t} for t in data_types
        ]
        return options, options, options
