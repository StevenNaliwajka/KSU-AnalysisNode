from dash import html, dcc


def get_plot_controls_with_grouping():
    return html.Div([
        html.Div([
            html.Label("Plot Title"),
            dcc.Input(id="plot-title-input", type="text", debounce=True),

            html.Label("Y1 Axis Label"),
            dcc.Input(id="y1-axis-input", type="text", debounce=True),

            html.Label("Y2 Axis Label"),
            dcc.Input(id="y2-axis-input", type="text", debounce=True),

            html.Label("Group Data By"),
            dcc.Dropdown(
                id="time-grouping-dropdown",
                options=[
                    {"label": "Raw (no grouping)", "value": "raw"},
                    {"label": "1 Second", "value": "1S"},
                    {"label": "1 Minute", "value": "1min"},
                    {"label": "1 Hour", "value": "1H"},
                    {"label": "1 Day", "value": "1D"},
                ],
                value="raw",  # Default
                clearable=False
            )
        ], style={"width": "25%", "display": "inline-block", "verticalAlign": "top", "paddingRight": "20px"})
    ])
