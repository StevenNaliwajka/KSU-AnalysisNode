from Codebase.DataManager.Processing.Header.normalize_header import normalize_header


def detect_header_row(filepath, max_scan_lines=10):
    # print(f"[DEBUG] Starting header detection for file: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        for i in range(max_scan_lines):
            line = f.readline()
            if not line:
                break
            # print(f"[DEBUG] Line {i}: {line.strip()}")
            cols = [c.strip().replace('"', '') for c in line.strip().split(',')]
            lower = [normalize_header(c) for c in cols]
            if any("date" in col for col in lower) and (
                any("time" in col for col in lower)
                or any(any(keyword in col for keyword in ("soil", "moisture", "temperature")) for col in lower)
            ):
                # print(f"[DEBUG] Header detected at line {i}: {cols}")
                return i, cols
    with open(filepath, 'r', encoding='utf-8') as f:
        first = f.readline().strip().split(',')
    first_clean = [c.strip().replace('"', '') for c in first]
    # print(f"[DEBUG] No header match; fallback to first line: {first_clean}")
    return 0, first_clean