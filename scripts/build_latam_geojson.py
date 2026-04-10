"""
build_latam_geojson.py
Genera data/latam.geojson con TODOS los países de América Latina y el Caribe
a partir del GeoJSON de Natural Earth (ne_50m_admin_0_countries).

Ejecutar una sola vez:
    python build_latam_geojson.py

Requiere: requests (pip install requests)
"""

import json
import os

# ── Todos los países de LATAM con sus códigos ISO A3 ──────────────────────────
# América Central + México
CENTRAL = {
    "MEX": "México",
    "GTM": "Guatemala",
    "BLZ": "Belice",
    "HND": "Honduras",
    "SLV": "El Salvador",
    "NIC": "Nicaragua",
    "CRI": "Costa Rica",
    "PAN": "Panamá",
}

# El Caribe (países independientes)
CARIBE = {
    "CUB": "Cuba",
    "JAM": "Jamaica",
    "HTI": "Haití",
    "DOM": "República Dominicana",
    "PRI": "Puerto Rico",
    "TTO": "Trinidad y Tobago",
    "BRB": "Barbados",
    "LCA": "Santa Lucía",
    "VCT": "San Vicente y las Granadinas",
    "GRD": "Granada",
    "ATG": "Antigua y Barbuda",
    "DMA": "Dominica",
    "KNA": "San Cristóbal y Nieves",
    "BHS": "Bahamas",
    "GUY": "Guyana",
    "SUR": "Surinam",
}

# América del Sur
SUR = {
    "COL": "Colombia",
    "VEN": "Venezuela",
    "ECU": "Ecuador",
    "PER": "Perú",
    "BOL": "Bolivia",
    "BRA": "Brasil",
    "PRY": "Paraguay",
    "URY": "Uruguay",
    "ARG": "Argentina",
    "CHL": "Chile",
}

LATAM_ISO = {**CENTRAL, **CARIBE, **SUR}
print(f"Buscando {len(LATAM_ISO)} países...")

# ── Cargar el GeoJSON de Natural Earth ────────────────────────────────────────
# Intentar primero descarga online; si falla, buscar archivo local
geojson_source = None

try:
    import requests
    url = (
        "https://raw.githubusercontent.com/nvkelso/natural-earth-vector"
        "/master/geojson/ne_10m_admin_0_countries.geojson"
    )
    print(f"Descargando desde Natural Earth...")
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    world = r.json()
    print("Descarga exitosa.")
except Exception as e:
    print(f"Sin conexión o error: {e}")
    print("Buscando archivo local ne_10m_admin_0_countries.geojson ...")
    # Buscar en carpetas comunes
    path = os.path.dirname(__file__) + "data/ne_10m_admin_0_countries.geojson"
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            world = json.load(f)
        print(f"Cargado desde: {path}")
        geojson_source = path
    else:
        raise FileNotFoundError(
            "No se encontró el GeoJSON de Natural Earth.\n"
            "Descargalo desde https://naturalearthdata.com y colocalo en la "
            "carpeta data/ como 'ne_10m_admin_0_countries.geojson'"
        )

# ── Función para resolver el ISO de cada feature ──────────────────────────────
def resolve_iso(props: dict) -> str | None:
    """
    Natural Earth a veces pone -99 en ISO_A3 para ciertos territorios.
    Intentamos varios campos alternativos en orden de confiabilidad.
    """
    for field in ("ISO_A3", "ISO_A3_EH", "ADM0_A3", "GU_A3", "SU_A3"):
        val = props.get(field, "")
        if val and val != "-99" and val != "-99.0":
            return val
    return None

# ── Filtrar y normalizar ───────────────────────────────────────────────────────
found = {}
unmatched_features = []

for feat in world["features"]:
    props = feat["properties"]
    iso   = resolve_iso(props)

    if iso in LATAM_ISO and iso not in found:
        # Normalizar properties: dejamos solo lo que necesitamos
        feat["properties"] = {
            "iso":  iso,
            "name": LATAM_ISO[iso],
            # Útiles para debug / futuros usos
            "name_ne":   props.get("NAME", ""),
            "subregion": props.get("SUBREGION", ""),
            "pop_est":   props.get("POP_EST", None),
        }
        found[iso] = feat

# ── Reporte ───────────────────────────────────────────────────────────────────
print(f"\n✓ Encontrados: {len(found)}/{len(LATAM_ISO)} países")

missing = set(LATAM_ISO.keys()) - set(found.keys())
if missing:
    print(f"✗ Faltantes ({len(missing)}):")
    for iso in sorted(missing):
        print(f"    {iso}  {LATAM_ISO[iso]}")
    print()
    print("  → Estos pueden ser territorios muy pequeños o islas no incluidas")

# ── Escribir GeoJSON final ────────────────────────────────────────────────────
latam_geojson = {
    "type": "FeatureCollection",
    "features": list(found.values()),
}

os.makedirs("app/data", exist_ok=True)
out_path = os.path.join("app", "data", "latam.geojson")

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(latam_geojson, f, ensure_ascii=False, indent=2)

size_kb = os.path.getsize(out_path) / 1024
print(f"\n✓ Guardado en: {out_path}  ({size_kb:.0f} KB)")
print(f"  Países incluidos:")
for iso, feat in sorted(found.items()):
    print(f"    {iso}  {feat['properties']['name']}")