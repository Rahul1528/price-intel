import os
from dotenv import load_dotenv
import requests
from datetime import datetime
from utils import safe_float

# Load credentials
load_dotenv()
app_id = os.getenv("EBAY_APP_ID")
cert_id = os.getenv("EBAY_CERT_ID")
dev_id = os.getenv("EBAY_DEV_ID")
environment = os.getenv("EBAY_ENVIRONMENT", "PRODUCTION")

def search(keyword, limit=20):
    """Search for products using eBay Browse API"""
    url = "https://api.sandbox.ebay.com/buy/browse/v1/item_summary/search" \
        if environment == "SANDBOX" else \
        "https://api.ebay.com/buy/browse/v1/item_summary/search"

    headers = {
        "X-EBAY-C-MARKETPLACE-ID": "EBAY_US",
        "Authorization": f"Bearer {app_id}"
    }
    params = {"q": keyword, "limit": limit}
    results = []

    try:
        r = requests.get(url, headers=headers, params=params, timeout=15)
        data = r.json().get("itemSummaries", [])
        for it in data:
            price_info = it.get("price", {})
            price, cur = safe_float(price_info.get("value"))
            results.append({
                "title": it.get("title"),
                "price": price,
                "currency": cur or price_info.get("currency"),
                "link": it.get("itemWebUrl"),
                "source": "ebay",
                "scraped_at": datetime.utcnow(),
            })
    except Exception as e:
        print("eBay API error:", e)

    return results
