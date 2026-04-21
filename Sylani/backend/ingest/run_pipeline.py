# run_pipeline.py
from ingest.fetch_news import fetch_news
from ingest.clean_data import clean_data
from ingest.normalize_data import normalize_data
from ingest.store_raw import store_raw

async def run_pipeline():
    raw = fetch_news("AI")
    cleaned = clean_data(raw)
    normalized = normalize_data(cleaned)
    await store_raw(normalized)




