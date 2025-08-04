# Pages/overview.py
import dash
from dash import html

dash.register_page(__name__, path="/overview")

layout = html.Div([
    html.H3("Data Overview"),
    html.P(
        "This dashboard currently pulls together three types of data collected at the KSU Field Station:"
    ),
    html.Ul([
        html.Li([
            html.Strong("Atmospheric Data: "),
            "Weather and environmental measurements recorded above ground."
        ]),
        html.Li([
            html.Strong("Buried Sensors: "),
            "Subsurface readings that capture conditions below the surface."
        ]),
        html.Li([
            html.Strong("TVWS Signals: "),
            "Radio data in the TV White Space spectrum, used for monitoring signal behavior in the field."
        ]),
    ]),
    html.P(
        "These datasets provide different perspectives on the same environment, helping us track and understand changes over time."
    )
])
