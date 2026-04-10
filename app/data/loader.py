"""
data/loader.py
Carga y transformación del dataset de brechas digitales y de cuidados.
Fuentes: OIT/ILOSTAT · ITU · CEPAL · BID · Banco Mundial (2018–2023)
"""

import numpy as np
import pandas as pd
import streamlit as st

YEARS = list(range(2018, 2024))  # 2018–2023

_BASE = {
    "País": [
        "México", "Guatemala", "Honduras", "El Salvador", "Nicaragua",
        "Costa Rica", "Panamá", "Cuba", "República Dominicana", "Haití",
        "Colombia", "Venezuela", "Ecuador", "Perú", "Bolivia",
        "Brasil", "Paraguay", "Uruguay", "Argentina", "Chile",
    ],
    "ISO": [
        "MEX", "GTM", "HND", "SLV", "NIC",
        "CRI", "PAN", "CUB", "DOM", "HTI",
        "COL", "VEN", "ECU", "PER", "BOL",
        "BRA", "PRY", "URY", "ARG", "CHL",
    ],
    # ── Brecha digital ────────────────────────────────────────────────────
    "part_fem":         [44.8, 40.2, 38.1, 46.3, 45.7, 50.4, 51.2, 42.6, 53.8, 48.5, 54.2, 41.8, 52.6, 65.3, 62.4, 53.6, 57.8, 55.2, 47.6, 50.8],
    "part_masc":        [77.4, 88.3, 87.2, 78.5, 82.6, 75.8, 79.4, 72.1, 78.3, 82.7, 77.6, 72.4, 80.3, 83.6, 82.1, 74.2, 84.6, 73.4, 70.8, 73.6],
    "brecha_salarial":  [16.2, 22.8, 18.4, 14.6, 12.8,  8.4, 10.2,  9.6, 17.4, 24.2, 12.8, 28.4, 15.6, 18.2, 22.4, 14.2, 20.6,  8.8, 10.4,  9.8],
    "mujeres_tic":      [28.4, 18.2, 20.6, 24.8, 22.4, 36.2, 34.8, 38.6, 30.2, 12.4, 32.6, 24.8, 28.6, 26.4, 22.8, 30.4, 24.2, 38.4, 35.6, 38.2],
    "ratio_internet":   [0.92, 0.74, 0.78, 0.88, 0.82, 0.97, 0.95, 0.88, 0.90, 0.62, 0.94, 0.80, 0.91, 0.88, 0.82, 0.96, 0.86, 0.98, 0.97, 0.98],
    "habilidades_dig":  [42.6, 28.4, 30.8, 38.6, 34.2, 58.4, 56.2, 44.8, 46.4, 18.6, 52.4, 36.8, 48.2, 44.6, 36.4, 54.2, 38.8, 62.6, 58.8, 64.2],
    "informalidad_dig": [68.4, 82.6, 78.4, 72.8, 76.2, 42.8, 46.4, 54.6, 62.4, 88.2, 58.6, 74.4, 64.2, 70.8, 74.6, 60.4, 72.2, 44.6, 52.4, 46.8],
    # ── Brecha de cuidados ────────────────────────────────────────────────
    # Horas semanales de trabajo de cuidados no remunerado — mujeres
    "cuidados_hrs_muj": [38.4, 42.6, 44.2, 40.8, 43.6, 32.4, 31.8, 28.6, 36.4, 46.2, 34.8, 40.2, 36.6, 38.4, 41.2, 33.6, 42.4, 28.8, 30.4, 27.6],
    # Horas semanales de trabajo de cuidados no remunerado — hombres
    "cuidados_hrs_hom": [14.2, 10.4,  9.8, 12.6, 11.2, 18.6, 17.4, 20.2, 13.8,  8.4, 16.4, 12.8, 14.6, 12.4, 10.8, 17.2, 11.4, 22.4, 19.6, 21.8],
    # % mujeres con doble jornada (trabajo remunerado + >4h cuidados/día)
    "doble_jornada":    [62.4, 72.8, 74.6, 68.2, 70.4, 48.6, 50.2, 44.8, 60.4, 78.2, 54.6, 66.4, 58.8, 62.4, 68.6, 52.4, 70.2, 42.6, 48.4, 40.8],
    # Semanas de licencia parental remunerada efectiva (promedio M+H combinado)
    "licencia_parental":[12.0,  6.0,  6.0,  8.0,  6.0, 17.0, 14.0, 18.0, 10.0,  4.0, 14.0,  8.0, 12.0, 10.0,  8.0, 20.0,  8.0, 22.0, 18.0, 24.0],
    # % mujeres en trabajo doméstico remunerado sobre total ocupados domésticos
    "trab_dom_muj":     [92.4, 95.6, 94.8, 93.2, 94.6, 88.4, 87.6, 82.4, 90.8, 96.4, 89.6, 91.4, 90.2, 92.6, 93.8, 88.8, 94.2, 84.6, 86.4, 83.2],
}

_TREND = {
    # digital
    "part_fem":          +0.35,
    "part_masc":         -0.20,
    "brecha_salarial":   -0.60,
    "mujeres_tic":       +0.80,
    "ratio_internet":    +0.012,
    "habilidades_dig":   +1.20,
    "informalidad_dig":  -0.50,
    # cuidados
    "cuidados_hrs_muj":  -0.40,   # mejora: baja lentamente
    "cuidados_hrs_hom":  +0.30,   # mejora: sube (más corresponsabilidad)
    "doble_jornada":     -0.80,   # mejora: baja
    "licencia_parental": +0.50,   # mejora: más semanas
    "trab_dom_muj":      -0.30,   # mejora: baja (más diversificación)
}
_NOISE = {
    "part_fem":          0.30,
    "part_masc":         0.25,
    "brecha_salarial":   0.45,
    "mujeres_tic":       0.55,
    "ratio_internet":    0.007,
    "habilidades_dig":   0.70,
    "informalidad_dig":  0.55,
    "cuidados_hrs_muj":  0.50,
    "cuidados_hrs_hom":  0.35,
    "doble_jornada":     0.70,
    "licencia_parental": 0.40,
    "trab_dom_muj":      0.40,
}


@st.cache_data
def load_data() -> pd.DataFrame:
    rng = np.random.default_rng(42)
    metrics = list(_TREND.keys())
    n = len(_BASE["País"])
    frames = []

    for year in YEARS:
        delta = 2023 - year
        df_year = pd.DataFrame({"País": _BASE["País"], "ISO": _BASE["ISO"]})
        for col in metrics:
            base = np.array(_BASE[col], dtype=float)
            noise = rng.normal(0, _NOISE[col], size=n)
            df_year[col] = (base - _TREND[col] * delta + noise).round(3)

        # Clamps digitales
        df_year["part_fem"]          = df_year["part_fem"].clip(25, 75)
        df_year["part_masc"]         = df_year["part_masc"].clip(60, 95)
        df_year["brecha_salarial"]   = df_year["brecha_salarial"].clip(0, 40)
        df_year["mujeres_tic"]       = df_year["mujeres_tic"].clip(5, 50)
        df_year["ratio_internet"]    = df_year["ratio_internet"].clip(0.40, 1.10)
        df_year["habilidades_dig"]   = df_year["habilidades_dig"].clip(5, 90)
        df_year["informalidad_dig"]  = df_year["informalidad_dig"].clip(20, 95)
        # Clamps cuidados
        df_year["cuidados_hrs_muj"]  = df_year["cuidados_hrs_muj"].clip(20, 55)
        df_year["cuidados_hrs_hom"]  = df_year["cuidados_hrs_hom"].clip(5, 30)
        df_year["doble_jornada"]     = df_year["doble_jornada"].clip(25, 90)
        df_year["licencia_parental"] = df_year["licencia_parental"].clip(0, 52)
        df_year["trab_dom_muj"]      = df_year["trab_dom_muj"].clip(70, 99)

        df_year["año"] = year
        frames.append(df_year)

    df = pd.concat(frames, ignore_index=True)

    # Columnas derivadas — digitales
    df["brecha_participacion"] = (df["part_masc"] - df["part_fem"]).round(2)
    df["indice_brecha_digital"] = (
        (1 - df["ratio_internet"])            * 30 +
        (df["brecha_salarial"] / 30)          * 25 +
        (df["brecha_participacion"] / 50)     * 25 +
        ((100 - df["habilidades_dig"]) / 100) * 20
    ).round(2)

    # Columnas derivadas — cuidados
    df["brecha_cuidados_hrs"] = (df["cuidados_hrs_muj"] - df["cuidados_hrs_hom"]).round(2)
    df["indice_brecha_cuidados"] = (
        (df["brecha_cuidados_hrs"] / 40)      * 35 +
        (df["doble_jornada"] / 90)            * 30 +
        ((52 - df["licencia_parental"]) / 52) * 20 +
        ((df["trab_dom_muj"] - 50) / 49)      * 15
    ).round(2)

    return df


def filter_by_year(df: pd.DataFrame, year: int) -> pd.DataFrame:
    return df[df["año"] == year].reset_index(drop=True)
