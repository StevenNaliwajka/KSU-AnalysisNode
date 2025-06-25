# pages/inspect_sdr.py
import dash
from dash import html

dash.register_page(__name__, path="/inspect-sdr", name="Inspect SDR")

layout = html.Div([
    html.H2("Inspect SDR Files"),
    html.P("This is where SDR analysis tools will go.")
])
