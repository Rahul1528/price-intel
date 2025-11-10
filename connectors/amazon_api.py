# Minimal Product Advertising API client (use your own credentials)
import os, requests, datetime, hashlib, hmac, base64
from utils import safe_float
from urllib.parse import urlencode

def search(keyword, max_results=10):
    access = os.getenv("AMAZON_ACCESS_KEY")
    secret = os.getenv("AMAZON_SECRET_KEY")
    tag = os.getenv("AMAZON_ASSOCIATE_TAG")
    region = os.getenv("AMAZON_REGION", "us-east-1")
    if not all([access, secret, tag]):
        print("Amazon API keys missing.")
        return []
    # In production use a PAAPI helper library for signing.
    # Here we show placeholder return.
    print("Using Amazon API placeholder – please configure PAAPI v5 client.")
    return []
