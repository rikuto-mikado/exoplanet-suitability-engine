import pandas as pd
import numpy as np


def calculate_biosig_suitability(csv_path="planets.csv"):
    df = pd.read_csv(csv_path)

    def score_temp(temp):
        if pd.isna(temp):
            return 0
        if 273 <= temp <= 320:
            return 70
        return 0


df = pd.read_csv("planets.csv")

print("--- Analysis data ---")
print()
