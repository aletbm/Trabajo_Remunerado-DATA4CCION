METRICS = {
    "Carga de Cuidados (%)": {
        "col": "carga_cuidados",
        "label": "Carga de Cuidados",
        "unit": "%",
        "desc": "Tiempo de trabajo no remunerado sobre el tiempo total de trabajo · Mayor valor = mayor carga",
        "higher_is_bad": True,
        "cmap": [[0, "#0a3d62"], [0.3, "#1e5fa8"], [0.6, "#d94a7a"], [1, "#ff2060"]],
        "dimension": "cuidados",
    },
    "Brecha Digital (%)": {
        "col": "brecha_digital",
        "label": "Brecha Digital",
        "unit": "%",
        "desc": "100 menos el porcentaje de uso de internet · Mayor valor = menor acceso digital",
        "higher_is_bad": True,
        "cmap": [[0, "#0a3d62"], [0.3, "#1e5fa8"], [0.6, "#d94a7a"], [1, "#ff2060"]],
        "dimension": "digital",
    },
    "Vulnerabilidad Estructural (%)": {
        "col": "vulnerabilidad_estructural",
        "label": "Vulnerabilidad Estructural",
        "unit": "%",
        "desc": "Promedio de carga de cuidados y brecha digital · Identifica los contextos más críticos por país",
        "higher_is_bad": True,
        "cmap": [[0, "#0a3d62"], [0.3, "#1e5fa8"], [0.6, "#d94a7a"], [1, "#ff2060"]],
        "dimension": "combinado",
    },
    "Peso Poblacional Edad Activa (%)": {
        "col": "peso_poblacional",
        "label": "Peso Poblacional",
        "unit": "%",
        "desc": "Proporción de mujeres en edad activa (15–64) sobre el total de mujeres del país",
        "higher_is_bad": True,
        "cmap": [[0, "#0a3d62"], [0.3, "#1e5fa8"], [0.6, "#d94a7a"], [1, "#ff2060"]],
        "dimension": "poblacional",
    },
    "Riesgo Poblacional (%)": {
        "col": "riesgo_poblacional",
        "label": "Riesgo Poblacional",
        "unit": "%",
        "desc": "Vulnerabilidad estructural ponderada por la proporción de mujeres en edad activa · Reescalado a 0–100",
        "higher_is_bad": True,
        "cmap": [[0, "#0a3d62"], [0.3, "#1e5fa8"], [0.6, "#d94a7a"], [1, "#ff2060"]],
        "dimension": "combinado",
    },
}

METRICS_REAL = METRICS  # todas son reales, sin separadores
