install:
	uv sync 

load_data:
	uv run python scripts/build_latam_geojson.py
	uv run python scripts/generate_datasets.py

run:
	uv run streamlit run app/app.py
