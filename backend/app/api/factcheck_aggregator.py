import asyncio
import httpx
from bs4 import BeautifulSoup
import os

GOOGLE_API_URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
GOOGLE_API_KEY = os.getenv("GOOGLE_FACTCHECK_API_KEY")

# --- Google Fact Check ---
async def fetch_google_factcheck(query: str):
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(GOOGLE_API_URL, params={"query": query, "key": GOOGLE_API_KEY, "languageCode": "en"})
            data = res.json()
            items = []
            for claim in data.get("claims", []):
                review = claim.get("claimReview", [{}])[0]
                items.append({
                    "publisher": review.get("publisher", {}).get("name", "Unknown"),
                    "title": review.get("title", claim.get("text", "")),
                    "url": review.get("url"),
                    "rating": review.get("textualRating", "Unrated"),
                    "language": claim.get("languageCode", "en"),
                })
            return items
    except Exception as e:
        print(f"⚠️ Google Fact Check error: {e}")
        return []

# --- Snopes ---
async def fetch_snopes(query: str):
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(f"https://www.snopes.com/search/?q={query}")
            soup = BeautifulSoup(res.text, "html.parser")
            items = []
            for article in soup.select("article.media-wrapper"):
                title_tag = article.select_one("h2.title")
                link = title_tag.find("a")["href"] if title_tag else None
                title = title_tag.get_text(strip=True) if title_tag else "Untitled"
                rating_tag = article.select_one("span.rating-text")
                rating = rating_tag.get_text(strip=True) if rating_tag else "Unrated"
                items.append({
                    "publisher": "Snopes",
                    "title": title,
                    "url": link,
                    "rating": rating,
                    "language": "en"
                })
            return items[:5]
    except Exception as e:
        print(f"⚠️ Snopes error: {e}")
        return []

# --- PolitiFact ---
async def fetch_politifact(query: str):
    try:
        rss_url = "https://www.politifact.com/rss/factchecks/"
        async with httpx.AsyncClient() as client:
            res = await client.get(rss_url)
            soup = BeautifulSoup(res.text, "xml")
            items = []
            for item in soup.find_all("item"):
                title = item.title.text
                link = item.link.text
                if query.lower() in title.lower():
                    items.append({
                        "publisher": "PolitiFact",
                        "title": title,
                        "url": link,
                        "rating": "Verified",
                        "language": "en"
                    })
            return items[:5]
    except Exception as e:
        print(f"⚠️ PolitiFact error: {e}")
        return []

# --- AFP FactCheck ---
async def fetch_afp(query: str):
    try:
        rss_url = "https://factcheck.afp.com/rss.xml"
        async with httpx.AsyncClient() as client:
            res = await client.get(rss_url)
            soup = BeautifulSoup(res.text, "xml")
            items = []
            for item in soup.find_all("item"):
                title = item.title.text
                link = item.link.text
                if query.lower() in title.lower():
                    items.append({
                        "publisher": "AFP FactCheck",
                        "title": title,
                        "url": link,
                        "rating": "Verified",
                        "language": "en"
                    })
            return items[:5]
    except Exception as e:
        print(f"⚠️ AFP error: {e}")
        return []

# --- Agregador principal ---
async def aggregate_factchecks(query: str):
    results = await asyncio.gather(
        fetch_google_factcheck(query),
        fetch_snopes(query),
        fetch_politifact(query),
        fetch_afp(query),
    )
    merged = [item for sublist in results for item in sublist]
    return merged
