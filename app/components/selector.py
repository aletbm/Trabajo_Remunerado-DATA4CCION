"""
components/selector.py
Selector de métrica + slider temporal de año (separados).
"""

import streamlit as st
from config.metric import METRICS, METRICS_REAL
from data.loader import YEARS

# Opciones del selectbox: solo métricas reales (sin separadores)
_OPTIONS = list(METRICS_REAL.keys())
# Primer índice real (saltando el separador inicial)
_DEFAULT_IDX = 0


def render_metric_selector() -> tuple[str, dict]:
    """Selectbox de métrica. Retorna (nombre, config)."""

    # Badge de dimensión según selección actual
    if "selected_metric" not in st.session_state:
        st.session_state.selected_metric = _OPTIONS[_DEFAULT_IDX]

    selected = st.selectbox(
        "MÉTRICA A VISUALIZAR",
        options=_OPTIONS,
        index=_OPTIONS.index(st.session_state.selected_metric),
        help="Seleccioná la dimensión que querés explorar en el mapa.",
        key="selected_metric",
    )

    m = METRICS_REAL[selected]

    badge_color = "#1e5fa8" if m["dimension"] == "digital" else "#7a3a9a"
    badge_label = "◈ BRECHA DIGITAL" if m["dimension"] == "digital" else "◈ BRECHA DE CUIDADOS"

    st.markdown(
        f"""
        <span style="font-family:'Space Mono',monospace;font-size:0.55rem;
           letter-spacing:2px;text-transform:uppercase;color:{badge_color};
           border:1px solid {badge_color};border-radius:2px;
           padding:0.1rem 0.4rem;margin-bottom:0.5rem;display:inline-block">
          {badge_label}
        </span>
        <p style="font-family:'Space Mono',monospace;font-size:0.65rem;
           letter-spacing:3px;text-transform:uppercase;
           color:#c8b090;margin:0.4rem 0 1rem">
          ◦ {m['desc']}
        </p>""",
        unsafe_allow_html=True,
    )
    return selected, m


def render_year_slider() -> int:
    """Slider temporal debajo del mapa. Retorna el año seleccionado."""
    st.markdown(
        """
        <p style="font-family:'Space Mono',monospace;font-size:0.62rem;
           letter-spacing:3px;text-transform:uppercase;
           color:#c8b090;margin:1.2rem 0 0.4rem">
          ◦ AÑO
        </p>""",
        unsafe_allow_html=True,
    )
    year = st.select_slider(
        "AÑO",
        options=YEARS,
        value=max(YEARS),
        label_visibility="collapsed",
    )
    return year
