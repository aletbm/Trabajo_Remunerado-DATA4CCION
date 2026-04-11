import os
import pandas as pd
import streamlit as st

_DATA_DIR = os.path.join(os.path.dirname(__file__))

PAISES = [
    "ARGENTINA", "CHILE", "COLOMBIA", "COSTA RICA", "EL SALVADOR",
    "GUATEMALA", "PERU", "REPUBLICA DOMINICANA", "URUGUAY",
]

ISO_MAP = {
    "ARGENTINA":           "ARG",
    "CHILE":               "CHL",
    "COLOMBIA":            "COL",
    "COSTA RICA":          "CRI",
    "EL SALVADOR":         "SLV",
    "GUATEMALA":           "GTM",
    "PERU":                "PER",
    "REPUBLICA DOMINICANA":"DOM",
    "URUGUAY":             "URY",
}

# Grupos que conforman la edad activa (15–64)
EDAD_ACTIVA = {
    "15-19","20-24","25-29","30-34","35-39",
    "40-44","45-49","50-54","55-59","60-64",
}


@st.cache_data
def load_poblacion() -> pd.DataFrame:
    """
    Retorna df_poblacion.csv normalizado.
    Columnas: pais, grupos_edad, anios, miles_personas_a_mitad_anio
    """
    df = pd.read_csv(os.path.join(_DATA_DIR, "df_poblacion.csv"))
    df.columns = df.columns.str.strip()
    df["pais"] = df["pais"].str.strip().str.upper()
    return df[df["pais"].isin(PAISES)].copy()


@st.cache_data
def load_tiempo_internet() -> pd.DataFrame:
    """
    Retorna df_tiempo_internet.csv normalizado.
    Columnas: pais, tiempo_total_trabajo, tiempo_trabajo_remunerado,
              tiempo_trabajo_no_remunerado, porcentaje_uso_internet
    """
    df = pd.read_csv(os.path.join(_DATA_DIR, "df_tiempo_internet.csv"))
    df.columns = df.columns.str.strip()
    df["pais"] = df["pais"].str.strip().str.upper()
    return df[df["pais"].isin(PAISES)].copy()


@st.cache_data
def load_riesgo() -> pd.DataFrame:
    """
    Retorna df_riesgo.csv normalizado.
    Columnas: pais, vulnerabilidad, peso_poblacional_edad_activa, riesgo_poblacional
    """
    df = pd.read_csv(os.path.join(_DATA_DIR, "df_riesgo.csv"))
    df.columns = df.columns.str.strip()
    df["pais"] = df["pais"].str.strip().str.upper()
    return df[df["pais"].isin(PAISES)].copy()


@st.cache_data
def load_indicadores() -> pd.DataFrame:
    """
    Combina los tres datasets y calcula todos los indicadores.
    Retorna un DataFrame con una fila por país:
        País, ISO,
        carga_cuidados, brecha_digital,
        vulnerabilidad_estructural, peso_poblacional, riesgo_poblacional
    """
    df_ti = load_tiempo_internet()
    df_r  = load_riesgo()

    # ── Indicadores desde df_tiempo_internet ──────────────────────────────
    df_ti["carga_cuidados"] = (
        df_ti["tiempo_trabajo_no_remunerado"] / df_ti["tiempo_total_trabajo"] * 100
    ).round(2)
    df_ti["brecha_digital"] = (100 - df_ti["porcentaje_uso_internet"]).round(2)

    # ── Merge con df_riesgo ───────────────────────────────────────────────
    df = df_ti.merge(df_r, on="pais", how="left")

    df = df.rename(columns={
        "pais":                       "País",
        "vulnerabilidad":             "vulnerabilidad_estructural",
        "peso_poblacional_edad_activa": "peso_poblacional",
    })

    df["vulnerabilidad_estructural"] = df["vulnerabilidad_estructural"].round(2)
    df["peso_poblacional"]           = df["peso_poblacional"].round(2)
    df["riesgo_poblacional"]         = df["riesgo_poblacional"].round(2)
    df["ISO"] = df["País"].map(ISO_MAP)

    cols = [
        "País", "ISO",
        "carga_cuidados", "brecha_digital",
        "vulnerabilidad_estructural", "peso_poblacional", "riesgo_poblacional",
    ]
    return df[cols].reset_index(drop=True)
