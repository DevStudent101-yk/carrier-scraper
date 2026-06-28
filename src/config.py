# src/config.py

# Website (fill in Monday when site is back)
BASE_URL = "https://your-client-site.com"

# ── Scraping ──────────────────────────────────
MAX_RECORDS = None

REQUEST_DELAY_MIN = 1.5
REQUEST_DELAY_MAX = 3.5

# ── Filter conditions ─────────────────────────
# MC must be at least 6 months old
MIN_AGE_MONTHS = 6

# Carrier must be active
VALID_STATUS = "Active"

# Carrier must be authorized
VALID_AUTH_STATUS = "Authorized"

# Only carriers with 1 driver (exact match)
EXACT_DRIVERS = 1

# Only carriers with 1 truck (exact match)
EXACT_TRUCKS = 1

# Hard rejection — ignore anything above this
MAX_DRIVERS = 2
MAX_TRUCKS = 2

# ── Output ────────────────────────────────────
OUTPUT_DIR = "output"
OUTPUT_FILENAME = "valid_carriers"

# ── Google Sheets ─────────────────────────────
# You will fill these in during Step 7
GOOGLE_SHEET_NAME = "Carrier Data"
GOOGLE_CREDENTIALS_FILE = "credentials.json"