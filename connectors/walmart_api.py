import os, requests
from datetime import datetime
from utils import safe_float

def search(keyword, limit=20):
    key = os.getenv("WALMART_API_KEY")
    if not key:
        print("Walmart API key missing.")
        return []
    url = "https://developer.api.walmart.com/api-proxy/service/affil/product/v2/search"
    params = {"apiKey": key, "query": keyword, "numItems": limit}
    results = []
    try:
        r = requests.get(url, params=params, timeout=15)
        data = r.json().get("items", [])
        for it in data:
            price, cur = safe_float(it.get("salePrice"))
            results.append({
                "title": it.get("name"),
                "price": price,
                "currency": cur or "USD",
                "link": it.get("productUrl"),
                "source": "walmart",
                "scraped_at": datetime.utcnow()
            })
    except Exception as e:
        print("Walmart API error:", e)
    return results
