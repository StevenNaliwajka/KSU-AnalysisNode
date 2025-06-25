def parse_special_value(special_value):
    """
    Converts a special value like '-1|-3' into (instance_id: int, special_key: str).
    Returns (None, None) if invalid or missing.
    """
    if not special_value or "|" not in special_value:
        return None, None
    try:
        instance_part, special_part = special_value.split("|", 1)
        return int(instance_part), special_part
    except Exception as e:
        print(f"[WARN] Failed to parse special_value '{special_value}': {e}")
        return None, None