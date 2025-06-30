from dash import html, dcc

def row_layout(
    row_id,
    dropdown_id,
    special_id,
    conditional_id,
    placeholder,
    time_grouping_id,
    outlier_filter_id,
    extra_transform_id  # ✅ NEW
):
    return html.Div([
        # Initial dropdown
        html.Div([
            dcc.Dropdown(id=dropdown_id, options=[], placeholder=placeholder)
        ], style={"width": "250px", "padding": "10px"}),

        # Special value dropdown
        html.Div([
            dcc.Dropdown(
                id=special_id,
                options=[],
                placeholder="Select Special Value",
                style={"display": "none"}
            )
        ], id=f"{special_id}-container", style={"width": "250px", "padding": "10px"}),

        # Column selector
        html.Div([
            dcc.Dropdown(
                id=conditional_id,
                options=[],
                placeholder="Select Column",
                value=None,
                clearable=False
            )
        ], style={"width": "250px", "padding": "10px"}),

        # Time grouping dropdown
        html.Div([
            dcc.Dropdown(
                id=time_grouping_id,
                options=[
                    {"label": "Raw (no grouping)", "value": "raw"},
                    {"label": "1 Second", "value": "1S"},
                    {"label": "5 Seconds", "value": "5S"},
                    {"label": "10 Seconds", "value": "10S"},
                    {"label": "30 Seconds", "value": "30S"},
                    {"label": "1 Minute", "value": "1min"},
                    {"label": "5 Minutes", "value": "5min"},
                    {"label": "15 Minutes", "value": "15min"},
                    {"label": "1 Hour", "value": "1H"},
                ],
                placeholder="Group By",
                value="raw",
                clearable=False,
            )
        ], style={"width": "200px", "padding": "10px"}),

        # ✅ Row with Outlier Filter + Extra Transform
        html.Div([
            # Outlier Filter
            html.Div([
                dcc.Dropdown(
                    id=outlier_filter_id,
                    options=[
                        {"label": "None", "value": "None"},
                        {"label": "Remove Top 5%", "value": "Remove Top 5%"},
                        {"label": "Remove Bottom 5%", "value": "Remove Bottom 5%"},
                        {"label": "Remove Top & Bottom 5%", "value": "Remove Top & Bottom 5%"},
                    ],
                    placeholder="Outlier Filter",
                    value=None,
                    clearable=True
                )
            ], style={"width": "230px", "padding": "10px"}),

            # Extra Transform
            html.Div([
                dcc.Dropdown(
                    id=extra_transform_id,
                    options=[
                        {"label": "None", "value": "none"},
                        {"label": "Convert °C to °F", "value": "c_to_f"},
                        {"label": "Convert °F to °C", "value": "f_to_c"},
                        {"label": "Apply Log10", "value": "log10"},
                        {"label": "Invert (1/x)", "value": "invert"},
                    ],
                    placeholder="Extra Transform",
                    value="none",
                    clearable=False
                )
            ], style={"width": "230px", "padding": "10px"})
        ], style={"display": "flex", "justifyContent": "center", "alignItems": "center"})
    ], style={"display": "flex", "flexWrap": "wrap", "justifyContent": "center", "alignItems": "center"})
