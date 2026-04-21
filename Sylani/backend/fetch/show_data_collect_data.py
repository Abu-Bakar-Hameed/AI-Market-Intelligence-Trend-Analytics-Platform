# show_data_collect_data.py
from database.database import raw_collection

async def show_data_collect_data():
    results = []

    cursor = raw_collection.find().limit(10)

    async for doc in cursor:
        results.append({
            "title": doc.get("title"),
            "source": doc.get("source"),
            "published_at": str(doc.get("published_at")),
            "content": doc.get("content") or "N/A",
            "category": doc.get("category") or "N/A",
        })

    return results