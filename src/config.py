# src/config.py

# ── Fenderr URLs ──────────────────────────────
FENDERR_SEARCH_URL = "https://app.fenderr.com/carrier-search?q={mc}"

# ── MC Range to scan ──────────────────────────

MC_RANGE_START = 1_780_000
MC_RANGE_END   = 1_800_000
TARGET_VALID_COUNT = 1000  # Start with 50 as a proof of concept


# ── Filter conditions ─────────────────────────
MIN_AGE_MONTHS = 2      # carrier must be at least 2 months old
MAX_AGE_MONTHS = 12     # carrier must be no older than 12 months

VALID_STATUS = "Active"
VALID_AUTH_STATUS = "Authorized"

MAX_DRIVERS = 2
MAX_TRUCKS  = 2

# ── Delays between requests (seconds) ────────
REQUEST_DELAY_MIN = 2.0
REQUEST_DELAY_MAX = 4.0

# ── Retry settings ────────────────────────────
MAX_RETRIES = 3

# ── Output ────────────────────────────────────
OUTPUT_DIR      = "output"
OUTPUT_FILENAME = "valid_carriers"

# ── Google Sheets (fill in later) ────────────
GOOGLE_SHEET_NAME        = "Carrier Data"
GOOGLE_CREDENTIALS_FILE  = "credentials.json"