"""
Unattended weather data fetcher for Andalucía region.

Reads coordinates from unique_coords.csv and fetches weather data
for 2025, saving progress incrementally.
"""
import os
import time
import pandas as pd
from fetch_weather import fetch_weather

# Configuration
START_DATE = "2025-01-01"
END_DATE = "2025-12-31"
BATCH_SIZE = 10
SLEEP_BETWEEN_BATCHES = 120

# Paths (relative to src/data/)
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
COORDS_FILE = os.path.join(DATA_DIR, "processed", "unique_coords.csv")
OUTPUT_FILE = os.path.join(DATA_DIR, "processed", "weather_andalucia_2025.csv")
PROGRESS_FILE = os.path.join(DATA_DIR, "processed", "fetch_progress.txt")


def load_progress():
    """Load the last processed index from progress file."""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return int(f.read().strip())
    return 0


def save_progress(index):
    """Save the current progress index."""
    with open(PROGRESS_FILE, "w") as f:
        f.write(str(index))


def main():
    # Load coordinates
    coords_df = pd.read_csv(COORDS_FILE)
    total_coords = len(coords_df)
    print(f"Loaded {total_coords} coordinates from {COORDS_FILE}")

    # Check progress
    start_index = load_progress()
    if start_index > 0:
        print(f"Resuming from index {start_index}")

    # Process in batches
    for batch_start in range(start_index, total_coords, BATCH_SIZE):
        batch_end = min(batch_start + BATCH_SIZE, total_coords)
        batch = coords_df.iloc[batch_start:batch_end]

        lats = batch["lat"].tolist()
        lons = batch["lon"].tolist()

        print(f"\nBatch {batch_start // BATCH_SIZE + 1}: coords {batch_start}-{batch_end - 1}")

        try:
            # Fetch weather for this batch (Open-Meteo returns daily data directly)
            df = fetch_weather(START_DATE, END_DATE, lats, lons)

            if df is not None and len(df) > 0:
                # Append to output file
                header = not os.path.exists(OUTPUT_FILE)
                df.to_csv(OUTPUT_FILE, mode='a', header=header, index=False)
                print(f"  Saved {len(df)} daily records")

            # Save progress
            save_progress(batch_end)

        except Exception as e:
            print(f"  Error: {e}")
            print(f"  Sleeping for 5 minutes before retry...")
            time.sleep(300)
            continue

        # Sleep between batches to avoid rate limits
        if batch_end < total_coords:
            print(f"  Sleeping {SLEEP_BETWEEN_BATCHES}s before next batch...")
            time.sleep(SLEEP_BETWEEN_BATCHES)

    print("\nDone! All coordinates processed.")


if __name__ == "__main__":
    main()
