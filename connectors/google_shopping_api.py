# connectors/google_shopping_api.py
import os, requests
from datetime import datetime
from dotenv import load_dotenv
from utils import safe_float

load_dotenv()

def search(keyword, limit=20):
    """Fetch product data from Google Shopping via SerpApi."""
    key = os.getenv("SERPAPI_KEY")
    if not key:
        print("❌ SerpApi key missing.")
        return []

    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_shopping",
        "q": keyword,
        "api_key": key,
        "gl": "us",
        "hl": "en"
    }

    results = []
    try:
        r = requests.get(url, params=params, timeout=20)
        r.raise_for_status()
        data = r.json().get("shopping_results", [])
        for it in data[:limit]:
            price, cur = safe_float(it.get("price"))
            results.append({
                "title": it.get("title"),
                "price": price,
                "currency": cur or "USD",
                "link": it.get("link"),
                "source": "google_shopping",
                "scraped_at": datetime.utcnow()
            })
    except Exception as e:
        print("Google Shopping (SerpApi) error:", e)
    return results
