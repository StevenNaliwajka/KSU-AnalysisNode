import os

from Codebase.Pathing.get_data_folder import get_data_folder

def find_short_csv_files(data_root, max_lines=3):
    short_files = []
    for root, _, files in os.walk(data_root):
        for file in files:
            if file.lower().endswith(".csv"):
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        line_count = sum(1 for _ in f)
                        if line_count <= max_lines:
                            short_files.append(full_path)
                except Exception as e:
                    print(f"[ERROR] Failed to read {full_path}: {e}")
    return short_files

def delete_files(file_list):
    for path in file_list:
        try:
            os.remove(path)
            print(f"[INFO] Deleted: {path}")
        except Exception as e:
            print(f"[ERROR] Failed to delete {path}: {e}")

if __name__ == "__main__":
    data_folder = get_data_folder()
    short_csvs = find_short_csv_files(data_folder, max_lines=3)

    if not short_csvs:
        print("[INFO] No CSV files with 3 or fewer lines found.")
    else:
        print(f"[INFO] Found {len(short_csvs)} CSV files with ≤ 3 lines. Deleting...")
        delete_files(short_csvs)
