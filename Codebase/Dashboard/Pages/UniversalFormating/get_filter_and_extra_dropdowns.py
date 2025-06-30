from dash import html, dcc

def get_filter_and_extra_dropdowns(role_id: str):
    return html.Div([
        html.Label(f"{role_id.upper()} Outlier Filter"),
        dcc.Dropdown(
            id=f"outlier-filter-{role_id}",
            options=[
                {"label": "None", "value": "none"},
                {"label": "Remove Top 5%", "value": "top5"},
                {"label": "Remove Bottom 5%", "value": "bottom5"},
                {"label": "Remove Both 5%", "value": "both5"},
            ],
            value="none",
            style={"marginBottom": "5px"}
        ),
        html.Label("Extra Actions"),
        dcc.Dropdown(
            id=f"extra-action-{role_id}",
            options=[
                {"label": "None", "value": "none"},
                {"label": "Convert C to F", "value": "c_to_f"},
                {"label": "Convert F to C", "value": "f_to_c"},
                {"label": "Negate", "value": "negate"},
            ],
            value="none"
        )
    ], style={"width": "30%", "display": "inline-block", "marginRight": "3%"})
