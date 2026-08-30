# Exoplanet Scoring Metrics Guide

This guide explains in simple terms how we calculate exoplanet suitability scores by combining different data points from our dataset.

---

## 1. The Core Idea

We want to answer three simple questions for each planet:

1. **Can liquid water and life exist on this planet?** (Habitability)
2. **Is the parent star safe and stable?** (Star Safety)
3. **Can our telescopes observe it from Earth?** (Observability)

By combining these, we produce a **Total Score (0 to 100)** to find the most promising target planets.

---

## 2. The Data Parameters We Use

Here is what our raw data columns mean:

| Column                    | What It Means                             | Ideal Value for Life                            |
| :------------------------ | :---------------------------------------- | :---------------------------------------------- |
| `pl_eqt`                  | Planet temperature (in Kelvin)            | ~250 K to 320 K (0°C to 47°C)                   |
| `pl_insol`                | Sunlight received compared to Earth       | Around 1.0 (Earth = 1.0)                        |
| `pl_rade`                 | Planet size (Earth radius = 1.0)          | 0.8 to 1.5 (similar to Earth)                   |
| `pl_bmasse`               | Planet mass (Earth mass = 1.0)            | 0.5 to 3.0 (rocky surface gravity)              |
| `pl_dens`                 | Planet density ($\text{g/cm}^3$)          | $\ge 4.0$ (rocky, not gas)                      |
| `pl_orbeccen`             | Orbital shape ($0 = \text{circle}$)       | Near 0 (stable climate throughout the year)     |
| `st_teff` / `st_spectype` | Host star temperature / type              | 3,900 K to 6,000 K (Orange & Yellow stars)      |
| `st_age`                  | Age of the star system (in Billion years) | 3 to 8 Gyr (mature & stable)                    |
| `sy_dist`                 | Distance from Earth (in Parsecs)          | Closer is better (< 50 pc)                      |
| `st_rad`                  | Host star size                            | Smaller stars make planet transit easier to see |
| `sy_pnum`                 | Number of planets in the system           | 2+ (interesting multi-planet systems)           |

---

## 3. How We Combine Parameters to Build Each Index

### Metric 1: Temperature & Climate Score (`score_temp`)

- **What it checks**: Is the planet in the "Goldilocks" zone where water can be liquid?
- **Parameters used**: `pl_eqt` (Temperature) and `pl_insol` (Sunlight)
- **Logic**:
  - If Temperature is between **250 K and 320 K** $\rightarrow$ **100 points**
  - If Temperature is between **200 K and 350 K** $\rightarrow$ **60 points** (partial score)
  - Otherwise $\rightarrow$ **0 points** (too hot or too cold)

---

### Metric 2: Rocky Planet Score (`score_rocky`)

- **What it checks**: Is the planet a solid rocky world like Earth, rather than a giant ball of gas like Neptune or Jupiter?
- **Parameters used**: `pl_rade` (Size), `pl_bmasse` (Mass), `pl_dens` (Density)
- **Logic**:
  - **Size**: Radius $\le 1.6 \times \text{Earth}$ means it is likely solid rock $\rightarrow$ **50 points**
  - **Mass / Density**: Mass between $0.5$ and $3.0 \times \text{Earth}$ OR density $\ge 4.0\text{ g/cm}^3$ $\rightarrow$ **50 points**
  - **Combined**: Add both points together (Maximum = 100 points).

---

### Metric 3: Orbit Stability Score (`score_orbit`)

- **What it checks**: Does the planet move in a calm, near-circular circle, or an extreme oval that causes wild climate swings?
- **Parameters used**: `pl_orbeccen` (Eccentricity)
- **Logic**:
  - Circular orbit ($e < 0.1$) $\rightarrow$ **100 points**
  - Slight oval ($0.1 \le e \le 0.25$) $\rightarrow$ **60 points**
  - Extreme oval ($e > 0.25$) $\rightarrow$ **0 points**

---

### Metric 4: Star Safety Score (`score_star`)

- **What it checks**: Is the host star peaceful and long-lived, or violent with dangerous solar flares?
- **Parameters used**: `st_teff` (Star Temp) and `st_age` (Star Age)
- **Logic**:
  - **Star Type**:
    - Orange Dwarf (K-type, 3900–5200 K) $\rightarrow$ **100 points** (Most stable & calm)
    - Yellow Dwarf (G-type like Sun, 5200–6000 K) $\rightarrow$ **90 points** (Proven good for life)
    - Red Dwarf (M-type, < 3900 K) $\rightarrow$ **60 points** (Prone to strong flares)
    - Giant / Hot Stars (> 6500 K) $\rightarrow$ **0 points** (Die too quickly)
  - **Star Age**:
    - Age between 3.0 and 8.0 Billion years $\rightarrow$ **100 points**
    - Too young (< 1.0 Billion years) $\rightarrow$ **30 points** (violent flare activity)

---

### Metric 5: Observability Score (`score_obs`)

- **What it checks**: Can telescopes like JWST easily take clear pictures or analyze the planet's atmosphere?
- **Parameters used**: `sy_dist` (Distance), `pl_rade` (Planet Size), `st_rad` (Star Size)
- **Logic**:
  - **Distance**:
    - Closer than 20 pc (~65 light-years) $\rightarrow$ **100 points**
    - 20 to 50 pc $\rightarrow$ **70 points**
    - Over 100 pc $\rightarrow$ **20 points**
  - **Transit Signal**: If the planet is relatively large compared to its host star (`pl_rade / st_rad`), atmospheric detection is much easier.

---

## 4. Overall Total Score Formula

We group the metrics into three simple categories:

$$\text{Habitability Score} = (\text{Temperature Score} \times 0.5) + (\text{Rocky Score} \times 0.3) + (\text{Orbit Score} \times 0.2)$$

$$\text{Star Score} = \text{Star Safety Score}$$

$$\text{Observability Score} = \text{Distance \& Visibility Score}$$

### Final Total:

$$\text{Total Score} = (\text{Habitability Score} \times 0.50) + (\text{Star Score} \times 0.25) + (\text{Observability Score} \times 0.25)$$

---

## 5. Sorting the Results

In the final `planets_scored.csv`:

1. **First Sort**: `total_score` from Highest to Lowest (best candidates at the top).
2. **Second Sort**: `sy_dist` from Nearest to Farthest (nearest planets win ties).
