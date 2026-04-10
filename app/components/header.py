import streamlit as st
import pandas as pd
import os


def render_header() -> None:
    col_t, col_tag = st.columns([3, 1])

    with col_t:
        logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "images", "onumujereslogo.png")
        st.image(logo_path, width=100)
        st.markdown(
            '<p class="hero-sub">◈ Observatorio de Género LATAM</p>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<h1 class="hero-title">Brechas de Género<br>Digital y de Cuidados</h1>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p class="hero-desc">'
            "Visualización de indicadores de inequidad digital y de cuidados "
            "en el empleo remunerado para 34 países de América Latina y el Caribe. "
            "<br><br>"
            "Datos: CEPAL · OIT · ITU · BID · 2018–2023"
            "</p>",
            unsafe_allow_html=True,
        )

    with col_tag:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="text-align:right">
              <span class="info-tag">20 países</span>&nbsp;
              <span class="info-tag">7 métricas</span><br><br>
              <span class="info-tag" style="color:#d94a7a;border-color:#6e1a3a">
                brecha activa
              </span>
            </div>""",
            unsafe_allow_html=True,
        )

    st.markdown('<hr class="hz-line">', unsafe_allow_html=True)


def render_kpis(df: pd.DataFrame) -> None:
    avg_gap      = (df["part_masc"] - df["part_fem"]).mean()
    avg_salary   = df["brecha_salarial"].mean()
    avg_internet = df["ratio_internet"].mean()
    avg_tic      = df["mujeres_tic"].mean()

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(
            f"""
            <div class="metric-card">
              <div class="metric-label">Brecha Promedio Participación</div>
              <div class="metric-value">{avg_gap:.1f}
                <span style="font-size:1rem;color:#4a72a0"> pp</span>
              </div>
              <div class="metric-delta neg">▲ hombres vs mujeres</div>
            </div>""",
            unsafe_allow_html=True,
        )

    with k2:
        st.markdown(
            f"""
            <div class="metric-card accent">
              <div class="metric-label">Brecha Salarial Promedio</div>
              <div class="metric-value">{avg_salary:.1f}
                <span style="font-size:1rem;color:#4a72a0"> %</span>
              </div>
              <div class="metric-delta neg">▲ hombres ganan más</div>
            </div>""",
            unsafe_allow_html=True,
        )

    with k3:
        st.markdown(
            f"""
            <div class="metric-card">
              <div class="metric-label">Ratio Internet M/H (prom.)</div>
              <div class="metric-value">{avg_internet:.2f}
                <span style="font-size:1rem;color:#4a72a0"> ratio</span>
              </div>
              <div class="metric-delta">objetivo: 1.00</div>
            </div>""",
            unsafe_allow_html=True,
        )

    with k4:
        st.markdown(
            f"""
            <div class="metric-card green">
              <div class="metric-label">Mujeres en TIC (prom.)</div>
              <div class="metric-value">{avg_tic:.1f}
                <span style="font-size:1rem;color:#4a72a0"> %</span>
              </div>
              <div class="metric-delta neg">▼ muy por debajo de paridad</div>
            </div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)