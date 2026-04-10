import streamlit as st
from config.styles import CSS
from data.loader import load_data, filter_by_year
from components.header import render_header, render_kpis
from components.selector import render_metric_selector, render_year_slider
from components.map_view import render_map_section
from components.charts import render_charts_section
from components.footer import render_footer

st.set_page_config(
    page_title="Brecha Digital · Género · LATAM",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(CSS, unsafe_allow_html=True)

df_all = load_data()

render_header()

_metric_name, m = render_metric_selector()
col = m["col"]

if "year" not in st.session_state:
    st.session_state.year = max(df_all["año"].unique())

df = filter_by_year(df_all, st.session_state.year)

render_kpis(df)

render_map_section(df, col, m)

year = render_year_slider()
if year != st.session_state.year:
    st.session_state.year = year
    st.rerun()

render_charts_section(df)
render_footer()
