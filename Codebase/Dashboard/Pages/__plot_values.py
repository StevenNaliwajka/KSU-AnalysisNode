import dash
from dash import html, dcc

dash.register_page(__name__, path="/plot-value", name="Plot Value")

dummy_options = [{"label": f"Option {i}", "value": f"val{i}"} for i in range(1, 6)]

def row_layout(row_id, dropdown_id, conditional_id, placeholder):
    return html.Div([
        html.Div([
            dcc.Dropdown(id=dropdown_id, options=[], placeholder=placeholder)
        ], style={"width": "250px", "padding": "10px"}),

        html.Div(id=conditional_id, style={"width": "250px", "padding": "10px"})
    ], style={"display": "flex", "justifyContent": "center", "alignItems": "center"})


layout = html.Div([
    dcc.Interval(id="page-init-trigger", interval=300, n_intervals=0, max_intervals=1),
    dcc.Store(id="loader-store"),  # ← stores serialized object

    html.H2("📈 Plot a Value Over Time", style={"textAlign": "center", "marginBottom": "30px"}),

    row_layout("row1", "dropdown-1", "conditional-1", "Select X Axis"),
    row_layout("row2", "dropdown-2", "conditional-2", "Select Y1 Axis"),
    row_layout("row3", "dropdown-3", "conditional-3", "Select Y2 Axis"),
])
