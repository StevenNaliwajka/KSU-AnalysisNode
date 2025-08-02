from dash import Dash, dcc, html
import dash
import json
import os

# Import callbacks
from Codebase.Dashboard.Pages.SimplePlot.Callbacks.register_plot_callbacks import register_plot_callbacks
from Codebase.Dashboard.Callbacks.global_callbacks import register_callbacks

# Path to config
CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Setup", "setup_config.json")

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
