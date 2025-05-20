from dash import html, dcc
from Codebase.DashboardApp.data_config import soil_depths, tvws_specials, available_columns

layout = html.Div([
    html.H1("📊 Time Series Dashboard (Dual Y-Axis)"),

    html.Div([
        html.Label("SoilData Instance"),
        dcc.Dropdown(
            id='soil-instance',
            options=[{"label": f"Soil ({soil_depths.get(i, '?')})", "value": i} for i in [1, 2]],
            value=1
        ),
    ], style={"width": "48%", "display": "inline-block"}),

    html.Div([
        html.Label("TVWS Instance"),
        dcc.Dropdown(
            id='tvws-instance',
            options=[
                {"label": f"TVWS ({tvws_specials.get(i, '?').replace('\"', '\'')})", "value": i}
                for i in [1, 2]
            ],
            value=1
        ),
    ], style={"width": "48%", "display": "inline-block", "marginLeft": "4%"}),

    html.Div([
        html.Label("Left Y-Axis (Y1)"),
        dcc.Dropdown(
            id='y1-axis',
            options=[{"label": col, "value": col} for col in available_columns],
            value="soil moisture value"
        ),
    ], style={"width": "48%", "display": "inline-block", "marginTop": "20px"}),

    html.Div([
        html.Label("Right Y-Axis (Y2)"),
        dcc.Dropdown(
            id='y2-axis',
            options=[{"label": col, "value": col} for col in available_columns],
            value="drssi"
        ),
    ], style={"width": "48%", "display": "inline-block", "marginLeft": "4%", "marginTop": "20px"}),

    html.Div([
        html.Label("Third Metric (Y3, plotted on Y1 axis)"),
        dcc.Dropdown(
            id='y3-axis',
            options=[{"label": col, "value": col} for col in available_columns],
            value=None
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
