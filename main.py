# main.py — FULL PRODUCTION SCRAPER

from playwright.sync_api import sync_playwright
from src.scraper import scrape_mc
from src.processor import process_carriers
from src.exporter import export_data
from src.progress import save_progress, load_progress
from src.config import MC_RANGE_START, MC_RANGE_END, TARGET_VALID_COUNT
import time


def run():
    # Load saved progress
    progress = load_progress()
    last_mc = progress["last_mc"]
    valid_count = progress["valid_count"]
    processed_count = progress["processed_count"]

    if last_mc > 0:
        print(f"[Resume] Continuing from MC {last_mc + 1}")
        print(f"[Resume] Valid so far: {valid_count} | Processed: {processed_count}")
    else:
        print(f"[Start] Scanning MC {MC_RANGE_START} → {MC_RANGE_END}")
        print(f"[Start] Target: {TARGET_VALID_COUNT} valid carriers")

    all_valid_records = []

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.pages[0]

        input("\nMake sure Chrome is open on Fenderr, then press Enter...")
        print("\n[Scraper] Running...\n")

        for mc in range(max(MC_RANGE_START, last_mc + 1), MC_RANGE_END + 1):

            # Stop when target reached
            if valid_count >= TARGET_VALID_COUNT:
                print(f"\n[Done] Target of {TARGET_VALID_COUNT} valid carriers reached!")
                break

            processed_count += 1

            # Progress report every 20 MCs
            if processed_count % 20 == 0:
                print(f"\n[Progress] Processed: {processed_count} | "
                      f"Valid: {valid_count} | Current MC: {mc}\n")

            # Scrape this MC number
            result = scrape_mc(page, mc)

            if result:
                print(f"  MC {mc} | Status: {result['status']} | "
                      f"Drivers: {result['num_drivers']} | "
                      f"Trucks: {result['num_trucks']} | "
                      f"MCS: {result['mcs_date']}")

                # Quick reject — skip Inactive immediately
                if result["status"].lower() != "active":
                    save_progress(mc, valid_count, processed_count)
                    time.sleep(1.5)
                    continue

                # Run through full filter pipeline
                valid_df = process_carriers([result])

                if not valid_df.empty:
                    valid_count += 1
                    all_valid_records.append(result)

                    print(f"\n  ✅ VALID #{valid_count}: {result['company_name']}")
                    print(f"     MC: {mc} | Phone: {result['phone']} | "
                          f"Drivers: {result['num_drivers']} | "
                          f"Trucks: {result['num_trucks']} | "
                          f"MCS: {result['mcs_date']}\n")

                    # Save every 10 valid records
                    if valid_count % 100 == 0:
                        df = process_carriers(all_valid_records)
                        export_data(df)
                        print(f"[Export] Checkpoint saved — {valid_count} valid records")

            save_progress(mc, valid_count, processed_count)
            time.sleep(2)

        # Final export
        print(f"\n[Final] {valid_count} valid carriers found "
              f"from {processed_count} MCs processed")

        if all_valid_records:
            df = process_carriers(all_valid_records)
            export_data(df)
            print("\n--- VALID CARRIERS ---")
            print(df.to_string(index=False))
        else:
            print("No valid carriers found in this run.")


if __name__ == "__main__":
    run()