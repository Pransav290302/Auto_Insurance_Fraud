"""
Augment uploads/insurance.csv with 2000 extra rows.

- Samples existing rows with replacement
- Replaces incident_date with random dates between 2024-01-01 and 2025-12-31
- Keeps all other fields as in the sampled rows
"""

import os
import random
from datetime import date, timedelta

import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
CSV_PATH = os.path.join(UPLOADS_DIR, "insurance.csv")

N_EXTRA_ROWS = 2000


def random_date_2024_2025() -> str:
    start = date(2024, 1, 1)
    end = date(2025, 12, 31)
    delta_days = (end - start).days
    offset = random.randint(0, delta_days)
    d = start + timedelta(days=offset)
    # Match existing format "m/d/YYYY 0:00"
    return d.strftime("%-m/%-d/%Y 0:00") if os.name != "nt" else d.strftime("%#m/%#d/%Y 0:00")


def main() -> None:
    if not os.path.exists(CSV_PATH):
        raise SystemExit(f"CSV not found: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)
    if "incident_date" not in df.columns:
        raise SystemExit("Column 'incident_date' not found in insurance.csv")

    # Sample with replacement
    extra = df.sample(n=N_EXTRA_ROWS, replace=True, random_state=42).reset_index(drop=True)

    # Assign new random incident dates in 2024–2025
    extra["incident_date"] = [random_date_2024_2025() for _ in range(len(extra))]

    # Append and save (overwrite original file)
    out = pd.concat([df, extra], ignore_index=True)
    out.to_csv(CSV_PATH, index=False)
    print(f"Appended {N_EXTRA_ROWS} rows. New total: {len(out)} rows -> {CSV_PATH}")


if __name__ == "__main__":
    main()

