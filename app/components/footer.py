import streamlit as st


def render_footer() -> None:
    st.markdown('<hr class="hz-line">', unsafe_allow_html=True)
    st.markdown(
        """
        <div style="display:flex;justify-content:space-between;
                    align-items:center;flex-wrap:wrap;gap:0.5rem">
          <div>
            <span class="info-tag">CEPAL</span>&nbsp;
            <span class="info-tag">OIT · ILOSTAT</span>&nbsp;
            <span class="info-tag">ITU</span>&nbsp;
            <span class="info-tag">BID</span>&nbsp;
            <span class="info-tag">Banco Mundial</span>
          </div>
          <p style="font-family:'Space Mono',monospace;font-size:0.6rem;
             letter-spacing:0.12em;text-transform:uppercase;color:#2a4060;margin:0">
            Datos estimados 2022–2023 · Visualización explorativa
          </p>
        </div>""",
        unsafe_allow_html=True,
    )