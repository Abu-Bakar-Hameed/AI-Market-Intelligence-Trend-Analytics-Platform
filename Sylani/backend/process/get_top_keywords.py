# get_top_keywords.py
from fastapi import HTTPException
from process.extract_keywords import extract_keywords

from collections import Counter
from database.database import raw_collection
async def get_top_keywords():
    try:
        cursor = raw_collection.find()
        all_keywords = []

        async for doc in cursor:
            title = doc.get("title") or ""
            content = doc.get("content") or ""

            text = f"{title} {content}"

            keywords = extract_keywords(text)
            if keywords:
                all_keywords.extend(keywords)

        top_keywords = Counter(all_keywords).most_common(10)

        # Convert tuple -> JSON safe format
        return [
            {"keyword": k, "count": v}
            for k, v in top_keywords
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))