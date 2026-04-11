import streamlit as st
from config.metric import METRICS_REAL

_OPTIONS = list(METRICS_REAL.keys())

_BADGE = {
    "cuidados":    ("#d97a4a", "◈ CARGA DE CUIDADOS"),
    "digital":     ("#1e5fa8", "◈ BRECHA DIGITAL"),
    "combinado":   ("#d94a7a", "◈ ÍNDICE COMBINADO"),
    "poblacional": ("#4ad98a", "◈ PESO POBLACIONAL"),
}


def render_metric_selector() -> tuple[str, dict]:
    """Selectbox de métrica. Retorna (nombre, config)."""
    selected = st.selectbox(
        "MÉTRICA A VISUALIZAR",
        options=_OPTIONS,
        index=0,
        help="Seleccioná el indicador que querés explorar en el mapa.",
    )
    m = METRICS_REAL[selected]
    color, label = _BADGE.get(m["dimension"], ("#4a72a0", "◈ INDICADOR"))
    st.markdown(
        f"""
        <span style="font-family:'Space Mono',monospace;font-size:0.55rem;
           letter-spacing:2px;text-transform:uppercase;color:{color};
           border:1px solid {color};border-radius:2px;
           padding:0.1rem 0.4rem;margin-bottom:0.5rem;display:inline-block">
          {label}
        </span>
        <p style="font-family:'Space Mono',monospace;font-size:0.65rem;
           letter-spacing:3px;text-transform:uppercase;
           color:#c8b090;margin:0.4rem 0 1rem">
          ◦ {m['desc']}
        </p>""",
        unsafe_allow_html=True,
    )
    return selected, m
