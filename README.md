# one-prompt-pipeline
End-to-end data pipeline generated from a single prompt —  Bronze → Silver → Gold → Streamlit dashboard,  built entirely by a Claude Code agent team.

## Layers
- **Bronze**: Raw CSV download → data/bronze/happiness_raw.csv
- **Silver**: Cleaned parquet → data/silver/happiness_clean.parquet  
- **Gold**: Aggregated parquet → data/gold/happiness_aggregated.parquet

## Setup
pip install -r requirements.txt

## Run
python src/ingest.py
python src/transform.py
python src/aggregate.py
