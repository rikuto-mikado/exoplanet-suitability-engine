from pathlib import Path
import pandas as pd
import numpy as np

# Resolve default data path
DEFAULT_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "planets.csv"


def calculate_biosig_suitability(csv_path=DEFAULT_DATA_PATH):
    df = pd.read_csv(csv_path)

    def score_temp(temp):
        if pd.isna(temp):
            return 0
        if 273 <= temp <= 320:
            return 70
        return 0

    def score_rocky(row):
        score = 0
        if pd.notna(row["pl_rade"]):
            if 0.8 <= row["pl_rade"] <= 1.5:
                score += 50
            elif 0.5 <= row["pl_rade"] <= 2.0:
                score += 20
        if pd.notna(row["pl_bmasse"]):
            if 0.5 <= row["pl_bmasse"] <= 3.0:
                score += 50
            elif 0.1 <= row["pl_bmasse"] <= 10.0:
                score += 20

        return min(score, 100)

    df["score_temp"] = df["pl_eqt"].apply(score_temp)
    df["score_rocky"] = df.apply(score_rocky, axis=1)

    df["total_score"] = (df["score_temp"] * 0.6) + (df["score_rocky"] * 0.4)

    df_sorted = df.sort_values(by=["total_score", "sy_dist"], ascending=[False, True])

    return df_sorted


if __name__ == "__main__":
    df_scored = calculate_biosig_suitability()

    # Display the top 10
    display_cols = ["pl_name", "pl_eqt", "pl_bmasse", "total_score", "sy_dist"]
    print("--- Top 10 Habitable Candidates ---")
    print(df_scored[display_cols].head(10))

    from pathlib import Path

    output_dir = Path(__file__).resolve().parent.parent / "data"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "planets_scored.csv"

    df_scored.to_csv(output_file, index=False)
    print(f"Saved scored data to {output_file} successfully.")
