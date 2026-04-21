# get_raw.py
from database.database import raw_collection
async def get_raw():
    data = []
    cursor = raw_collection.find().limit(50)

    async for doc in cursor:
        doc.pop("_id", None)
        data.append(doc)

    return data