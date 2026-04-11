import pandas as pd
import numpy as np
from pathlib import Path

INPUT_DIR = "data/"
OUTPUT_DIR = "app/data/"

INTERNET_CSV   = INPUT_DIR + "Uso del Internet.csv"
TRABAJO_CSV    = INPUT_DIR + "Tiempo total de trabajo.csv"
POBLACION_CSV  = INPUT_DIR + "Poblacion por genero y edad.csv"


def estandarizar_pais(serie: pd.Series) -> pd.Series:
    """Strip, uppercase, quitar acentos."""
    return (
        serie
        .str.strip()
        .str.upper()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )


def procesar_internet() -> pd.DataFrame:
    df = pd.read_csv(INTERNET_CSV)

    for col in ["SEX_LABEL", "AGE_LABEL", "REF_AREA_LABEL", "INDICATOR_LABEL"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    df["TIME_PERIOD"] = pd.to_numeric(df["TIME_PERIOD"], errors="coerce").astype("Int64")
    df = df.dropna(subset=["SEX_LABEL", "REF_AREA_LABEL", "TIME_PERIOD"])

    paises_objetivo = [
        "Argentina", "Colombia", "Dominican Republic", "Costa Rica",
        "Guatemala", "Uruguay", "Chile", "El Salvador", "Peru",
    ]

    df = df[
        (df["SEX_LABEL"] == "Female")
        & (df["TIME_PERIOD"].between(2020, 2025))
        & (df["REF_AREA_LABEL"].isin(paises_objetivo))
        & (df["AGE_LABEL"] == "All age ranges or no breakdown by age")
    ]

    cols = [c for c in ["REF_AREA_LABEL", "TIME_PERIOD", "AGE_LABEL", "OBS_VALUE"] if c in df.columns]
    df = df[cols].sort_values(["REF_AREA_LABEL", "TIME_PERIOD"])

    ultimos = df.groupby("REF_AREA_LABEL", as_index=False)["TIME_PERIOD"].max()
    df = df.merge(ultimos, on=["REF_AREA_LABEL", "TIME_PERIOD"], how="inner")

    df = df.rename(columns={
        "REF_AREA_LABEL": "pais",
        "TIME_PERIOD":    "anio",
        "AGE_LABEL":      "edad",
        "OBS_VALUE":      "porcentaje_uso_internet",
    })

    dicc_paises = {
        "Argentina":        "Argentina",
        "Chile":            "Chile",
        "Colombia":         "Colombia",
        "Costa Rica":       "Costa Rica",
        "Dominican Republic": "Republica Dominicana",
        "El Salvador":      "El Salvador",
        "Guatemala":        "Guatemala",
        "Peru":             "Peru",
        "Uruguay":          "Uruguay",
    }
    df["pais"] = df["pais"].replace(dicc_paises)
    df["pais"] = estandarizar_pais(df["pais"])
    return df


def procesar_tiempo_trabajo() -> pd.DataFrame:
    df = pd.read_csv(TRABAJO_CSV, encoding="latin-1")

    df = df.drop(columns=["Sexo__población", "unit", "notes_ids", "source_id"], errors="ignore")

    df = df.rename(columns={
        "indicator":           "indicador",
        "Años__ESTANDAR":      "anios",
        "País__ESTANDAR":      "pais",
        "Tipos de trabajo":    "tipo_trabajo",
        "value":               "promedio_horas_semanales",
    })

    df["promedio_horas_semanales"] = pd.to_numeric(
        df["promedio_horas_semanales"].astype(str).str.replace(",", "."),
        errors="coerce",
    )

    df["pais"] = estandarizar_pais(df["pais"])

    df_wide = df.pivot(
        index="pais", columns="tipo_trabajo", values="promedio_horas_semanales"
    ).reset_index()
    df_wide.columns.name = None

    df_extra = df[["pais", "indicador", "anios"]].drop_duplicates()
    df_wide = df_wide.merge(df_extra, on="pais", how="left")

    df_wide = df_wide.rename(columns={
        "Tiempo total de trabajo":       "tiempo_total_trabajo",
        "Tiempo trabajo remunerado":     "tiempo_trabajo_remunerado",
        "Tiempo trabajo no remunerado":  "tiempo_trabajo_no_remunerado",
    })

    return df_wide[["indicador", "anios", "pais",
                    "tiempo_total_trabajo", "tiempo_trabajo_remunerado",
                    "tiempo_trabajo_no_remunerado"]]


def procesar_poblacion() -> pd.DataFrame:
    df = pd.read_csv(POBLACION_CSV, encoding="latin-1")

    df = df.rename(columns={
        "indicator":                  "indicador",
        "País__ESTANDAR":             "pais",
        "Grupos quinquenales de edad": "grupos_edad",
        "Años__ESTANDAR":             "anios",
        "value":                      "miles_personas_a_mitad_anio",
    })

    df["miles_personas_a_mitad_anio"] = pd.to_numeric(
        df["miles_personas_a_mitad_anio"].astype(str).str.replace(",", "."),
        errors="coerce",
    )

    df = df.drop(columns=["Sexo", "unit", "notes_ids", "source_id"], errors="ignore")

    ref_max = df.groupby("pais", as_index=False)["anios"].max()
    df = df.merge(ref_max, on=["pais", "anios"], how="inner")

    df["pais"] = estandarizar_pais(df["pais"])

    orden_edades = [
        "0-4", "5-9", "10-14", "15-19", "20-24",
        "25-29", "30-34", "35-39", "40-44", "45-49",
        "50-54", "55-59", "60-64", "65-69", "70-74",
        "75-79", "80-84", "85-89", "90-94", "95-99",
        "100 y más",
    ]
    df["grupos_edad"] = pd.Categorical(df["grupos_edad"], categories=orden_edades, ordered=True)
    df = df.sort_values(["pais", "grupos_edad"])
    return df


def construir_datasets(df_internet, df_trabajo, df_poblacion):
    df_tiempo = df_trabajo.drop(columns=["indicador", "anios"], errors="ignore")
    df_int    = df_internet.drop(columns=["edad", "anio"], errors="ignore")

    # Intermedio con todos los indicadores (no se exporta tal cual)
    df_calc = df_tiempo.merge(df_int, on="pais", how="left")

    df_calc["carga_cuidados"] = (
        df_calc["tiempo_trabajo_no_remunerado"]
        / df_calc["tiempo_total_trabajo"].replace(0, np.nan)
    ) * 100
    df_calc["brecha_digital"] = 100 - df_calc["porcentaje_uso_internet"]
    df_calc["vulnerabilidad"] = (df_calc["carga_cuidados"] + df_calc["brecha_digital"]) / 2

    # DATASET 1: solo columnas base
    df_ti = df_calc[["pais", "tiempo_total_trabajo", "tiempo_trabajo_remunerado",
                      "tiempo_trabajo_no_remunerado", "porcentaje_uso_internet"]].copy()

    # DATASET 2: df_poblacion
    df_pob = df_poblacion.drop(columns=["indicador"], errors="ignore")

    # DATASET 3: df_riesgo — parte del intermedio, solo sus columnas
    edades_activas = [
        "15-19", "20-24", "25-29", "30-34", "35-39",
        "40-44", "45-49", "50-54", "55-59", "60-64",
    ]
    df_activa   = df_pob[df_pob["grupos_edad"].isin(edades_activas)]
    pob_total   = df_pob.groupby("pais")["miles_personas_a_mitad_anio"].sum()
    pob_activa  = df_activa.groupby("pais")["miles_personas_a_mitad_anio"].sum()
    peso_activa = (pob_activa / pob_total * 100).rename("peso_poblacional_edad_activa")

    df_riesgo = df_calc[["pais", "vulnerabilidad"]].copy()
    df_riesgo = df_riesgo.merge(peso_activa, on="pais", how="left")
    df_riesgo["riesgo_poblacional"] = (
        df_riesgo["vulnerabilidad"] * df_riesgo["peso_poblacional_edad_activa"]
    ) / 100
    df_riesgo = df_riesgo.sort_values("riesgo_poblacional", ascending=False)

    return df_ti, df_pob, df_riesgo


if __name__ == "__main__":
    print("-> Procesando fuentes…")
    df_internet  = procesar_internet()
    df_trabajo   = procesar_tiempo_trabajo()
    df_poblacion = procesar_poblacion()

    print("-> Construyendo datasets finales…")
    df_tiempo_internet, df_pob_final, df_riesgo = construir_datasets(
        df_internet, df_trabajo, df_poblacion
    )

    df_tiempo_internet.to_csv(OUTPUT_DIR + "df_tiempo_internet.csv", index=False)
    df_pob_final.to_csv(OUTPUT_DIR + "df_poblacion.csv", index=False)
    df_riesgo.to_csv(OUTPUT_DIR + "df_riesgo.csv", index=False)

    print(f"\ndf_tiempo_internet.csv  ->  {len(df_tiempo_internet)} filas, {df_tiempo_internet.shape[1]} cols")
    print(f"df_poblacion.csv        ->  {len(df_pob_final)} filas, {df_pob_final.shape[1]} cols")
    print(f"df_riesgo.csv           ->  {len(df_riesgo)} filas, {df_riesgo.shape[1]} cols")
    print("\nColumnas df_tiempo_internet:", df_tiempo_internet.columns.tolist())
    print("Columnas df_poblacion:      ", df_pob_final.columns.tolist())
    print("Columnas df_riesgo:         ", df_riesgo.columns.tolist())