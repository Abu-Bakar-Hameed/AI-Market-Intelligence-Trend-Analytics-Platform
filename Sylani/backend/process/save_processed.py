from database.database import processed_collection

async def save_processed(data):
    if not data:
        print("No processed data to save")
        return

    try:
        await processed_collection.insert_many(data, ordered=False)
        print(f"Inserted {len(data)} PROCESSED documents")

    except Exception as e:
        print("Insert warning (possible duplicates):", e)