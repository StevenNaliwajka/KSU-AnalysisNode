# Pages/home.py
import dash
from dash import html

dash.register_page(__name__, path="/")

layout = html.Div([
    html.H3("Welcome to the FS-Testbed Dashboard"),
    html.P("Use the navigation bar to explore data plots, overview insights, and project bio information.")
])