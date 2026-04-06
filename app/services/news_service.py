import requests
from config import NEWS_API_KEY, NEWS_URL

def fetch_news(country: str = "in", category: str = "technology") -> dict:
    try:
        params = {
            "q":        "india technology",
            "language": "en",
            "pageSize": 5,
            "apiKey":   NEWS_API_KEY
        }

        response = requests.get(NEWS_URL, params=params, timeout=5)
        response.raise_for_status()
        raw = response.json()

        if raw.get("status") != "ok":
            return {"source": "news", "status": "error", "message": raw.get("message", "Unknown error")}

        articles = []
        for article in raw.get("articles", []):
            articles.append({
                "title":        article.get("title", "N/A"),
                "source":       article.get("source", {}).get("name", "N/A"),
                "published_at": article.get("publishedAt", "N/A"),
                "url":          article.get("url", "N/A")
            })

        return {
            "source":   "news",
            "country":  country,
            "category": category,
            "articles": articles,
            "status":   "success"
        }

    except requests.exceptions.Timeout:
        return {"source": "news", "status": "error", "message": "Request timed out"}

    except requests.exceptions.HTTPError as e:
        return {"source": "news", "status": "error", "message": str(e)}

    except Exception as e:
        return {"source": "news", "status": "error", "message": str(e)}