# pages/train_ml.py
import dash
from dash import html

dash.register_page(__name__, path="/train-ml", name="Train ML")

layout = html.Div([
    html.H2("🤖 Train Machine Learning Model"),
    html.P("This page will allow you to select input/output variables and train a model."),
])
