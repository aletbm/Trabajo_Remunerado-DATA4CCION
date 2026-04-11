import streamlit as st


def render_footer() -> None:
    st.markdown('<hr class="hz-line">', unsafe_allow_html=True)

    left, center, right = st.columns([2, 3, 1])

    with left:
        st.markdown(
            """
            <div style="display:flex;align-items:center;gap:0.4rem;height:100%">
              <span class="info-tag">CEPAL</span>
              <span class="info-tag">WB</span>
            </div>""",
            unsafe_allow_html=True,
        )

    with center:
        st.markdown(
            """
            <p style="font-family:'Space Mono',monospace;font-size:0.6rem;
               letter-spacing:0.12em;text-transform:uppercase;
               color:#2a4060;margin:0;text-align:center">
              Datos estimados 2025 · Visualización explorativa
            </p>""",
            unsafe_allow_html=True,
        )

    with right:
      with st.popover("✉ Contacto", use_container_width=True):
          st.link_button("🔗 María Agustina Cuello", "https://www.linkedin.com/in/maria-agustina-cuello/", use_container_width=True)
          st.link_button("🔗 Camila Bozzoletti", "https://www.linkedin.com/in/camilabozzoletti/", use_container_width=True)
          st.link_button("🔗 Alexander Daniel Rios", "https://www.linkedin.com/in/alexander-daniel-rios/", use_container_width=True)