from pathlib import Path
import pandas as pd
import numpy as np

# Resolve default data path
DEFAULT_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "planets.csv"


# def calculate_biosig_suitability(csv_path=DEFAULT_DATA_PATH):
#     df = pd.read_csv(csv_path)

#     def score_temp(temp):
#         if pd.isna(temp):
#             return 0
#         if 273 <= temp <= 320:
#             return 70
#         return 0

#     def score_rocky(row):
#         score = 0
#         if pd.notna(row["pl_rade"]):
#             if 0.8 <= row["pl_rade"] <= 1.5:
#                 score += 50
#             elif 0.5 <= row["pl_rade"] <= 2.0:
#                 score += 20
#         if pd.notna(row["pl_bmasse"]):
#             if 0.5 <= row["pl_bmasse"] <= 3.0:
#                 score += 50
#             elif 0.1 <= row["pl_bmasse"] <= 10.0:
#                 score += 20

#         return min(score, 100)

#     df["score_temp"] = df["pl_eqt"].apply(score_temp)
#     df["score_rocky"] = df.apply(score_rocky, axis=1)

#     df["total_score"] = (df["score_temp"] * 0.6) + (df["score_rocky"] * 0.4)

#     df_sorted = df.sort_values(by=["total_score", "sy_dist"], ascending=[False, True])

#     return df_sorted


# if __name__ == "__main__":
#     df_scored = calculate_biosig_suitability()

#     # Display the top 10
#     display_cols = ["pl_name", "pl_eqt", "pl_bmasse", "total_score", "sy_dist"]
#     print("--- Top 10 Habitable Candidates ---")
#     print(df_scored[display_cols].head(10))

#     from pathlib import Path

#     output_dir = Path(__file__).resolve().parent.parent / "data"
#     output_dir.mkdir(parents=True, exist_ok=True)
#     output_file = output_dir / "planets_scored.csv"

#     df_scored.to_csv(output_file, index=False)
#     print(f"Saved scored data to {output_file} successfully.")


def calculate_biosig_suitability(csv_path=DEFAULT_DATA_PATH):
    df = pd.read_csv(csv_path)

    # Temputure and Climate Score(score_temp)
    def score_temp(row):
        temp = row["pl_eqt"]
        insol = row["pl_insol"]

        if pd.notna(temp):
            if 250 <= temp <= 320:
                return 100
            elif 200 <= temp <= 350:
                return 60
            return 0

        elif pd.notna(insol):
            if 0.35 <= insol <= 1.11:
                return 100
            elif 0.35 <= insol <= 1.5:
                return 60
            return 0
        return 0

    # Rockly Planet Score(score_rockly)
    def score_rockly(row):
        score = 0

        if pd.notna(row["pl_rade"]):
            if row["pl_rade"] <= 1.6:
                score += 50

        if pd.notna(row["pl_bmasse"]) and (0.5 <= row["pl_bmasse"] <= 3.0):
            score += 50
        elif pd.notna(row["pl_bmasse"]) and (row["pl_dens"] >= 4.0):
            score += 50
        return min(score, 100)

    # Orbit Stability Score(score_orbit)
    def score_orbit(eccen):
        if pd.isna(eccen):
            return 50
        if eccen < 0.1:
            return 100
        elif 0.1 <= eccen <= 0.25:
            return 60
        return 0
