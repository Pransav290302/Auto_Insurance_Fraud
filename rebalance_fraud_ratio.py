import os

import numpy as np
import pandas as pd


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
SOURCE_CSV = os.path.join(UPLOADS_DIR, "insurance_claims_fraud.csv")
BACKUP_CSV = os.path.join(UPLOADS_DIR, "insurance_claims_fraud_backup_full.csv")


def main(target_fraud_ratio: float = 0.30) -> None:
    if not os.path.exists(SOURCE_CSV):
        raise SystemExit(f"Source CSV not found: {SOURCE_CSV}")

    df = pd.read_csv(SOURCE_CSV)
    if "fraud_reported" not in df.columns:
        raise SystemExit("Expected 'fraud_reported' column in CSV.")

    fraud_flags = (
        df["fraud_reported"]
        .astype(str)
        .str.upper()
        .str.strip()
        .isin(["Y", "YES", "1", "TRUE"])
    )
    fraud_df = df[fraud_flags]
    legit_df = df[~fraud_flags]

    n_total = len(df)
    n_fraud = len(fraud_df)
    n_legit = len(legit_df)
    current_ratio = n_fraud / n_total if n_total > 0 else 0.0

    print(f"Current rows: {n_total} (fraud={n_fraud}, legit={n_legit}), fraud_ratio={current_ratio:.3f}")

    if n_legit == 0:
        raise SystemExit("No legitimate rows found; cannot rebalance.")

    # Max fraud rows allowed to be at or below target_fraud_ratio:
    # target = F / (F + L)  =>  F = target * (F + L)
    # Solve for F => F = (target / (1 - target)) * L
    max_fraud = int((target_fraud_ratio / (1.0 - target_fraud_ratio)) * n_legit)
    max_fraud = max(1, max_fraud)

    n_keep = min(n_fraud, max_fraud)
    print(f"Target fraud_ratio <= {target_fraud_ratio:.2f}. Keeping at most {n_keep} fraud rows.")

    if n_keep <= 0:
        raise SystemExit("Computed 0 fraud rows to keep; aborting to avoid empty fraud class.")

    fraud_sampled = fraud_df.sample(n=n_keep, random_state=42)
    df_new = pd.concat([legit_df, fraud_sampled], axis=0).sample(frac=1.0, random_state=42).reset_index(drop=True)

    new_flags = (
        df_new["fraud_reported"]
        .astype(str)
        .str.upper()
        .str.strip()
        .isin(["Y", "YES", "1", "TRUE"])
    )
    new_n_total = len(df_new)
    new_n_fraud = int(new_flags.sum())
    new_n_legit = new_n_total - new_n_fraud
    new_ratio = new_n_fraud / new_n_total if new_n_total > 0 else 0.0

    print(f"New rows: {new_n_total} (fraud={new_n_fraud}, legit={new_n_legit}), fraud_ratio={new_ratio:.3f}")

    # One-time backup of original file if not already present
    if not os.path.exists(BACKUP_CSV):
        df.to_csv(BACKUP_CSV, index=False)
        print(f"Backup of original data written to: {BACKUP_CSV}")
    else:
        print(f"Backup already exists at: {BACKUP_CSV}")

    # Overwrite source CSV in-place so the whole project uses the rebalanced data
    df_new.to_csv(SOURCE_CSV, index=False)
    print(f"Rebalanced data written to: {SOURCE_CSV}")


if __name__ == "__main__":
    # Default target: 30% fraud or less
    main(0.30)

