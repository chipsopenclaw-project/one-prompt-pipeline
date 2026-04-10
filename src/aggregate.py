import pandas as pd
import os


def main():
    input_path = "data/silver/happiness_clean.parquet"
    output_path = "data/gold/happiness_aggregated.parquet"

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print(f"Reading {input_path}...")
    df = pd.read_parquet(input_path)
    print(f"Columns: {df.columns.tolist()}")
    print(f"Shape: {df.shape}")

    # Region column after snake_case is 'regional_indicator'
    region_col = "regional_indicator"
    score_col = "ladder_score"

    # 1. Calculate average happiness_score grouped by region
    region_avg = df.groupby(region_col)[score_col].mean().reset_index()
    region_avg.columns = [region_col, "avg_regional_happiness"]

    # 2. Calculate rank per country within its region (descending, method='min')
    df["regional_rank"] = df.groupby(region_col)[score_col].rank(
        ascending=False, method="min"
    ).astype(int)

    # 3. Add category column
    def categorize(score):
        if score >= 7:
            return "Happy"
        elif score >= 5:
            return "Neutral"
        else:
            return "Unhappy"

    df["category"] = df[score_col].apply(categorize)

    # 4. Merge avg_regional_happiness onto each row
    df = df.merge(region_avg, on=region_col, how="left")

    df.to_parquet(output_path, index=False)
    print(f"Saved aggregated parquet to {output_path}")
    print(f"Shape: {df.shape}")
    print(df[[region_col, "country_name", score_col, "regional_rank", "category", "avg_regional_happiness"]].head(10))


if __name__ == "__main__":
    main()
