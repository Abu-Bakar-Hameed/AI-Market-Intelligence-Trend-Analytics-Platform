def trend_score(keywords):
    return len(keywords)


def relevance_score(text, keywords):
    if not text:
        return 0

    text_lower = text.lower()
    keyword_hits = sum(text_lower.count(k) for k in keywords)
    text_length = len(text.split())

    score = (keyword_hits * 2) + (text_length * 0.01)
    return round(score, 2)