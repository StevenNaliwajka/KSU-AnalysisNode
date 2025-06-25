from dash import html, dcc
from Codebase.Dashboard.DashboardApp.data_config import all_available_columns

# Define safe defaults for Y1 and Y2 axes
y1_default = "soil moisture value" if "soil moisture value" in all_available_columns else (
    all_available_columns[0] if all_available_columns else "__none__"
)

y2_default = "drssi" if "drssi" in all_available_columns else (
    all_available_columns[1] if len(all_available_columns) > 1 else y1_default
)

# Prepend safe "None" option
dropdown_options = [{"label": "None", "value": "__none__"}] + [
    {"label": col, "value": col} for col in all_available_columns
]

layout = html.Div([
    html.H1("📊 Time Series Dashboard (Dual Y-Axis)"),

    html.Div([
        html.Label("Left Y-Axis (Y1)"),
        dcc.Dropdown(
            id='y1-axis',
            options=dropdown_options,
            value=y1_default
        ),
    ], style={"width": "48%", "display": "inline-block", "marginTop": "20px"}),

    html.Div([
        html.Label("Right Y-Axis (Y2)"),
        dcc.Dropdown(
            id='y2-axis',
            options=dropdown_options,
            value=y2_default
        ),
    ], style={"width": "48%", "display": "inline-block", "marginLeft": "4%", "marginTop": "20px"}),

    html.Div([
        html.Label("Third Metric (Y3, plotted on Y1 axis)"),
        dcc.Dropdown(
            id='y3-axis',
            options=dropdown_options,
            value="__none__"
        ),
    ], style={"width": "48%", "marginTop": "20px"}),

    html.Div([
        html.Label("Time Aggregation"),
        dcc.Dropdown(
            id='time-agg',
            options=[
                {"label": "1 minute", "value": "1min"},
                {"label": "5 minutes", "value": "5min"},
                {"label": "1 hour", "value": "1H"},
                {"label": "1 day", "value": "1D"},
            ],
            value="1min"
        ),
    ], style={"width": "48%", "marginTop": "20px"}),

    html.Div([
        html.Label("Select Time Range"),
        dcc.DatePickerRange(
            id='date-range',
            start_date="2025-01-01",
            end_date="2025-12-31",
            initial_visible_month="2025-01-01"
        )
    ], style={"marginTop": "20px"}),

    dcc.Graph(id='time-series'),
    html.Div(id='debug-output', style={'whiteSpace': 'pre-wrap'})
])
