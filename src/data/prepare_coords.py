"""
Prepare unique coordinates for Andalucía region.

Loads eBird data, filters to Andalucía, rounds coordinates to 0.1 precision,
and saves unique coordinate pairs.
"""
import os
import pandas as pd

# Paths (relative to src/data/)
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
INPUT_FILE = os.path.join(DATA_DIR, "raw", "ebird_spain_2020-2025.txt")
OUTPUT_FILE = os.path.join(DATA_DIR, "processed", "unique_coords.csv")


def main():
    print(f"Loading bird data from {INPUT_FILE}...")

    # Load only the columns we need
    df = pd.read_csv(
        INPUT_FILE,
        delimiter="\t",
        usecols=["STATE", "LATITUDE", "LONGITUDE"]
    )
    print(f"Loaded {len(df):,} total rows")

    # Filter to Andalucía only
    df = df[df["STATE"] == "Andalucía"]
    print(f"Filtered to {len(df):,} Andalucía rows")

    # Round coordinates to 0.1 precision
    df["lat"] = df["LATITUDE"].round(1)
    df["lon"] = df["LONGITUDE"].round(1)

    # Drop duplicates
    unique_coords = df[["lat", "lon"]].drop_duplicates()

    # Save to CSV
    unique_coords.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSaved {len(unique_coords)} unique coordinates to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
