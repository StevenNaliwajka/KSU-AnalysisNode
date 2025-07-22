import numpy as np
import os

def prompt_user_to_select_iq_file(base_dir="Data") -> str:
    """
    Recursively scans for .iq files under the given base_dir and prompts user to select one.
    Returns the full path to the selected file.
    """
    iq_files = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".iq"):
                full_path = os.path.join(root, file)
                iq_files.append(full_path)

    if not iq_files:
        raise FileNotFoundError(f"No .iq files found under {base_dir}")

    print("\nAvailable .iq files:")
    for i, path in enumerate(iq_files):
        print(f"  {i + 1}. {path}")

    while True:
        try:
            selection = int(input(f"\nSelect a file [1-{len(iq_files)}]: "))
            if 1 <= selection <= len(iq_files):
                return iq_files[selection - 1]
            else:
                print("Invalid number. Try again.")
        except ValueError:
            print("Please enter a valid number.")

def load_hackrf_iq(filename: str = None) -> np.ndarray:
    """
    Loads a HackRF .iq file (complex int8) and returns a complex float32 array.
    If no filename is provided, prompts the user to select one from Data/.
    """
    if filename is None:
        filename = prompt_user_to_select_iq_file()

    print(f"\n[INFO] Loading: {filename}")
    raw = np.fromfile(filename, dtype=np.int8)
    iq = raw[::2].astype(np.float32) + 1j * raw[1::2].astype(np.float32)
    return iq
