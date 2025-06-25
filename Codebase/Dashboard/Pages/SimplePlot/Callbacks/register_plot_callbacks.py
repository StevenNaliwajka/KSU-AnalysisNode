from dash import Input, Output, State, dcc, no_update, html
from dash.exceptions import PreventUpdate

from Codebase.Dashboard.Pages.SimplePlot.Callbacks.ensure_data_is_loaded import ensure_data_is_loaded
from Codebase.Dashboard.Pages.SimplePlot.Callbacks.make_conditional_dropdown_callback import \
    make_conditional_dropdown_callback
from Codebase.Dashboard.Pages.SimplePlot.Callbacks.populate_inital_dropdowns import populate_inital_dropdowns
from Codebase.Dashboard.Pages.SimplePlot.Callbacks.register_plot_figure_callback import register_plot_figure_callback
from Codebase.Dashboard.Pages.SimplePlot.Callbacks.register_plot_init_loader import register_plot_init_loader
from Codebase.Dashboard.Pages.SimplePlot.Callbacks.make_special_dropdown import make_special_dropdown
from Codebase.DataManager.data_loader import DataLoader

def register_plot_callbacks(app):
    register_plot_init_loader(app)
    populate_inital_dropdowns(app)

    ensure_data_is_loaded(app, "dropdown-1")
    ensure_data_is_loaded(app, "dropdown-2")
    ensure_data_is_loaded(app, "dropdown-3")

    # Inject "Special Value" dropdown for soil/tvws
    make_special_dropdown(app, "dropdown-1", "dropdown-special-1")
    make_special_dropdown(app, "dropdown-2", "dropdown-special-2")
    make_special_dropdown(app, "dropdown-3", "dropdown-special-3")

    # Register conditional dropdowns
    make_conditional_dropdown_callback(app, "dropdown-1", "dropdown-special-1", "conditional-1")
    make_conditional_dropdown_callback(app, "dropdown-2", "dropdown-special-2", "conditional-2")
    make_conditional_dropdown_callback(app, "dropdown-3", "dropdown-special-3", "conditional-3")

    register_plot_figure_callback(app)

'''
    @app.callback(
        Output("loader-store", "data"),
        Input("page-init-trigger", "n_intervals"),
        prevent_initial_call=False
    )
    def init_loader(_):
        dropdown_blacklist = {"datetime", "date", "time"}
        loader = DataLoader(dropdown_blacklist)
        return sorted(loader.data_types_available)

    @app.callback(
        Output("dropdown-1", "options"),
        Output("dropdown-2", "options"),
        Output("dropdown-3", "options"),
        Input("loader-store", "data")
    )
    def populate_dropdowns(data_types):
        if not data_types:
            raise PreventUpdate

        options = [{"label": "None", "value": "none"}] + [
            {"label": t.title(), "value": t} for t in data_types
        ]
        return options, options, options

    @app.callback(
        Output("conditional-1", "children"),
        Input("dropdown-1", "value")
    )
    def show_y1_dropdown(x_type):
        if x_type is None or x_type == "none":
            return None
        return html.Label("Y1 Options Visible")

    @app.callback(
        Output("conditional-2", "children"),
        Input("dropdown-2", "value")
    )
    def show_y2_dropdown(y1_type):
        if y1_type is None or y1_type == "none":
            return None
        return html.Label("Y2 Options Visible")

    @app.callback(
        Output("conditional-3", "children"),
        Input("dropdown-3", "value")
    )
    def show_y3_dropdown(y2_type):
        if y2_type is None or y2_type == "none":
            return None
        return html.Label("Y2 Options Visible")
    '''

