import pandas as pd
import os
import re


def to_snake_case(col: str) -> str:
    col = col.strip()
    col = re.sub(r"[\s\-]+", "_", col)
    col = col.lower()
    return col


def main():
    input_path = "data/bronze/happiness_raw.csv"
    output_path = "data/silver/happiness_clean.parquet"

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print(f"Reading {input_path}...")
    df = pd.read_csv(input_path)

    # Rename all columns to snake_case
    df.columns = [to_snake_case(c) for c in df.columns]
    print(f"Columns after rename: {df.columns.tolist()}")

    # Identify happiness score column (ladder_score after rename)
    # Drop rows where ladder_score is null
    score_col = "ladder_score"
    before = len(df)
    df = df.dropna(subset=[score_col])
    after = len(df)
    print(f"Dropped {before - after} rows with null {score_col}. Remaining: {after}")

    # Add ingestion_date
    df["ingestion_date"] = "2026-04-10"

    df.to_parquet(output_path, index=False)
    print(f"Saved cleaned parquet to {output_path}")
    print(f"Shape: {df.shape}")


if __name__ == "__main__":
    main()
