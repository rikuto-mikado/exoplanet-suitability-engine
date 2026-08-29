import requests

# def fetch_exoplanet_data():
#     url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
#     query = """
#         SELECT top 20 pl_name, pl_bmasse, pl_eqt, pl_orbsmax
#         FROM ps
#         WHERE pl_eqt IS NOT NULL
#     """
#     params = {"query": query, "format": "json"}

#     response = requests.get(url, params=params)
#     response.raise_for_status
#     return response.jspn()

url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"

# NASA Exoplanet Archive (ps table) query
# Selected columns:
# - pl_name: Planet Name
# - hostname: Host Star Name
# - discoverymethod: Discovery Method
# - disc_year: Discovery Year
# - pl_orbper: Orbital Period [days]
# - pl_orbsmax: Semi-Major Axis [AU]
# - pl_rade: Planet Radius [Earth radii]
# - pl_bmasse: Planet Mass [Earth mass]
# - pl_dens: Planet Density [g/cm3]
# - pl_eqt: Equilibrium Temperature [K]
# - pl_insol: Insolation Flux [Earth flux]
# - pl_orbeccen: Orbital Eccentricity
# - st_spectype: Stellar Spectral Type
# - st_teff: Stellar Effective Temperature [K]
# - st_rad: Stellar Radius [Solar radii]
# - st_mass: Stellar Mass [Solar mass]
# - st_age: Stellar Age [Gyr]
# - sy_dist: Distance from Earth [parsec]
# - sy_pnum: Number of Planets in System

query = (
    "SELECT top 100 "
    "pl_name, hostname, discoverymethod, disc_year, "
    "pl_orbper, pl_orbsmax, pl_rade, pl_bmasse, pl_dens, "
    "pl_eqt, pl_insol, pl_orbeccen, st_spectype, st_teff, "
    "st_rad, st_mass, st_age, sy_dist, sy_pnum "
    "FROM ps "
    "WHERE default_flag = 1 AND pl_eqt IS NOT NULL "
    "ORDER BY pl_name"
)

params = {
    "query": query,
    "format": "csv",
}

print("Fetching exoplanet data from NASA Exoplanet Archive...")
response = requests.get(url, params=params)
response.raise_for_status()

from pathlib import Path

# Resolve data output directory (data/)
output_dir = Path(__file__).resolve().parent.parent / "data"
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / "planets.csv"

with open(output_file, "w", encoding="utf-8") as f:
    f.write(response.text)

print(f"Saved data to {output_file} successfully!")
