import pandas as pd
from Codebase.Dashboard.SupportMethods.parse_special_value import parse_special_value
from functools import reduce

from Codebase.DataManager.data_loader import DataLoader


def restore_loader(loader_state, roles):
    loader = DataLoader.from_cached_state(
        dropdown_blacklist=loader_state.get("dropdown_blacklist", []),
        data_types_available=loader_state.get("data_types_available", []),
        column_list_by_type=loader_state.get("column_list_by_type", {}),
        all_csv_files=loader_state.get("all_csv_files", [])
    )
    for role_type, role_col, role_special in roles:
        if role_type and role_col:
            instance_id, _ = parse_special_value(role_special)
            loader.load_data(csv_category=role_type, instance_id=instance_id, set_of_columns={role_col})
    return loader