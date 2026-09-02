from pathlib import Path
import pandas as pd
import numpy as np

# Resolve default data path
DEFAULT_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "planets.csv"


def updated_calculate_biosig_suitability(csv_path=DEFAULT_DATA_PATH):
    df = pd.read_csv(csv_path)

    # Definition of stellar luminosity functions
    teff_clean = df["st_teff"].fillna(5778)
    rad_clean = df["st_rad"].fillna(1.0)
    df["st_lum"] = (rad_clean**2) * ((teff_clean / 5778) ** 4)

    # Definition of mass and radius functions
    mass_estimated = df["pl_bmasse"].fillna(
        df["pl_rade"].apply(lambda r: r**3.45 if (pd.notna(r) and r < 1.5) else np.nan)
    )
    df["mass_imputed"] = mass_estimated.fillna(1.0)
    df["rade_imputed"] = df["pl_rade"].fillna(1.0)

    # Definition of density function
    calculated_density = df["mass_imputed"] / (df["rade_imputed"] ** 3)
    df["dens_imputed"] = df["pl_dens"].fillna(calculated_density).fillna(5.51)

    # Definition of escape velocity \(v_{\text{esc}}\) (relative to Earth)
    df["v_esc_rel"] = np.sqrt(df["mass_imputed"] / df["rade_imputed"]).fillna(1.0)

    # Definition of physical complementation for insolation (pl_insol) and equilibrium temperature (pl_eqt)
    s_form_orbit = df["st_lum"] / (df["pl_orbsmax"] ** 2)
    df["insol_imputed"] = df["pl_insol"].fillna(s_form_orbit).fillna(1.0)

    calculated_eqt = 255.0 * (df["insol_imputed"] ** 0.25)
    df["eqt_imputed"] = df["pl_eqt"].fillna(calculated_eqt).fillna(255.0)

    # ESI (Earth Similarity Index) calculation
    def single_esi(row):
        return

    print("--- Top 10 Habitable Planets ---")
    print(df_scored[display_cols].head(10))

    # Resolve data output directory (data/)
    output_dir = Path(__file__).resolve().parent.parent / "data"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "updated_planets_scored.csv"

    df_scored.to_csv(output_file, index=False)

    print(f"Saved scored data to {output_file} successfully!")
