import requests
from config import NEWS_API_KEY

def fetch_news(query="AI"):
    url = "https://newsapi.org/v2/everything"

    params = {
        "q": query,
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": 50,
        "apiKey": NEWS_API_KEY
    }

    try:
        res = requests.get(url, params=params)
        data = res.json()

        if res.status_code != 200 or data.get("status") != "ok":
            print("API Error:", data)
            return []

        return data.get("articles", [])

    except Exception as e:
        print("Fetch Error:", e)
        return []