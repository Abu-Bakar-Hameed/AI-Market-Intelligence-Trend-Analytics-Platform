from collections import defaultdict
from database.database import raw_collection

async def daily_counts():
    cursor = raw_collection.find()
    counts = defaultdict(int)

    async for doc in cursor:
        published = doc.get("published_at")

        if not published:
            continue

        # Handle both string and datetime safely
        if isinstance(published, str):
            date = published[:10]
        else:
            date = str(published)[:10]

        counts[date] += 1

    return dict(counts)