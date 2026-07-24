# src/processor.py

import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from src.config import (
    MIN_AGE_MONTHS,
    MAX_AGE_MONTHS,
    VALID_STATUS,
    MAX_DRIVERS,
    MAX_TRUCKS,
)


def clean_number(value):
    try:
        return int(str(value).strip())
    except (ValueError, TypeError):
        return 999


def parse_date(value):
    formats = [
        "%m/%d/%Y", "%Y-%m-%d", "%d-%m-%Y",
        "%B %d, %Y", "%b %d, %Y",   # Jun 15, 2024
    ]
    for fmt in formats:
        try:
            return datetime.strptime(str(value).strip(), fmt)
        except ValueError:
            continue
    return None


def get_age_months(date):
    now = datetime.now()
    age = relativedelta(now, date)
    return age.years * 12 + age.months


def is_valid_age(issuance_date):
    months = get_age_months(issuance_date)
    return MIN_AGE_MONTHS <= months <= MAX_AGE_MONTHS


def process_carriers(raw_data):
    if not raw_data:
        print("[Processor] No data received.")
        return pd.DataFrame()

    df = pd.DataFrame(raw_data)
    print(f"[Processor] Raw records received: {len(df)}")

    df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)

    df["mcs_date_parsed"] = df["mcs_date"].apply(parse_date)
    df["num_drivers"]     = df["num_drivers"].apply(clean_number)
    df["num_trucks"]      = df["num_trucks"].apply(clean_number)

    # Filter 1 — status must be Active (exact)
    mask_status = df["status"].str.lower() == VALID_STATUS.lower()

    # Filter 2 — auth must CONTAIN the word "authorized" anywhere
    # Fenderr returns: "Authorized for hire", "Authorized for hire;exempt for hire"
    mask_auth = df["auth_status"].str.lower().str.contains("authorized", na=False)

    # Filter 3 — age between MIN and MAX months
    mask_age = df["mcs_date_parsed"].apply(
        lambda d: is_valid_age(d) if d is not None else False
    )

    # Filter 4 — exactly 1 driver
    mask_drivers = df["num_drivers"] == 1

    # Filter 5 — exactly 1 truck
    mask_trucks = df["num_trucks"] == 1

    # Filter 6 — must have phone
    mask_phone = df["phone"].str.strip().str.len() > 0

    all_conditions = (
        mask_status  &
        mask_auth    &
        mask_age     &
        mask_drivers &
        mask_trucks  &
        mask_phone
    )

    filtered_df = df[all_conditions].copy()

    print(f"[Processor] Valid records after filtering: {len(filtered_df)}")
    print(f"[Processor] Rejected records: {len(df) - len(filtered_df)}")

    # Rejection breakdown — helps you understand what's failing
    if len(filtered_df) == 0 and len(df) > 0:
        print(f"  Status Active:     {mask_status.sum()}/{len(df)}")
        print(f"  Authorized:        {mask_auth.sum()}/{len(df)}")
        print(f"  Age valid:         {mask_age.sum()}/{len(df)}")
        print(f"  Drivers == 1:      {mask_drivers.sum()}/{len(df)}")
        print(f"  Trucks == 1:       {mask_trucks.sum()}/{len(df)}")
        print(f"  Has phone:         {mask_phone.sum()}/{len(df)}")

    if filtered_df.empty:
        return pd.DataFrame()

    output_cols = [
        "mc_number", "company_name", "phone", "email",
        "mcs_date", "num_drivers", "num_trucks", "status", "auth_status"
    ]
    existing = [c for c in output_cols if c in filtered_df.columns]
    final_df = filtered_df[existing].copy()
    final_df.columns = [c.replace("_", " ").title() for c in existing]

    return final_df