def extract_keywords(text):
    if not text:
        return []

    words = text.lower().split()

    stop_words = {
        "the", "is", "a", "an", "and", "in", "on",
        "of", "to", "for", "with", "this", "that"
    }

    cleaned = []

    for w in words:
        w = w.strip(".,!?()[]{}\"'")
        if w.isalpha() and w not in stop_words:
            cleaned.append(w)

    return cleaned