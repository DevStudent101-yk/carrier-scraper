# src/processor.py

import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from src.config import (
    MIN_AGE_MONTHS,
    VALID_STATUS,
    VALID_AUTH_STATUS,
    MAX_DRIVERS,
    MAX_TRUCKS,
)


def clean_number(value):
    try:
        return int(str(value).strip())
    except (ValueError, TypeError):
        return 999


def parse_date(value):
    formats = ["%m/%d/%Y", "%Y-%m-%d", "%d-%m-%Y", "%B %d, %Y"]
    for fmt in formats:
        try:
            return datetime.strptime(str(value).strip(), fmt)
        except ValueError:
            continue
    return None


def is_old_enough(issuance_date):
    now = datetime.now()
    age = relativedelta(now, issuance_date)
    total_months = age.years * 12 + age.months
    return total_months >= MIN_AGE_MONTHS


def process_carriers(raw_data):
    if not raw_data:
        print("[Processor] No data received.")
        return pd.DataFrame()

    df = pd.DataFrame(raw_data)
    print(f"[Processor] Raw records received: {len(df)}")

    # Clean whitespace from all text columns
    df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)

    # Parse dates and numbers
    df["issuance_date_parsed"] = df["issuance_date"].apply(parse_date)
    df["num_drivers"] = df["num_drivers"].apply(clean_number)
    df["num_trucks"] = df["num_trucks"].apply(clean_number)

    # Filter condition 1 — must be Active
    mask_status = df["status"].str.lower() == VALID_STATUS.lower()

    # Filter condition 2 — must be Authorized
    mask_auth = df["auth_status"].str.lower() == VALID_AUTH_STATUS.lower()

    # Filter condition 3 — MC must be at least 6 months old
    mask_age = df["issuance_date_parsed"].apply(
        lambda d: is_old_enough(d) if d is not None else False
    )

    # Filter condition 4 — drivers must be 1 or 2
    mask_drivers = df["num_drivers"].between(1, MAX_DRIVERS)

    # Filter condition 5 — trucks must be 1 or 2
    mask_trucks = df["num_trucks"].between(1, MAX_TRUCKS)

    # Filter condition 6 — must have a valid email
    mask_email = df["email"].str.strip().str.len() > 0

    # Combine all conditions
    all_conditions = (
        mask_status &
        mask_auth &
        mask_age &
        mask_drivers &
        mask_trucks &
        mask_email
    )

    filtered_df = df[all_conditions].copy()

    print(f"[Processor] Valid records after filtering: {len(filtered_df)}")
    print(f"[Processor] Rejected records: {len(df) - len(filtered_df)}")

    # Keep only the columns the client needs
    final_df = filtered_df[[
        "mc_number",
        "issuance_date",
        "phone",
        "email",
    ]].copy()

    # Rename columns for clean output
    final_df.columns = ["MC Number", "MC Issuance Date", "Phone", "Email"]

    return final_df