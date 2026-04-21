def normalize_data(data):
    normalized = []

    for d in data:
        normalized.append({
            "title": (d.get("title") or "").lower(),
            "description": d.get("description"),
            "content": d.get("content"),
            "url": d.get("url"),
            "source": (d.get("source") or "unknown").lower(),
            "published_at": d.get("published_at"),
            "ingested_at": d.get("ingested_at"),
            "category": d.get("category", "news")
        })

    return normalized