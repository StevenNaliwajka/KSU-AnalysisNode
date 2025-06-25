from Codebase.Pathing.get_dashboard_assets_folder import get_dashboard_assets_folder


def load_dropdown_blacklist():
    """Load blacklisted column names from a file."""
    dashboard_assets_folder = get_dashboard_assets_folder()
    blacklist_file = dashboard_assets_folder / "dropdown_blacklist.txt"
    blacklist = set()

    if blacklist_file.exists():
        with open(blacklist_file, "r", encoding="utf-8") as f:
            for line in f:
                entry = line.strip().lower()
                if entry:
                    blacklist.add(entry)
    else:
        print(f"[WARN] Blacklist file not found: {blacklist_file}")
    # print("BLACKLIST:")
    # print(blacklist)
    return blacklist


if __name__ == "__main__":
    print(load_dropdown_blacklist())
