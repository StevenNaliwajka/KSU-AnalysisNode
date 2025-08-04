# Pages/bio.py
import dash
from dash import html

dash.register_page(__name__, path="/bio")

layout = html.Div([
    html.H3("About This Project"),
    html.P(
        "This dashboard is part of a joint research effort between Georgia State University (GSU) "
        "and Kennesaw State University (KSU). The work is centered at KSU’s Field Station, where we "
        "collect and analyze environmental data to better understand conditions on site. "
    ),
    html.P(
        "This dashboard pulls together the ongoing data collection in a way that’s "
        "practical for students, researchers, and collaborators across both universities."
    )
])
