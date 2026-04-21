from process.get_raw import get_raw
from process.article_processor import process
from process.save_processed import save_processed



async def run_processing():
    try:
        raw = await get_raw()
        if not raw:
            return
        processed = [process(r) for r in raw]
        await save_processed(processed)
    except Exception as e:
        print("Processing Error:", e)
        raise e