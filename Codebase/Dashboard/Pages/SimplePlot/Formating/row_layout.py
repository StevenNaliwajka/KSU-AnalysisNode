import dash
from dash import html, dcc

def row_layout(row_id, dropdown_id, special_id, conditional_id, placeholder):
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
                style={"display": "none"}  # initially hidden
            )
        ], id=f"{special_id}-container", style={"width": "250px", "padding": "10px"}),

        # ✅ Directly define the conditional dropdown with static ID
        html.Div([
            dcc.Dropdown(
                id=conditional_id,
                options=[],
                placeholder="Select Column",
                value=None,
                clearable=False
            )
        ], style={"width": "250px", "padding": "10px"})
    ], style={"display": "flex", "justifyContent": "center", "alignItems": "center"})
