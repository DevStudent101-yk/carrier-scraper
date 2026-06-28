# src/exporter.py
# ─────────────────────────────────────────
# Takes the final clean DataFrame and saves
# it as both CSV and Excel files in /output
# ─────────────────────────────────────────

import os
import pandas as pd
from datetime import datetime
from src.config import OUTPUT_DIR, OUTPUT_FILENAME


def export_data(df: pd.DataFrame) -> None:

    # If DataFrame is empty, nothing to export
    if df.empty:
        print("[Exporter] No valid records to export.")
        return

    # Create output folder if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Add timestamp to filename so files never overwrite each other
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_path = os.path.join(OUTPUT_DIR, f"{OUTPUT_FILENAME}_{timestamp}")

    # ── Save as CSV ───────────────────────────
    csv_path = base_path + ".csv"
    df.to_csv(csv_path, index=False)
    print(f"[Exporter] CSV saved  → {csv_path}")

    # ── Save as Excel ─────────────────────────
    excel_path = base_path + ".xlsx"
    df.to_excel(excel_path, index=False, sheet_name="Valid Carriers")
    print(f"[Exporter] Excel saved → {excel_path}")

    print(f"[Exporter] Total valid records exported: {len(df)}")