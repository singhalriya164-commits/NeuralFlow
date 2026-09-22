with open("generate_full_25page_report.py", "r", encoding="utf-8") as f:
    for idx, line in enumerate(f, 1):
        if "add_table" in line or "add_fig" in line or "Inches" in line:
            print(f"Line {idx:04d}: {line.strip()[:80]}")
