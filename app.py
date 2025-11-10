import streamlit as st
from PIL import Image
from analysis import compute_stats
from db import init_db, insert_many, fetch_by_keyword, clear_keyword
from image_recognition import extract_keywords_from_image
import pandas as pd
import altair as alt

# Import all connectors
from connectors import ebay_api, amazon_api, walmart_api, etsy_api

# -----------------------------------------
# Streamlit UI Setup
# -----------------------------------------
st.set_page_config(page_title="🧠 AI Price Intelligence", layout="wide")
init_db()

st.title("🧠 AI-Powered Price Intelligence Dashboard")

# Sidebar – choose sources
st.sidebar.header("Marketplaces")
sources = st.sidebar.multiselect(
    "Select marketplaces to search",
    ["eBay", "Amazon", "Walmart", "Etsy"],
    default=["eBay"]
)

st.sidebar.markdown("---")
st.sidebar.info("You can select multiple sources at once.")

# -----------------------------------------
# Step 1: Upload or type
# -----------------------------------------
uploaded = st.file_uploader("Upload a product image", type=["jpg", "jpeg", "png"])
query = st.text_input("Or enter a keyword manually")

detected = None
if uploaded:
    img = Image.open(uploaded)
    st.image(img, caption="Uploaded Image", width=300)
    with st.spinner("🔍 Analyzing image..."):
        labels = extract_keywords_from_image(img)
        detected = labels[0]
    st.success(f"Detected item type: **{detected}**")
    if not query:
        query = detected

st.markdown("---")

# -----------------------------------------
# Step 2: Fetch listings from APIs
# -----------------------------------------
pages = st.slider("Number of pages to search (for APIs that support it)", 1, 3, 1)

def run_sources(keyword):
    all_items = []
    if "eBay" in sources:
        with st.spinner("Fetching from eBay..."):
            all_items += ebay_api.search(keyword, limit=pages * 20)
    if "Amazon" in sources:
        with st.spinner("Fetching from Amazon..."):
            all_items += amazon_api.search(keyword)
    if "Walmart" in sources:
        with st.spinner("Fetching from Walmart..."):
            all_items += walmart_api.search(keyword, limit=pages * 20)
    if "Etsy" in sources:
        with st.spinner("Fetching from Etsy..."):
            all_items += etsy_api.search(keyword, limit=pages * 20)
    return all_items

if st.button("🔎 Get Price Metrics") and query:
    with st.spinner("Collecting listings from selected marketplaces..."):
        items = run_sources(query)
        for it in items:
            it["keyword"] = query
        insert_many(items)
    st.success(f"✅ Fetched and stored {len(items)} items for '{query}'")

if st.button("🗑️ Clear data for this keyword") and query:
    clear_keyword(query)
    st.success("Cleared previous results.")

# -----------------------------------------
# Step 3: Show metrics
# -----------------------------------------
records = fetch_by_keyword(query) if query else []
if records:
    stats = compute_stats(records)
    st.subheader("📊 Price Metrics")
    st.write(f"Count: **{stats['count']}**")
    st.write(f"Min: **{stats['min']}**")
    st.write(f"Max: **{stats['max']}**")
    st.write(f"Mean: **{stats['mean']}**")
    st.write(f"Median: **{stats['median']}**")
    st.metric("Recommended Price", stats["recommendation"])

    df = stats["df"]

    # Boxplot
    st.subheader("Price Distribution")
    chart = alt.Chart(df).mark_boxplot().encode(
        y="price:Q",
        color="source:N"
    ).properties(height=200)
    st.altair_chart(chart, use_container_width=True)

    # Listings table
    st.subheader("Listings")
    show = df[["title", "price", "currency", "link", "source", "scraped_at"]]
    show["link"] = show["link"].apply(lambda x: f"[link]({x})" if x else "")
    st.dataframe(show, height=400)

    # CSV export
    csv = df.to_csv(index=False)
    st.download_button("⬇️ Download CSV", csv, file_name=f"{query}_listings.csv")
else:
    st.info("Upload an image or enter a keyword, then click 'Get Price Metrics'.")
