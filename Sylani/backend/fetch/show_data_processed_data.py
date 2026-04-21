from database.database import processed_collection

async def show_data_processed_data():
    cursor = processed_collection.find().limit(10)
    results = []

    async for doc in cursor:
        results.append({
            "title": doc.get("title"),
            "sentiment": doc.get("sentiment"),
            "polarity": doc.get("polarity"),
            "keywords": doc.get("keywords"),
            "trend_score": doc.get("trend_score"),
            "relevance_score": doc.get("relevance_score"),
        })

    return results