# pages/see_variance.py
import dash
from dash import html

dash.register_page(__name__, path="/see-variance", name="See Variance")

layout = html.Div([
    html.H2("📈 See Variance of Value"),
    html.P("This page will let you select a variable and see its variance across time."),
])
