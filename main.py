# main.py
from src.processor import process_carriers
from src.exporter import export_data

# ─────────────────────────────────────────────
# MOCK DATA — Fake carrier records that look
# exactly like real scraped data from the site.
# Some will pass filters, some will be rejected.
# ─────────────────────────────────────────────

mock_data = [
    {
        # ✅ SHOULD PASS — Active, Authorized, 1 driver, 1 truck, old enough
        "mc_number": "MC-100001",
        "issuance_date": "01/01/2024",
        "phone": "555-101-0001",
        "email": "carrier1@email.com",
        "status": "Active",
        "auth_status": "Authorized",
        "num_drivers": "1",
        "num_trucks": "1",
    },
    {
        # ✅ SHOULD PASS
        "mc_number": "MC-100002",
        "issuance_date": "03/15/2023",
        "phone": "555-101-0002",
        "email": "carrier2@email.com",
        "status": "Active",
        "auth_status": "Authorized",
        "num_drivers": "1",
        "num_trucks": "1",
    },
    {
        # ❌ FAIL — status is Inactive
        "mc_number": "MC-100003",
        "issuance_date": "01/10/2024",
        "phone": "555-101-0003",
        "email": "carrier3@email.com",
        "status": "Inactive",
        "auth_status": "Authorized",
        "num_drivers": "1",
        "num_trucks": "1",
    },
    {
        # ❌ FAIL — not Authorized
        "mc_number": "MC-100004",
        "issuance_date": "01/10/2024",
        "phone": "555-101-0004",
        "email": "carrier4@email.com",
        "status": "Active",
        "auth_status": "Not Authorized",
        "num_drivers": "1",
        "num_trucks": "1",
    },
    {
        # ❌ FAIL — too new, only 2 months old
        "mc_number": "MC-100005",
        "issuance_date": "04/01/2026",
        "phone": "555-101-0005",
        "email": "carrier5@email.com",
        "status": "Active",
        "auth_status": "Authorized",
        "num_drivers": "1",
        "num_trucks": "1",
    },
    {
        # ❌ FAIL — 3 trucks, too many
        "mc_number": "MC-100006",
        "issuance_date": "01/10/2024",
        "phone": "555-101-0006",
        "email": "carrier6@email.com",
        "status": "Active",
        "auth_status": "Authorized",
        "num_drivers": "1",
        "num_trucks": "3",
    },
    {
        # ❌ FAIL — 3 drivers, too many
        "mc_number": "MC-100007",
        "issuance_date": "01/10/2024",
        "phone": "555-101-0007",
        "email": "carrier7@email.com",
        "status": "Active",
        "auth_status": "Authorized",
        "num_drivers": "3",
        "num_trucks": "1",
    },
    {
        # ✅ SHOULD PASS
        "mc_number": "MC-100008",
        "issuance_date": "06/20/2023",
        "phone": "555-101-0008",
        "email": "carrier8@email.com",
        "status": "Active",
        "auth_status": "Authorized",
        "num_drivers": "1",
        "num_trucks": "1",
    },
    {
        # ❌ FAIL — missing email
        "mc_number": "MC-100009",
        "issuance_date": "01/10/2024",
        "phone": "555-101-0009",
        "email": "",
        "status": "Active",
        "auth_status": "Authorized",
        "num_drivers": "1",
        "num_trucks": "1",
    },
    {
        # ❌ FAIL — Inactive and too many trucks
        "mc_number": "MC-100010",
        "issuance_date": "01/10/2024",
        "phone": "555-101-0010",
        "email": "carrier10@email.com",
        "status": "Inactive",
        "auth_status": "Authorized",
        "num_drivers": "1",
        "num_trucks": "4",
    },
]

if __name__ == "__main__":
    print("=" * 45)
    print("   CARRIER SCRAPER — PIPELINE TEST")
    print("=" * 45)

    # Step 1 — Process and filter
    print("\n[Step 1] Running processor...")
    valid_df = process_carriers(mock_data)

    # Step 2 — Export to CSV and Excel
    print("\n[Step 2] Running exporter...")
    export_data(valid_df)

    # Step 3 — Preview in terminal
    print("\n[Step 3] Preview of valid records:")
    print("-" * 45)
    print(valid_df.to_string(index=False))
    print("-" * 45)
    print("\n✅ Pipeline test complete")