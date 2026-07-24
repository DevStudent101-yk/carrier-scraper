# src/exporter.py

import os
import logging
import pandas as pd
from datetime import datetime
from src.config import OUTPUT_DIR, OUTPUT_FILENAME

# ── Setup logging ─────────────────────────────
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/scraper.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def export_data(df: pd.DataFrame) -> None:

    if df.empty:
        logger.warning("No valid records to export.")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_path = os.path.join(OUTPUT_DIR, f"{OUTPUT_FILENAME}_{timestamp}")

    # Save CSV
    csv_path = base_path + ".csv"
    df.to_csv(csv_path, index=False)
    logger.info(f"CSV saved → {csv_path}")

    # Save Excel
    excel_path = base_path + ".xlsx"
    df.to_excel(excel_path, index=False, sheet_name="Valid Carriers")
    logger.info(f"Excel saved → {excel_path}")

    logger.info(f"Total valid records exported: {len(df)}")