import streamlit as st
import pandas as pd
import os


def render_header() -> None:
    col_t, col_tag = st.columns([3, 1])

    with col_t:
        logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "images", "dat4ccion_logos.png")
        st.image(logo_path, width=500)
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
            "en el empleo remunerado para 9 países de América Latina y el Caribe. "
            "<br><br>"
            "Datos: CEPAL · WB · 2025"
            "</p>",
            unsafe_allow_html=True,
        )

    with col_tag:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="text-align:right">
              <span class="info-tag">9 países</span>&nbsp;
              <span class="info-tag">5 métricas</span><br><br>
              <span class="info-tag" style="color:#d94a7a;border-color:#6e1a3a">
                brecha activa
              </span>
            </div>""",
            unsafe_allow_html=True,
        )

    st.markdown('<hr class="hz-line">', unsafe_allow_html=True)


def render_kpis(df: pd.DataFrame) -> None:
    avg_cuidados   = df["carga_cuidados"].mean()
    avg_digital    = df["brecha_digital"].mean()
    avg_vuln       = df["vulnerabilidad_estructural"].mean()
    avg_riesgo     = df["riesgo_poblacional"].mean()

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(
            f"""
            <div class="metric-card">
              <div class="metric-label">Carga de Cuidados (prom.)</div>
              <div class="metric-value">{avg_cuidados:.1f}
                <span style="font-size:1rem;color:#4a72a0"> %</span>
              </div>
              <div class="metric-delta neg">▲ tiempo no remunerado</div>
            </div>""",
            unsafe_allow_html=True,
        )

    with k2:
        st.markdown(
            f"""
            <div class="metric-card accent">
              <div class="metric-label">Brecha Digital (prom.)</div>
              <div class="metric-value">{avg_digital:.1f}
                <span style="font-size:1rem;color:#4a72a0"> %</span>
              </div>
              <div class="metric-delta neg">▲ sin acceso a internet</div>
            </div>""",
            unsafe_allow_html=True,
        )

    with k3:
        st.markdown(
            f"""
            <div class="metric-card accent">
              <div class="metric-label">Vulnerabilidad Estructural (prom.)</div>
              <div class="metric-value">{avg_vuln:.1f}
                <span style="font-size:1rem;color:#4a72a0"> %</span>
              </div>
              <div class="metric-delta neg">▲ índice combinado</div>
            </div>""",
            unsafe_allow_html=True,
        )

    with k4:
        st.markdown(
            f"""
            <div class="metric-card">
              <div class="metric-label">Riesgo Poblacional (prom.)</div>
              <div class="metric-value">{avg_riesgo:.1f}
                <span style="font-size:1rem;color:#4a72a0"> %</span>
              </div>
              <div class="metric-delta neg">▼ vulnerabilidad ponderada</div>
            </div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
