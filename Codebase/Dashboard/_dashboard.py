from dash import Dash
from Codebase.Dashboard.DashboardApp.layout import layout
from Codebase.Dashboard.DashboardApp.callbacks import register_callbacks
from Codebase.Dashboard.DashboardApp.data_config import loader  # ← use the full loader with scanned data

app = Dash(__name__)
app.layout = layout

# The loader has already:
# - recursively scanned for CSV files
# - extracted header info
# - blacklisted undesired columns
# - loaded CSV content into memory

register_callbacks(app, loader)

def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()
