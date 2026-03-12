"""
Update year values in uploads/fraud_oracle.csv:

- 1994 -> 2024
- 1995 -> 2025
- 1996 -> 2023

- For numeric columns: exact 1994/1995/1996 become 2024/2025/2023.
- For string columns: substrings "1994"/"1995"/"1996" become "2024"/"2025"/"2023".
- Overwrites uploads/fraud_oracle.csv in place.
"""

import os
import pandas as pd


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
CSV_PATH = os.path.join(UPLOADS_DIR, "fraud_oracle.csv")


def main() -> None:
    if not os.path.exists(CSV_PATH):
        raise SystemExit(f"CSV not found: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)

    for col in df.columns:
        s = df[col]
        # Numeric: replace exact year values
        if pd.api.types.is_integer_dtype(s) or pd.api.types.is_float_dtype(s):
            df[col] = s.replace({1994: 2024, 1995: 2025, 1996: 2023})
        else:
            # String-like: replace substrings
            s_str = s.astype(str)
            s_str = (
                s_str.str.replace("1994", "2024")
                .str.replace("1995", "2025")
                .str.replace("1996", "2023")
            )
            df[col] = s_str

    df.to_csv(CSV_PATH, index=False)
    print(f"Updated years 1994->2024 and 1995->2025 in {CSV_PATH}")


if __name__ == "__main__":
    main()

