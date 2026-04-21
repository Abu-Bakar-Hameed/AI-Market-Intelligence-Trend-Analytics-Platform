from datetime import datetime, timezone

def clean_data(articles):
    seen = set()
    cleaned = []

    for a in articles:
        url = a.get("url")

        if not url or url in seen:
            continue

        seen.add(url)

        title = a.get("title")
        if not title:
            continue

        cleaned.append({
            "title": title.strip(),
            "description": a.get("description"),
            "content": a.get("content"),
            "url": url,
            "source": a.get("source", {}).get("name", "unknown"),
            "published_at": a.get("publishedAt"),
            "ingested_at": datetime.now(timezone.utc),
            "category": "news"
        })

    return cleaned