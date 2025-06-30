from dash import html, dcc

def get_plot_label_inputs():
    return html.Div([
        html.Div([
            html.Label("Plot Title", htmlFor="plot-title-input"),
            dcc.Input(
                id="plot-title-input",
                type="text",
                value="Time Series Data",
                debounce=True,
                style={"width": "100%"}
            )
        ], style={"margin-bottom": "1rem"}),

        html.Div([
            html.Label("Y1 Axis Label", htmlFor="y1-axis-input"),
            dcc.Input(
                id="y1-axis-input",
                type="text",
                value="Y1 Axis",
                debounce=True,
                style={"width": "100%"}
            )
        ], style={"margin-bottom": "1rem"}),

        html.Div([
            html.Label("Y2 Axis Label", htmlFor="y2-axis-input"),
            dcc.Input(
                id="y2-axis-input",
                type="text",
                value="Y2 Axis",
                debounce=True,
                style={"width": "100%"}
            )
        ], style={"margin-bottom": "1rem"}),

        html.Div([
            html.Label("Y3 Axis Label", htmlFor="y3-axis-input"),
            dcc.Input(
                id="y3-axis-input",
                type="text",
                value="Y3 Axis",
                debounce=True,
                style={"width": "100%"}
            )
        ])
    ], style={"padding": "1rem", "border": "1px solid #ccc", "borderRadius": "10px"})
