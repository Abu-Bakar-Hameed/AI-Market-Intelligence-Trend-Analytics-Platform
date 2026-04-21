# router.py
from fastapi import APIRouter, Depends, Query, HTTPException
from datetime import datetime, timedelta
from router.router1 import get_current_user
from schemas.models import ArticleRequest, SentimentRequest,KeywordRequest

from ingest.run_pipeline import run_pipeline
from process.run_processing import run_processing
from process.get_top_keywords import get_top_keywords
from process.get_sentiment import get_sentiment
from process.extract_keywords import extract_keywords
from process.growth_trend import growth_trend
from process.daily_counts import daily_counts
from process.article_processor import process
from fetch.show_data_collect_data import show_data_collect_data
from fetch.show_data_processed_data import show_data_processed_data
from database.database import raw_collection, processed_collection

router = APIRouter()




# =====================================================
# ⚙️ POST /ingest (REVIEWED)
# =====================================================
@router.post("/ingest",tags=["Data Ingestion"])
async def ingest_endpoint(get_current_user=Depends(get_current_user)):
    try:
        await run_pipeline()

        data = await show_data_collect_data()

        return {
            "message": "Data ingestion completed successfully",
            "count": len(data),
            "data": data
        }

    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))


# =====================================================
# ⚙️ POST /process (REVIEWED)
# =====================================================
@router.post("/process",tags=["Data Processing"])
async def process_endpoint(get_current_user=Depends(get_current_user)):
    try:
        await run_processing()

        data = await show_data_processed_data()

        return {
            "message": "Processing completed successfully",
            "count": len(data),
            "data": data
        }

    except Exception as e:
        print("PROCESS ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))
# =====================================================
# 📊 GET /trends?days=7 (FIXED)
# =====================================================
@router.get("/trends",tags=["Analytics"])
async def trends(days: int = Query(7, ge=1, le=30), get_current_user=Depends(get_current_user)):
    try:
        cutoff = datetime.utcnow() - timedelta(days=days)

        cursor = raw_collection.find({
            "ingested_at": {"$gte": cutoff}
        })

        words = []

        async for doc in cursor:
            text = (doc.get("title", "") + " " + doc.get("content", "")).lower()
            words += text.split()

        from collections import Counter

        return {
            "days": days,
            "top_keywords": Counter(words).most_common(15),
            "daily_counts": await daily_counts(),
            "growth_trend": await growth_trend()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =====================================================
# 🆕 GET /insights (MISSING FEATURE ADDED)
# =====================================================
@router.get("/insights",tags=["Analytics"])
async def insights(get_current_user=Depends(get_current_user)):
    try:
        cursor = processed_collection.find()

        total = 0
        sentiment = {"positive": 0, "negative": 0, "neutral": 0}

        async for doc in cursor:
            total += 1
            s = doc.get("sentiment", "neutral")
            sentiment[s] += 1

        return {
            "total_articles": total,
            "sentiment_breakdown": sentiment
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/top-keywords",tags=["Analytics"])
async def top_keywords_api(get_current_user=Depends(get_current_user)):
    return {
        "message": "Top keywords fetched successfully",
        "data": await get_top_keywords()
    }

@router.post("/sentiment",tags=["Analytics"])
async def sentiment_api(request: SentimentRequest, get_current_user=Depends(get_current_user)):
    try:
        sentiment, polarity = get_sentiment(request.text)  # ✅ no await

        return {
            "text": request.text,
            "sentiment": sentiment,
            "polarity": polarity
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/extract-keywords",tags=["Analytics"])
async def extract_keywords_api(request: KeywordRequest, get_current_user=Depends(get_current_user)):
    try:
        keywords = extract_keywords(request.text)  # ✅ no await

        return {
            "text": request.text,
            "total_keywords": len(keywords),
            "keywords": keywords
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/growth-trend",tags=["Analytics"])
async def growth_trend_api(get_current_user=Depends(get_current_user)):
    try:
        result = await growth_trend()

        return {
            "message": "Growth trend calculated successfully",
            "data": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/process-article",tags=["Data Processing"])
async def process_article_api(request: ArticleRequest, get_current_user=Depends(get_current_user)):
    try:
        article = {
            "title": request.title,
            "content": request.content
        }

        result = process(article)  # ✅ NO await

        return {
            "message": "Article processed successfully",
            "data": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# =====================================================
# 🔍 GET /search?q=keyword&page=1&limit=10 (PAGINATION ADDED)
# =====================================================
@router.get("/search",tags=["Data Search"])
async def search(
    q: str,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    get_current_user=Depends(get_current_user)
):
    try:
        skip = (page - 1) * limit

        cursor = raw_collection.find({
            "title": {"$regex": q, "$options": "i"}
        }).skip(skip).limit(limit)

        results = []

        async for doc in cursor:
            results.append({
                "title": doc.get("title"),
                "source": doc.get("source"),
                "url": doc.get("url")
            })

        total = await raw_collection.count_documents({
            "title": {"$regex": q, "$options": "i"}
        })

        return {
            "page": page,
            "limit": limit,
            "total_results": total,
            "results": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =====================================================
# 📈 GET /analytics/summary
# =====================================================
@router.get("/analytics/summary",tags=["Analytics"])
async def summary(get_current_user=Depends(get_current_user)):
    try:
        cursor = processed_collection.find()

        total = 0
        sentiment = {"positive": 0, "negative": 0, "neutral": 0}
        relevance_sum = 0

        async for doc in cursor:
            total += 1
            sentiment[doc.get("sentiment", "neutral")] += 1
            relevance_sum += doc.get("relevance_score", 0)

        return {
            "total_articles": total,
            "sentiment": sentiment,
            "avg_relevance": round(relevance_sum / total, 2) if total else 0
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))