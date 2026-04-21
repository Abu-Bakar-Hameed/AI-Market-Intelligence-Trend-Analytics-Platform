from database.database import raw_collection

async def store_raw(data):
    try:
        if not data:
            print("No data to insert")
            return

        await raw_collection.insert_many(data)
        print(f"Inserted {len(data)} documents")

    except Exception as e:
        print("DB Insert Error:", e)
        raise e