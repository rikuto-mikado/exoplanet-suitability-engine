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
