import os
import sys

# Add project root to sys.path before any Codebase imports
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Now safe to import project files
from Codebase.Dashboard.dashboard import main

# Third-party imports
from dash import Dash, dcc, html
import dash
import json


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
    suppress_callback_exceptions=True
)

# Shared navigation links
shared_links = html.Div([
    html.Div([
        dcc.Link("🔍 Inspect SDR Files", href="/inspect-sdr", className="dropdown-link"),
        dcc.Link("📈 Plot a Value Over Time", href="/plot-value", className="dropdown-link"),
        dcc.Link("📊 See Variance of Value", href="/see-variance", className="dropdown-link"),
        dcc.Link("🤖 Train Machine Learning Model", href="/train-ml", className="dropdown-link"),
    ], className="dropdown-nav")
])

# Global layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.H2("📂 Select a Function", style={"textAlign": "center"}),
    shared_links,
    dash.page_container
])

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
