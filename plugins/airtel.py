import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from pyrogram import Client, filters
from pyrogram.enums import ParseMode

WORKER_URL = "https://air.botzs.workers.dev/?url="

# OTT Detection Map (Removed airtelxstream)
OTT_MAP = {
    "zee5": "ZEE5",
    "hotstar": "JioHotstar",
    "disneyplus": "Disney+ Hotstar",
    "jiocinema": "JioCinema",
    "sunnxt": "Sun NXT",
    "aha": "Aha",
    "sonyliv": "Sony LIV",
    "lionsgate": "Lionsgate Play",
    "hoichoi": "Hoichoi",
    "erosnow": "Eros Now",
    "shemaroome": "ShemarooMe",
    "manoramamax": "ManoramaMax",
    "hungama": "Hungama Play",
    "epicon": "Epic On",
    "docubay": "DocuBay",
    "chaupal": "Chaupal",
    "shortstv": "ShortsTV",
    "altbalaji": "Alt Balaji",
    "ultra": "Ultra",
    "klikk": "Klikk",
    "dollywood": "Dollywood Play",
    "nammaflix": "Namma Flix",
    "fancode": "FanCode",
    "stage": "Stage",
    "rajdigital": "Raj Digital TV",
    "divo": "DIVO",
    "socialswag": "Social Swag",
    "primevideo": "Amazon Prime Video",
    "mxplayer": "MX Player",
}

def detect_ott(url: str) -> str:
    """Detect OTT platform from domain"""
    try:
        domain = urlparse(url).netloc.lower()
        for key, name in OTT_MAP.items():
            if key in domain:
                return name
        # Special case: Airtel Xstream (not in map anymore)
        if "airtelxstream" in domain:
            return "Airtel Xstream"
    except Exception:
        pass
    return "OTT"

def extract_title_year(url: str) -> str:
    """Scrape movie title + year from OTT page"""
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        title = soup.find("meta", property="og:title")
        if title and title.get("content"):
            title_text = title["content"]
        else:
            title_text = soup.title.string if soup.title else "Unknown Movie"

        year_match = re.search(r"\b(19|20)\d{2}\b", title_text)
        year = year_match.group(0) if year_match else "Unknown"

        clean_title = re.sub(r"\(\d{4}\)|\d{4}", "", title_text).strip()

        return f"{clean_title} ({year})"
    except Exception:
        return "Unknown Movie"

def extract_poster(url: str) -> str:
    """Scrape poster (og:image) if worker fails"""
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content"):
            return og_image["content"]
    except Exception:
        pass
    return None


# ========= /airtel or /airtelxtream =========
@Client.on_message(filters.command(["airtel", "airtelxtream"]))
async def airtel_handler(client, message):
    try:
        if len(message.command) < 2:
            await message.reply_text("❌ Usage: /airtel <movie_url>")
            return

        movie_url = message.command[1]

        ott_name = detect_ott(movie_url)
        movie_name = extract_title_year(movie_url)

        # Try Worker first
        api_url = f"{WORKER_URL}{movie_url}"
        res = requests.get(api_url).json()
        poster_url = res.get("image")

        # Fallback: if worker fails or returns AddaFiles default
        if not poster_url or "AddaFiles.jpg" in poster_url:
            poster_url = extract_poster(movie_url)

        if not poster_url:
            await message.reply_text("❌ Poster not found")
            return

        text = (
            f"<b>{ott_name}</b> Poster: {poster_url}\n\n"
            f"🌄 <b>Landscape Posters:</b>\n"
            f"1. <a href=\"{poster_url}\">Click Here</a>\n\n"
            f"🎬 {movie_name}\n\n"
            f"⚡ Powered By @AddaFiles"
        )

        await message.reply_text(
            text=text,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False
        )

    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")
