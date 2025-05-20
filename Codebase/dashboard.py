from dash import Dash
from Codebase.DashboardApp.layout import layout
from Codebase.DashboardApp.callbacks import register_callbacks
from Codebase.DashboardApp.data_config import loader

app = Dash(__name__)
app.layout = layout
register_callbacks(app, loader)

if __name__ == "__main__":
    app.run(debug=True)
