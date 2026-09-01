from pathlib import Path
import pandas as pd
import numpy as np

# Resolve default data path
DEFAULT_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "planets.csv"


def updated_calculate_biosig_suitability(csv_path=DEFAULT_DATA_PATH):
    df = pd.read_csv(csv_path)

    print("--- Top 10 Habitable Planets ---")
    print(df_scored[display_cols].head(10))

    # Resolve data output directory (data/)
    output_dir = Path(__file__).resolve().parent.parent / "data"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "updated_planets_scored.csv"

    df_scored.to_csv(output_file, index=False)

    print(f"Saved scored data to {output_file} successfully!")
