import pandas as pd

def compute_stats(records):
    df = pd.DataFrame(records)
    df = df.dropna(subset=["price"]).copy()
    if df.empty:
        return {"count": 0, "min": None, "max": None, "mean": None, "median": None, "recommendation": None, "df": df}
    stats = {
        "count": len(df),
        "min": df["price"].min(),
        "max": df["price"].max(),
        "mean": df["price"].mean(),
        "median": df["price"].median(),
    }
    stats["recommendation"] = round(stats["mean"] * 0.95, 2)
    return {**stats, "df": df}
