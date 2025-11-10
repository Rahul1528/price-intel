# connectors/etsy_api.py
import os, requests
from datetime import datetime
from dotenv import load_dotenv
from utils import safe_float

load_dotenv()

def search(keyword, limit=20):
    key = os.getenv("ETSY_API_KEY")
    if not key:
        print("Etsy API key missing.")
        return []

    url = "https://openapi.etsy.com/v2/listings/active"
    params = {
        "api_key": key,
        "keywords": keyword,
        "limit": limit,
        "includes": "MainImage"
    }

    results = []
    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        data = r.json().get("results", [])
        for it in data:
            price, cur = safe_float(it.get("price"))
            results.append({
                "title": it.get("title"),
                "price": price,
                "currency": cur or it.get("currency_code"),
                "link": it.get("url"),
                "source": "etsy",
                "scraped_at": datetime.utcnow()
            })
    except Exception as e:
        print("Etsy API error:", e)
    return results
