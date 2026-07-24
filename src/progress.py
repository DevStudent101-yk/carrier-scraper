# src/progress.py
# ─────────────────────────────────────────────
# Saves and loads the last processed MC number
# so the scraper can resume after a crash or stop
# ─────────────────────────────────────────────

import json
import os

PROGRESS_FILE = "progress.json"


def save_progress(last_mc: int, valid_count: int, processed_count: int):
    """Save current position to disk."""
    data = {
        "last_mc": last_mc,
        "valid_count": valid_count,
        "processed_count": processed_count
    }
    with open(PROGRESS_FILE, "w") as f:
        json.dump(data, f)


def load_progress() -> dict:
    """Load saved position. Returns defaults if no file exists."""
    if not os.path.exists(PROGRESS_FILE):
        return {"last_mc": 0, "valid_count": 0, "processed_count": 0}
    with open(PROGRESS_FILE, "r") as f:
        return json.load(f)


def reset_progress():
    """Delete progress file to start from scratch."""
    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)
        print("[Progress] Progress reset. Starting from beginning.")