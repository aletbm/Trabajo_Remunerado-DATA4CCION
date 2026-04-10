import json
import os
import streamlit as st
import plotly.graph_objects as go
import pandas as pd


_GEOJSON_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "latam.geojson")

with open(_GEOJSON_PATH, encoding="utf-8") as _f:
    _LATAM_GEOJSON = json.load(_f)

# ── Construcción del mapa ──────────────────────────────────────────────────────

def _build_choropleth(df: pd.DataFrame, col: str, m: dict, mapbox_token: str = "") -> go.Figure:
    """
    Choropleth sobre GeoJSON de LATAM.
    - featureidkey="properties.iso"  ->  une con df["ISO"]
    - mapbox style "outdoors"        ->  relieve real con colores de altitud
                                         (verdes->marrones->blancos), curvas de nivel,
                                         rios y nombres geograficos. Requiere token.
    - Fallback a "stamen-terrain"    ->  si no hay token (sin API key, gratis).

    TOKEN: Obtene uno gratis en https://account.mapbox.com -> Access tokens.
    Agregalo en .streamlit/secrets.toml como:
        MAPBOX_TOKEN = "pk.eyJ1IjoiLi4uIn0..."
    o como variable de entorno MAPBOX_TOKEN.
    """
    import os

    token = mapbox_token or st.secrets.get("MAPBOX_TOKEN", "") or os.getenv("MAPBOX_TOKEN", "")

    map_style = "mapbox://styles/mapbox/satellite-streets-v12" if token else "stamen-terrain"

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
                title=dict(
                    text=m["unit"],
                    font=dict(family="Space Mono", size=10, color="#2a1a00"),
                ),
                tickfont=dict(family="Space Mono", size=9, color="#2a1a00"),
                bgcolor="rgba(255,252,240,0.88)",
                bordercolor="#c8a87a",
                borderwidth=1,
                thickness=10,
                len=0.55,
                x=0.01,
                xanchor="left",
                yanchor="middle",
                y=0.5,
            ),
            text=df["País"],
            hovertemplate=(
                "<b>%{text}</b><br>"
                f"{m['label']}: %{{z:.2f}} {m['unit']}"
                "<extra></extra>"
            ),
        )
    )

    layout_mapbox = dict(
        style=map_style,
        center=dict(lat=-15, lon=-65),
        zoom=1.1,
        bounds=dict(
            west=-180,
            east=0,
            south=-60,
            north=35,
        ),
        
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
            x=0.5,
            xanchor="center",
        ),
        dragmode="pan",
    )
    return fig


# ── Ranking lateral ────────────────────────────────────────────────────────────

def _render_ranking(df: pd.DataFrame, col: str, m: dict) -> None:
    st.markdown(
        '<div style="margin-bottom:1rem"><span class="info-tag">RANKING PAÍSES</span></div>',
        unsafe_allow_html=True,
    )

    sorted_df = (
        df.sort_values(col, ascending=not m["higher_is_bad"])
        .reset_index(drop=True)
    )
    vmin = df[col].min()
    vmax = df[col].max()

    for i, row in sorted_df.iterrows():
        val = row[col]
        pct = (val - vmin) / (vmax - vmin) if vmax != vmin else 0.5

        if m["higher_is_bad"]:
            if pct < 0.35:
                r = int(10 + pct/0.35 * (30 - 10))
                g = int(61 + pct/0.35 * (95 - 61))
                b = int(98 + pct/0.35 * (168 - 98))
            elif pct < 0.65:
                t = (pct - 0.35) / 0.30
                r = int(30 + t * (217 - 30))
                g = int(95 + t * (74 - 95))
                b = int(168 + t * (122 - 168))
            else:
                t = (pct - 0.65) / 0.35
                r = int(217 + t * (255 - 217))
                g = int(74 + t * (32 - 74))
                b = int(122 + t * (96 - 122))
            bar_color = f"rgb({r},{g},{b})"
        else:
            t = 1 - pct
            if t < 0.35:
                r = int(10 + t/0.35 * (30 - 10))
                g = int(61 + t/0.35 * (95 - 61))
                b = int(98 + t/0.35 * (168 - 98))
            elif t < 0.65:
                s = (t - 0.35) / 0.30
                r = int(30 + s * (217 - 30))
                g = int(95 + s * (74 - 95))
                b = int(168 + s * (122 - 168))
            else:
                s = (t - 0.65) / 0.35
                r = int(217 + s * (255 - 217))
                g = int(74 + s * (32 - 74))
                b = int(122 + s * (96 - 122))
            bar_color = f"rgb({r},{g},{b})"

        st.markdown(
            f"""
            <div class="country-row">
              <span style="font-family:'Space Mono',monospace;font-size:0.58rem;
                    color:#2a4060;min-width:24px">#{i+1}</span>
              <span class="country-name" style="min-width:80px;font-size:0.75rem">
                {row['País'][:12]}
              </span>
              <div class="bar-wrap">
                <div class="bar-fill"
                     style="width:{pct*100:.0f}%;background:{bar_color}">
                </div>
              </div>
              <span style="font-family:'Space Mono',monospace;font-size:0.65rem;
                    color:#6090c0;min-width:38px;text-align:right">
                {val:.1f}
              </span>
            </div>""",
            unsafe_allow_html=True,
        )


# ── Render público ─────────────────────────────────────────────────────────────

def render_map_section(df: pd.DataFrame, col: str, m: dict) -> None:
    map_col, rank_col = st.columns([3, 1], gap="large")

    with map_col:
        import os
        token = st.secrets.get("MAPBOX_TOKEN", "") or os.getenv("MAPBOX_TOKEN", "")
        fig = _build_choropleth(df, col, m, mapbox_token=token)
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