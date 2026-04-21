# process.py 
from process.get_sentiment import get_sentiment
from process.extract_keywords import extract_keywords
from process.score import trend_score,relevance_score

def process(article):
    text = (article.get("title", "") or "") + " " + (article.get("content", "") or "")

    sentiment, polarity = get_sentiment(text)
    keywords = extract_keywords(text)

    return {
        **article,
        "sentiment": sentiment,
        "polarity": polarity,
        "keywords": keywords[:10],
        "trend_score": trend_score(keywords),
        "relevance_score": relevance_score(text, keywords)
    }