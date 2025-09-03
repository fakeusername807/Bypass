import requests
import re
from bs4 import BeautifulSoup
from pyrogram import Client, filters
from pyrogram.enums import ParseMode

WORKER_URL = "https://air.botzs.workers.dev/?url="

# OTT Detection Map
OTT_MAP = {
    "airtelxstream": "Airtel Xstream",
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
    url = url.lower()
    for key, name in OTT_MAP.items():
        if key in url:
            return name
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


# ========= /airtel or /airtelxtream =========
@Client.on_message(filters.command(["airtel", "airtelxtream"]))
async def airtel_handler(client, message):  # <-- async here
    try:
        if len(message.command) < 2:
            await message.reply_text("❌ Usage: /airtel <movie_url>")
            return

        movie_url = message.command[1]

        ott_name = detect_ott(movie_url)
        movie_name = extract_title_year(movie_url)

        api_url = f"{WORKER_URL}{movie_url}"
        res = requests.get(api_url).json()

        if "image" not in res:
            await message.reply_text("❌ Poster not found from worker")
            return

        poster_url = res["image"]

        text = (
            f"{ott_name} Poster: {poster_url}\n\n"
            f"🌄 Landscape Posters:\n"
            f"1. <a href=\"{poster_url}\">Click Here</a>\n\n"
            f"🎬 {movie_name}\n\n"
            f"⚡ Powered By @AddaFiles"
        )

        await message.reply_text(   # <-- await here
            text=text,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False
        )

    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")  # <-- await here
