# merge.py

import pandas as pd
import os
import glob

OUTPUT_DIR = "output"

def merge_all_files():
    csv_files = glob.glob(os.path.join(OUTPUT_DIR, "*.csv"))

    if not csv_files:
        print("No CSV files found in output folder.")
        return

    print(f"Found {len(csv_files)} CSV files:")

    all_dfs = []
    for file in csv_files:
        df = pd.read_csv(file)
        print(f"  {file} → {len(df)} records")
        all_dfs.append(df)

    # Merge into one DataFrame
    merged_df = pd.concat(all_dfs, ignore_index=True)

    # Show actual column names so we know what we're working with
    print(f"\nColumns found: {list(merged_df.columns)}")

    # Remove duplicates using first column (MC number column)
    first_col = merged_df.columns[0]
    print(f"Deduplicating on column: '{first_col}'")

    before = len(merged_df)
    merged_df.drop_duplicates(subset=[first_col], keep="first", inplace=True)
    after = len(merged_df)

    if before != after:
        print(f"Removed {before - after} duplicate records")

    print(f"\nTotal unique records: {len(merged_df)}")

    # Save merged file
    output_path = os.path.join(OUTPUT_DIR, "MERGED_valid_carriers.xlsx")
    merged_df.to_excel(output_path, index=False, sheet_name="Valid Carriers")
    print(f"\n✅ Merged file saved → {output_path}")

if __name__ == "__main__":
    merge_all_files()