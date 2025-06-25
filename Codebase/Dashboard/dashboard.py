# Codebase/Dashboard/dashboard.py

from dash import Dash, dcc, html
import dash

# changed to diff stuff
# from Codebase.Dashboard.DashboardApp.data_config import loader
from Codebase.Dashboard.Pages.SimplePlot.Callbacks.register_plot_callbacks import register_plot_callbacks
from Codebase.Dashboard.Callbacks.global_callbacks import register_callbacks

# Initialize Dash
app = Dash(
    __name__,
    use_pages=True,
    pages_folder="Pages",
    suppress_callback_exceptions=True
)
'''
# Shared buttons for navigation (persistent across all pages)
shared_links = html.Div([
    html.H2("📂 Select a Function", style={"textAlign": "center"}),

    
    html.Div([
        dcc.Link("🔍 Inspect SDR Files", href="/inspect-sdr", className="nav-link"),
        html.Br(),
        dcc.Link("📈 Plot a Value Over Time", href="/plot-value", className="nav-link"),
        html.Br(),
        dcc.Link("📊 See Variance of Value", href="/see-variance", className="nav-link"),
        html.Br(),
        dcc.Link("🤖 Train Machine Learning Model", href="/train-ml", className="nav-link"),
    ], style={"textAlign": "center", "fontSize": "18px", "lineHeight": "2"})
    
])
'''
shared_links = html.Div([
    html.Div([
        dcc.Link("🔍 Inspect SDR Files", href="/inspect-sdr", className="dropdown-link"),
        dcc.Link("📈 Plot a Value Over Time", href="/plot-value", className="dropdown-link"),
        dcc.Link("📊 See Variance of Value", href="/see-variance", className="dropdown-link"),
        dcc.Link("🤖 Train Machine Learning Model", href="/train-ml", className="dropdown-link"),
    ], className="dropdown-nav")
])
'''
# Global layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    shared_links,
    dash.page_container
])
'''
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.H2("📂 Select a Function", style={"textAlign": "center"}),
    shared_links,
    dash.page_container
])

# Register all callbacks
register_callbacks(app)         # for dropdown routing
#register_plot_callbacks(app, loader)
register_plot_callbacks(app)

def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()
