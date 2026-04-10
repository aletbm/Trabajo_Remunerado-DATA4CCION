import streamlit as st
import plotly.graph_objects as go
import pandas as pd

_PLOT_BG  = "#070d1a"
_PAPER_BG = "#050810"
_GRID     = "#0f1e35"
_FONT_FAM = "Saira Stencil"
_AXIS_COL = "#3a6090"


def _scatter_fig(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["part_fem"],
            y=df["brecha_salarial"],
            mode="markers+text",
            marker=dict(
                size=df["habilidades_dig"] / 4,
                color=df["indice_brecha_digital"],
                colorscale=[[0, "#0a3d62"], [0.3, "#1e5fa8"], [0.65, "#d94a7a"], [1, "#ff2060"]],
                showscale=True,
                colorbar=dict(
                    title=dict(
                        text="Índice<br>Brecha",
                        font=dict(family=_FONT_FAM, size=8, color="#4a72a0"),
                    ),
                    tickfont=dict(family=_FONT_FAM, size=8, color="#4a72a0"),
                    bgcolor="#070d1a",
                    bordercolor="#1a2d50",
                    borderwidth=1,
                    thickness=8,
                    len=0.8,
                ),
                line=dict(color=_PAPER_BG, width=1),
                opacity=0.9,
            ),
            text=df["ISO"],
            textfont=dict(family=_FONT_FAM, size=8, color="#7a94b8"),
            textposition="top center",
            hovertemplate=(
                "<b>%{customdata}</b><br>"
                "Part. Fem: %{x:.1f}%<br>"
                "Brecha Sal: %{y:.1f}%<extra></extra>"
            ),
            customdata=df["País"],
        )
    )

    fig.update_layout(
        paper_bgcolor=_PAPER_BG,
        plot_bgcolor=_PLOT_BG,
        margin=dict(l=40, r=20, t=30, b=40),
        height=320,
        xaxis=dict(
            title=dict(
                text="Participación laboral femenina (%)",
                font=dict(family=_FONT_FAM, size=9, color=_AXIS_COL),
            ),
            tickfont=dict(family=_FONT_FAM, size=8, color=_AXIS_COL),
            gridcolor=_GRID,
            gridwidth=1,
            zeroline=False,
        ),
        yaxis=dict(
            title=dict(
                text="Brecha salarial (%)",
                font=dict(family=_FONT_FAM, size=9, color=_AXIS_COL),
            ),
            tickfont=dict(family=_FONT_FAM, size=8, color=_AXIS_COL),
            gridcolor=_GRID,
            gridwidth=1,
            zeroline=False,
        ),
        font=dict(family="Saira Condensed", color="#c8d6e8"),
        showlegend=False,
        title=dict(
            text=(
                "<span style='font-size:9px;letter-spacing:2px'>"
                "PART. FEMENINA vs BRECHA SALARIAL · tamaño = habilidades digitales"
                "</span>"
            ),
            font=dict(family=_FONT_FAM, size=9, color=_AXIS_COL),
            x=0.5,
        ),
    )
    return fig


def _bar_fig(df: pd.DataFrame) -> go.Figure:
    bar_df = df.sort_values("mujeres_tic")
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=bar_df["mujeres_tic"],
            y=bar_df["País"],
            orientation="h",
            marker=dict(
                color=bar_df["mujeres_tic"],
                colorscale=[[0, "#0a3d62"], [0.35, "#1e5fa8"], [0.7, "#d94a7a"], [1, "#ff2060"]],
                line=dict(width=0),
            ),
            hovertemplate="<b>%{y}</b>: %{x:.1f}%<extra></extra>",
        )
    )

    fig.add_vline(
        x=50,
        line_dash="dot",
        line_color="#d94a7a",
        line_width=1,
        annotation_text=(
            "<span style='font-family:Space Mono;font-size:8px'>50% PARIDAD</span>"
        ),
        annotation_font_color="#d94a7a",
        annotation_position="top right",
    )

    fig.update_layout(
        paper_bgcolor=_PAPER_BG,
        plot_bgcolor=_PLOT_BG,
        margin=dict(l=10, r=40, t=30, b=30),
        height=320,
        xaxis=dict(
            title=dict(
                text="% mujeres en sector TIC",
                font=dict(family=_FONT_FAM, size=9, color=_AXIS_COL),
            ),
            tickfont=dict(family=_FONT_FAM, size=8, color=_AXIS_COL),
            gridcolor=_GRID,
            gridwidth=1,
            range=[0, 55],
        ),
        yaxis=dict(
            tickfont=dict(family=_FONT_FAM, size=8, color="#6090c0"),
        ),
        font=dict(family="Saira Condensed", color="#c8d6e8"),
        title=dict(
            text=(
                "<span style='font-size:9px;letter-spacing:2px'>"
                "MUJERES EN EMPLEO DIGITAL (TIC)"
                "</span>"
            ),
            font=dict(family=_FONT_FAM, size=9, color=_AXIS_COL),
            x=0.5,
        ),
        bargap=0.3,
    )
    return fig


def render_charts_section(df: pd.DataFrame) -> None:
    st.markdown('<hr class="hz-line">', unsafe_allow_html=True)
    st.markdown(
        """
        <p class="hero-sub">◈ Análisis de correlación</p>
        <h3 style="font-family:'Saira Condensed',sans-serif;font-weight:700;
            font-size:1.3rem;color:#d0e4ff;margin:0 0 0.3rem">
          Participación Laboral vs Brecha Salarial
        </h3>""",
        unsafe_allow_html=True,
    )

    sc1, sc2 = st.columns(2, gap="large")

    with sc1:
        st.plotly_chart(
            _scatter_fig(df),
            width='stretch',
            config={"displayModeBar": False},
        )

    with sc2:
        st.plotly_chart(
            _bar_fig(df),
            width='stretch',
            config={"displayModeBar": False},
        )