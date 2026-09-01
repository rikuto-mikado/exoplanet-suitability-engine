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

    # Rocky Planet Score(score_rocky)
    def score_rocky(row):
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

    # Star Safety Score(score_star)
    def score_star(row):
        teff = row["st_teff"]
        age = row["st_age"]
        score = 0

        if pd.notna(teff):
            if 3900 <= teff <= 5200:
                score += 60
            elif 5200 <= teff <= 6000:
                score += 50
            elif teff < 3900:
                score += 30
            else:
                score += 0
        else:
            score += 30

        if pd.notna(age):
            if 3.0 <= age <= 8.0:
                score += 40
            elif age < 1.0:
                score += 10
            else:
                score += 20
        else:
            score += 20

        return min(score, 100)

    # Observability Score(score_obs)
    def score_obs(dist):
        if pd.isna(dist):
            return 20
        if dist < 20:
            return 100
        elif 20 <= dist <= 50:
            return 70
        return 20

    # Apply to each dataframe row
    df["score_temp"] = df.apply(score_temp, axis=1)
    df["score_rocky"] = df.apply(score_rocky, axis=1)
    df["score_orbit"] = df["pl_orbeccen"].apply(score_orbit)
    df["score_star"] = df.apply(score_star, axis=1)
    df["score_obs"] = df["sy_dist"].apply(score_obs)

    # Habitability Score (combined temp, rocky, orbit)
    habitability_score = (
        (df["score_temp"] * 0.5) + (df["score_rocky"] * 0.3) + (df["score_orbit"] * 0.2)
    )

    # Total Suitability Score Calculation
    df["total_score"] = (
        (habitability_score * 0.50)
        + (df["score_star"] * 0.25)
        + (df["score_obs"] * 0.25)
    ).round(2)

    df_sorted = df.sort_values(by=["total_score", "sy_dist"], ascending=[False, True])

    return df_sorted


if __name__ == "__main__":
    df_scored = calculate_biosig_suitability()

    display_cols = [
        "pl_name",
        "score_temp",
        "score_rocky",
        "score_orbit",
        "score_star",
        "score_obs",
        "total_score",
        "sy_dist",
    ]
    print("--- Top 10 Habitable Planets ---")
    print(df_scored[display_cols].head(10))

    # Resolve data output directory (data/)
    output_dir = Path(__file__).resolve().parent.parent / "data"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "planets_scored.csv"

    df_scored.to_csv(output_file, index=False)

    print(f"Saved scored data to {output_file} successfully!")
