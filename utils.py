import re

def safe_float(text):
    if not text:
        return (None, None)
    cur = None
    if "£" in text:
        cur = "GBP"
    elif "$" in text:
        cur = "USD"
    elif "€" in text:
        cur = "EUR"
    m = re.search(r"([0-9]+(?:[.,][0-9]+)?)", text.replace(",", ""))
    if not m:
        return (None, cur)
    try:
        return (float(m.group(1)), cur)
    except:
        return (None, cur)
