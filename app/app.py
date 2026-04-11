"""
app.py
Punto de entrada del dashboard.
Ejecutar con:  streamlit run app.py
"""

import streamlit as st
from config.styles import CSS
from data.loader import load_indicadores, load_poblacion
from components.header import render_header, render_kpis
from components.selector import render_metric_selector
from components.map_view import render_map_section
from components.charts import render_charts_section
from components.footer import render_footer

st.set_page_config(
    page_title="Brecha Digital · Carga de Cuidados · Género · LATAM",
    page_icon="♀️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(CSS, unsafe_allow_html=True)

df          = load_indicadores()
df_pob      = load_poblacion()

render_header()

_metric_name, m = render_metric_selector()
col = m["col"]

render_kpis(df)
render_map_section(df, col, m, df_pob)
render_charts_section(df)
render_footer()
