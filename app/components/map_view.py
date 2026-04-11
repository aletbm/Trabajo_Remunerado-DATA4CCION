import json
import os
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

_GEOJSON_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "latam.geojson")

with open(_GEOJSON_PATH, encoding="utf-8") as _f:
    _LATAM_GEOJSON = json.load(_f)

from data.loader import ISO_MAP, EDAD_ACTIVA

# Mapeo inverso ISO -> nombre en mayúsculas (como está en df_poblacion)
_ISO_INV = {v: k for k, v in ISO_MAP.items()}


def _build_choropleth(
    df: pd.DataFrame,
    col: str,
    m: dict,
    df_pob: pd.DataFrame,
    mapbox_token: str = "",
) -> go.Figure:

    token = mapbox_token or st.secrets.get("MAPBOX_TOKEN", "") or os.getenv("MAPBOX_TOKEN", "")
    map_style = "mapbox://styles/mapbox/satellite-streets-v12" if token else "stamen-terrain"

    # Ranking posicional
    ascending = not m["higher_is_bad"]
    rank = df[col].rank(ascending=ascending, method="min").astype(int)

    # Total mujeres por país desde df_pob
    pob_total = (
        df_pob.groupby("pais")["miles_personas_a_mitad_anio"].sum()
        .reset_index()
        .rename(columns={"pais": "PAIS_UP", "miles_personas_a_mitad_anio": "total_miles"})
    )
    # Unir por ISO → nombre en mayúsculas
    df_merged = df.copy()
    df_merged["PAIS_UP"] = df_merged["ISO"].map(_ISO_INV)
    df_merged = df_merged.merge(pob_total, on="PAIS_UP", how="left")
    df_merged["rank"] = rank.values

    customdata = df_merged[
        ["carga_cuidados", "brecha_digital", "rank", "total_miles"]
    ].values

    n = len(df)

    fig = go.Figure(
        go.Choroplethmapbox(
            geojson=_LATAM_GEOJSON,
            locations=df["ISO"],
            featureidkey="properties.iso",
            z=df[col],
            colorscale=m["cmap"],
            zmin=df[col].min(),
            zmax=df[col].max(),
            marker=dict(
                line=dict(color="#FFFFFF", width=0.2),
                opacity=0.75,
            ),
            colorbar=dict(
                title=dict(text=m["unit"], font=dict(family="Space Mono", size=10, color="#2a1a00")),
                tickfont=dict(family="Space Mono", size=9, color="#2a1a00"),
                bgcolor="rgba(255,252,240,0.88)",
                bordercolor="#c8a87a", borderwidth=1,
                thickness=10, len=0.55,
                x=0.01, xanchor="left", yanchor="middle", y=0.5,
            ),
            text=df["País"],
            customdata=customdata,
            hovertemplate=(
                "<b>%{text}</b><br>"
                "──────────────────────<br>"
                f"<b>{m['label']}:</b> %{{z:.1f}} {m['unit']}   #%{{customdata[2]}} de {n}<br>"
                "<br>"
                "<b>Carga de cuidados:</b>  %{customdata[0]:.1f}%<br>"
                "<b>Brecha digital:</b>      %{customdata[1]:.1f}%<br>"
                "<br>"
                "<b>Total mujeres:</b>       %{customdata[3]:.0f}k"
                "<extra></extra>"
            ),
        )
    )

    layout_mapbox = dict(
        style=map_style,
        center=dict(lat=-15, lon=-65),
        zoom=1.1,
        bounds=dict(west=-180, east=0, south=-60, north=35),
    )
    if token:
        layout_mapbox["accesstoken"] = token

    fig.update_layout(
        mapbox=layout_mapbox,
        paper_bgcolor="#050810",
        margin=dict(l=0, r=0, t=36, b=0),
        height=620,
        font=dict(family="Saira Stencil", color="#c8d6e8"),
        title=dict(
            text=(
                f"<span style='font-size:11px;letter-spacing:3px;"
                f"text-transform:uppercase'>{m['label'].upper()}</span>"
            ),
            font=dict(family="Space Mono", size=11, color="#c8b090"),
            x=0.5, xanchor="center",
        ),
        dragmode="pan",
    )
    return fig


def _bar_color(pct: float, higher_is_bad: bool) -> str:
    t = pct if higher_is_bad else 1 - pct
    if t < 0.35:
        r = int(10 + t/0.35*20); g = int(61 + t/0.35*34); b = int(98 + t/0.35*70)
    elif t < 0.65:
        s = (t-0.35)/0.30; r = int(30+s*187); g = int(95-s*21); b = int(168-s*46)
    else:
        s = (t-0.65)/0.35; r = int(217+s*38); g = int(74-s*42); b = int(122-s*26)
    return f"rgb({r},{g},{b})"


def _render_ranking(df: pd.DataFrame, col: str, m: dict) -> None:
    st.markdown(
        '<div style="margin-bottom:1rem"><span class="info-tag">RANKING PAÍSES</span></div>',
        unsafe_allow_html=True,
    )

    sorted_df = df.sort_values(col, ascending=not m["higher_is_bad"]).reset_index(drop=True)
    vmin, vmax = df[col].min(), df[col].max()

    for i, row in sorted_df.iterrows():
        val = row[col]
        pct = (val - vmin) / (vmax - vmin) if vmax != vmin else 0.5
        color = _bar_color(pct, m["higher_is_bad"])
        st.markdown(
            f"""
            <div class="country-row">
              <span style="font-family:'Space Mono',monospace;font-size:0.58rem;
                    color:#2a4060;min-width:24px">#{i+1}</span>
              <span class="country-name" style="min-width:80px;font-size:0.75rem">
                {row['País'][:14].title()}
              </span>
              <div class="bar-wrap">
                <div class="bar-fill" style="width:{pct*100:.0f}%;background:{color}"></div>
              </div>
              <span style="font-family:'Space Mono',monospace;font-size:0.65rem;
                    color:#6090c0;min-width:38px;text-align:right">
                {val:.1f}
              </span>
            </div>""",
            unsafe_allow_html=True,
        )


def _render_poblacion(df_pob: pd.DataFrame) -> None:
    st.markdown(
        '<div style="margin-bottom:1rem">'
        '<span class="info-tag">POBLACIÓN FEMENINA %</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    pob_total = (
        df_pob.groupby("pais")["miles_personas_a_mitad_anio"].sum()
        .reset_index()
        .rename(columns={"miles_personas_a_mitad_anio": "total"})
    )
    grand_total = pob_total["total"].sum()
    pob_total["pct"] = (pob_total["total"] / grand_total * 100).round(1)
    pob_total = pob_total.sort_values("pct", ascending=True)
    pob_total["label"] = pob_total["total"].apply(
        lambda x: f"{x/1000:.1f}M" if x >= 1000 else f"{x:.0f}k"
    )
    pob_total["nombre"] = pob_total["pais"].str.title()

    fig = go.Figure(go.Bar(
        x=pob_total["pct"],
        y=pob_total["nombre"],
        orientation="h",
        text=pob_total.apply(lambda r: f"{r['pct']:.1f}% · {r['label']}", axis=1),
        textposition="inside",
        textfont=dict(size=9, color="white"),
        insidetextanchor="end",
        marker=dict(
            color=pob_total["pct"],
            colorscale=[[0, "#1e5fa8"], [1, "#d94a7a"]],
            showscale=False,
        ),
        hovertemplate="%{y}: %{x:.1f}%<extra></extra>",
    ))

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),  # menos espacio derecho
        xaxis=dict(visible=False),
        yaxis=dict(tickfont=dict(size=9, color="#7a94b8"),),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=200,
    )
    st.plotly_chart(fig, width='stretch')


def render_map_section(df: pd.DataFrame, col: str, m: dict, df_pob: pd.DataFrame) -> None:
    map_col, rank_col = st.columns([3, 1], gap="large")

    with map_col:
        token = st.secrets.get("MAPBOX_TOKEN", "") or os.getenv("MAPBOX_TOKEN", "")
        fig = _build_choropleth(df, col, m, df_pob, mapbox_token=token)
        st.plotly_chart(
            fig,
            width='stretch',
            config={
                "displayModeBar": True,
                "modeBarButtonsToRemove": [
                    "select2d", "lasso2d", "toImage",
                    "resetScale2d", "hoverClosestCartesian",
                ],
                "displaylogo": False,
                "scrollZoom": True,
            },
        )

    with rank_col:
        _render_ranking(df, col, m)
        _render_poblacion(df_pob)