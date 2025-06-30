from Codebase.Dashboard.SupportMethods.parse_special_value import parse_special_value


def extract_df(loader, data_type, col, special, role_label=None):
    if not data_type or not col or data_type not in loader.data:
        return None
    if data_type in ["tvws", "soil"] and not special:
        return None

    special_instance_id, _ = parse_special_value(special)
    frames = []

    for instance_id, instance in loader.data[data_type].items():
        if data_type in ["tvws", "soil"] and str(special_instance_id) not in str(instance_id):
            continue

        for subkey, subdict in instance.items():
            for df in subdict["data"]:
                if col in df.columns:
                    safe_label = f"{role_label}::{col}::{instance_id or 'unknown'}"
                    temp = df[["datetime", col]].copy()
                    temp = temp.rename(columns={col: safe_label})
                    frames.append(temp)

    return frames if frames else None