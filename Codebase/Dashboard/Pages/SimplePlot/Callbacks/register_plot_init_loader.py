from dash import Input, Output

from Codebase.Dashboard.SupportMethods.load_dropdown_blacklist import load_dropdown_blacklist
from Codebase.DataManager.data_loader import DataLoader

def register_plot_init_loader(app):
    @app.callback(
        Output("loader-store", "data"),
        Input("page-init-trigger", "n_intervals"),
        prevent_initial_call=False
    )
    def init_loader(_):
        dropdown_blacklist = load_dropdown_blacklist()
        loader = DataLoader(dropdown_blacklist)

        return {
            "dropdown_blacklist": sorted(dropdown_blacklist),
            "data_types_available": sorted(loader.data_types_available),
            "column_list_by_type": loader.column_list_by_type,
            "all_csv_files": [str(path) for path in loader.all_csv_files]
        }