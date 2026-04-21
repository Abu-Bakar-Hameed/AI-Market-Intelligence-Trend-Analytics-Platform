# get_sentiment.py
from textblob import TextBlob


def get_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity

    if polarity > 0:
        return "positive", polarity
    elif polarity < 0:
        return "negative", polarity
    return "neutral", polarity