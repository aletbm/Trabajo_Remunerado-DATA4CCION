"""
config/metric.py
Definición de métricas del dashboard, organizadas en dos dimensiones:
  · Brecha Digital de Género
  · Brecha de Cuidados por Género
"""

METRICS = {
    # ── BRECHA DIGITAL ────────────────────────────────────────────────────
    "── Brecha Digital ──────────────────": None,  # separador visual

    "Índice de Brecha Digital (compuesto)": {
        "col": "indice_brecha_digital",
        "label": "Índice Brecha Digital",
        "unit": "pts",
        "desc": "Índice compuesto: acceso internet, salario, participación laboral y habilidades digitales",
        "higher_is_bad": True,
        "cmap": [[0, "#0a3d62"], [0.3, "#1e5fa8"], [0.6, "#d94a7a"], [1, "#ff2060"]],
        "dimension": "digital",
    },
    "Brecha de Participación Laboral (pp)": {
        "col": "brecha_participacion",
        "label": "Brecha Participación",
        "unit": "pp",
        "desc": "Diferencia en puntos porcentuales entre tasa de participación laboral masculina y femenina",
        "higher_is_bad": True,
        "cmap": [[0, "#0a3d62"], [0.4, "#1e5fa8"], [0.7, "#d97a4a"], [1, "#ff8c00"]],
        "dimension": "digital",
    },
    "Brecha Salarial de Género (%)": {
        "col": "brecha_salarial",
        "label": "Brecha Salarial",
        "unit": "%",
        "desc": "Porcentaje adicional que ganan los hombres vs mujeres en trabajo remunerado equivalente",
        "higher_is_bad": True,
        "cmap": [[0, "#0a3d62"], [0.4, "#1e5fa8"], [0.7, "#d94a7a"], [1, "#ff2060"]],
        "dimension": "digital",
    },
    "Mujeres en Sector TIC (%)": {
        "col": "mujeres_tic",
        "label": "Mujeres en TIC",
        "unit": "%",
        "desc": "Porcentaje de mujeres ocupadas en el sector digital y de tecnologías de la información",
        "higher_is_bad": False,
        "cmap": [[0, "#6e1a3a"], [0.3, "#1a3a6e"], [0.7, "#1e5fa8"], [1, "#4ad98a"]],
        "dimension": "digital",
    },
    "Ratio Acceso Internet M/H": {
        "col": "ratio_internet",
        "label": "Paridad Internet",
        "unit": "ratio",
        "desc": "Proporción de acceso a internet de mujeres respecto a hombres (1.0 = paridad total)",
        "higher_is_bad": False,
        "cmap": [[0, "#6e1a1a"], [0.4, "#1a3a6e"], [0.8, "#1e5fa8"], [1, "#4ad98a"]],
        "dimension": "digital",
    },
    "Habilidades Digitales Femeninas (0–100)": {
        "col": "habilidades_dig",
        "label": "Habilidades Digitales",
        "unit": "/100",
        "desc": "Índice de habilidades digitales de la fuerza laboral femenina: uso de software, internet y herramientas digitales",
        "higher_is_bad": False,
        "cmap": [[0, "#6e1a1a"], [0.4, "#1a3a6e"], [0.7, "#1e5fa8"], [1, "#4ad98a"]],
        "dimension": "digital",
    },
    "Informalidad Digital Femenina (%)": {
        "col": "informalidad_dig",
        "label": "Informalidad Digital",
        "unit": "%",
        "desc": "Porcentaje de mujeres en empleo digital informal (plataformas, gig economy sin protección social)",
        "higher_is_bad": True,
        "cmap": [[0, "#0a3d62"], [0.4, "#1e5fa8"], [0.7, "#d97a4a"], [1, "#ff2060"]],
        "dimension": "digital",
    },

    # ── BRECHA DE CUIDADOS ────────────────────────────────────────────────
    "── Brecha de Cuidados ──────────────": None,  # separador visual

    "Índice de Brecha de Cuidados (compuesto)": {
        "col": "indice_brecha_cuidados",
        "label": "Índice Brecha Cuidados",
        "unit": "pts",
        "desc": "Índice compuesto: horas de cuidado, doble jornada, licencia parental y trabajo doméstico remunerado",
        "higher_is_bad": True,
        "cmap": [[0, "#0a3d62"], [0.3, "#1e5fa8"], [0.6, "#d94a7a"], [1, "#ff2060"]],
        "dimension": "cuidados",
    },
    "Brecha de Horas de Cuidados No Remunerados (h/sem)": {
        "col": "brecha_cuidados_hrs",
        "label": "Brecha Horas Cuidados",
        "unit": "h/sem",
        "desc": "Diferencia semanal en horas de trabajo de cuidados no remunerado entre mujeres y hombres",
        "higher_is_bad": True,
        "cmap": [[0, "#0a3d62"], [0.4, "#1e5fa8"], [0.7, "#d97a4a"], [1, "#ff8c00"]],
        "dimension": "cuidados",
    },
    "Mujeres con Doble Jornada (%)": {
        "col": "doble_jornada",
        "label": "Doble Jornada",
        "unit": "%",
        "desc": "Porcentaje de mujeres que combinan trabajo remunerado con más de 4 horas diarias de cuidados no remunerados",
        "higher_is_bad": True,
        "cmap": [[0, "#0a3d62"], [0.4, "#1e5fa8"], [0.7, "#d94a7a"], [1, "#ff2060"]],
        "dimension": "cuidados",
    },
    "Licencia Parental Remunerada Efectiva (semanas)": {
        "col": "licencia_parental",
        "label": "Licencia Parental",
        "unit": "sem",
        "desc": "Promedio de semanas de licencia parental remunerada efectivamente disponible (madres + padres combinado)",
        "higher_is_bad": False,
        "cmap": [[0, "#6e1a3a"], [0.3, "#1a3a6e"], [0.7, "#1e5fa8"], [1, "#4ad98a"]],
        "dimension": "cuidados",
    },
    "Mujeres en Trabajo Doméstico Remunerado (%)": {
        "col": "trab_dom_muj",
        "label": "Trabajo Doméstico Rem.",
        "unit": "%",
        "desc": "Porcentaje de mujeres sobre el total de trabajadoras/es domésticos remunerados",
        "higher_is_bad": True,
        "cmap": [[0, "#0a3d62"], [0.4, "#1e5fa8"], [0.7, "#d94a7a"], [1, "#ff2060"]],
        "dimension": "cuidados",
    },
}

# Solo métricas reales (sin separadores)
METRICS_REAL = {k: v for k, v in METRICS.items() if v is not None}
