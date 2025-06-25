from Codebase.Pathing.get_data_folder import get_data_folder


def get_all_csv_files():
    data_folder = get_data_folder()
    return list(data_folder.rglob("*.csv"))
