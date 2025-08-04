import os
import sys

# Add project root to sys.path before any Codebase imports
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Third-party imports
from dash import Dash, dcc, html, Output, Input
import dash
import json
import dash_bootstrap_components as dbc
from Codebase.Dashboard.Callbacks.global_callbacks import register_callbacks
from Codebase.Dashboard.Pages.SimplePlot.Callbacks.register_plot_callbacks import register_plot_callbacks

# Path to config (define BEFORE using it)
CONFIG_PATH = os.path.join(PROJECT_ROOT, "Codebase", "Setup", "setup_config.json")

# Load configuration (fallback to defaults)
def load_config():
    default = {"ip_address": "localhost", "port": 8050}
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                config = json.load(f)
                # Validate
                ip = config.get("ip_address", default["ip_address"])
                port = config.get("port", default["port"])
                if not isinstance(ip, str) or not isinstance(port, int):
                    raise ValueError
                return {"ip_address": ip, "port": port}
        except (json.JSONDecodeError, ValueError):
            print(f"[WARN] Invalid config at {CONFIG_PATH}, using defaults.")
    return default

config = load_config()

# Initialize Dash
app = Dash(
    __name__,
    use_pages=True,
    pages_folder="Pages",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

# Top Navbar
navbar = html.Div([
    html.Div([
        dcc.Link(
            "FS-Testbed Dashboard",
            href="/",
            style={
                "fontSize": "1.5rem",
                "fontWeight": "400",
                "color": "#000",
                "textDecoration": "none"
            }
        ),
    ]),
    html.Div(id="nav-links-container", className="nav-links")  # <-- now dynamic
], className="navbar")


@app.callback(
    Output("nav-links-container", "children"),
    Input("url", "pathname")
)
def update_navbar_active(pathname):
    # Helper to set active class based on current page
    def nav_link(name, href):
        classes = "dropdown-link"
        if pathname == href:  # only add active-link if it's the exact page
            classes += " active-link"
        return dcc.Link(name, href=href, className=classes)

    return [
        nav_link("Data", "/data"),
        nav_link("Overview", "/overview"),
        nav_link("Bio", "/bio"),
    ]



# Global layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div([
        html.H2(id="page-header", style={"textAlign": "center"}),  # Dynamic header
        dash.page_container
    ], className="page-content")
])

# Callback to update header based on current path
@app.callback(
    Output("page-header", "children"),
    Input("url", "pathname")
)
def update_header(pathname):
    page_titles = {
        "/data": "FieldStation Data Plotter",
        "/overview": "Overview",
        "/bio": "Bio",
        "/": "Home"
    }
    return page_titles.get(pathname, "FieldStation Data Plotter")



# Register all callbacks
register_callbacks(app)
register_plot_callbacks(app)

def main():
    print(f"[INFO] Starting Dash app on {config['ip_address']}:{config['port']}")
    app.run(
        debug=True,
        host=config["ip_address"],
        port=config["port"]
    )

if __name__ == "__main__":
    main()
