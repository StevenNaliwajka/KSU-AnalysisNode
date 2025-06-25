import dash
from dash import html, dcc

from Codebase.Dashboard.Pages.SimplePlot.Formating.get_plot_controls_with_grouping import \
    get_plot_controls_with_grouping
from Codebase.Dashboard.Pages.SimplePlot.Formating.get_plot_label_inputs import get_plot_label_inputs
from Codebase.Dashboard.Pages.SimplePlot.Formating.row_layout import row_layout

# Register the page in the multi-page Dash app
dash.register_page(__name__, path="/plot-value", name="Plot Value")

layout = html.Div([
    dcc.Interval(id="page-init-trigger", interval=300, n_intervals=0, max_intervals=1),
    dcc.Store(id="loader-store"),

    html.H2("📈 Plot a Value Over Time", style={"textAlign": "center", "marginBottom": "30px"}),

    row_layout("row1", "dropdown-1", "dropdown-special-1", "conditional-1", "Select Y1 Axis"),
    row_layout("row2", "dropdown-2", "dropdown-special-2", "conditional-2", "Select Y2 Axis"),
    row_layout("row3", "dropdown-3", "dropdown-special-3", "conditional-3", "Select Y3 Axis"),

    get_plot_controls_with_grouping(),  # <- NEW: editable labels

    html.Div(id="plot-container"),
])