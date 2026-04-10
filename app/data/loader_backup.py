import pandas as pd
import streamlit as st


@st.cache_data
def load_data() -> pd.DataFrame:
    raw = {
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
        # Tasa de participación laboral femenina (%)
        "part_fem": [
            44.8, 40.2, 38.1, 46.3, 45.7, 50.4, 51.2, 42.6, 53.8, 48.5,
            54.2, 41.8, 52.6, 65.3, 62.4, 53.6, 57.8, 55.2, 47.6, 50.8,
        ],
        # Tasa de participación laboral masculina (%)
        "part_masc": [
            77.4, 88.3, 87.2, 78.5, 82.6, 75.8, 79.4, 72.1, 78.3, 82.7,
            77.6, 72.4, 80.3, 83.6, 82.1, 74.2, 84.6, 73.4, 70.8, 73.6,
        ],
        # Brecha salarial de género — hombres ganan X% más (%)
        "brecha_salarial": [
            16.2, 22.8, 18.4, 14.6, 12.8,  8.4, 10.2,  9.6, 17.4, 24.2,
            12.8, 28.4, 15.6, 18.2, 22.4, 14.2, 20.6,  8.8, 10.4,  9.8,
        ],
        # Mujeres en empleo digital / TIC (%)
        "mujeres_tic": [
            28.4, 18.2, 20.6, 24.8, 22.4, 36.2, 34.8, 38.6, 30.2, 12.4,
            32.6, 24.8, 28.6, 26.4, 22.8, 30.4, 24.2, 38.4, 35.6, 38.2,
        ],
        # Ratio acceso internet mujer/hombre (1.0 = paridad)
        "ratio_internet": [
            0.92, 0.74, 0.78, 0.88, 0.82, 0.97, 0.95, 0.88, 0.90, 0.62,
            0.94, 0.80, 0.91, 0.88, 0.82, 0.96, 0.86, 0.98, 0.97, 0.98,
        ],
        # Índice habilidades digitales femeninas (0–100)
        "habilidades_dig": [
            42.6, 28.4, 30.8, 38.6, 34.2, 58.4, 56.2, 44.8, 46.4, 18.6,
            52.4, 36.8, 48.2, 44.6, 36.4, 54.2, 38.8, 62.6, 58.8, 64.2,
        ],
        # Mujeres en empleo digital informal (%)
        "informalidad_dig": [
            68.4, 82.6, 78.4, 72.8, 76.2, 42.8, 46.4, 54.6, 62.4, 88.2,
            58.6, 74.4, 64.2, 70.8, 74.6, 60.4, 72.2, 44.6, 52.4, 46.8,
        ],
    }

    df = pd.DataFrame(raw)

    # ── Columnas derivadas ─────────────────────────────────────────────────
    df["brecha_participacion"] = df["part_masc"] - df["part_fem"]

    df["indice_brecha_digital"] = (
        (1 - df["ratio_internet"])          * 30 +
        (df["brecha_salarial"] / 30)        * 25 +
        (df["brecha_participacion"] / 50)   * 25 +
        ((100 - df["habilidades_dig"]) / 100) * 20
    ).round(2)

    return df
