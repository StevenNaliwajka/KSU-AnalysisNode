# Pages/home.py

import dash
from dash import html

dash.register_page(__name__, path="/", name="Home")

layout = html.Div([
    html.H3("👋 Welcome! Use the dropdown above to navigate.")
])
