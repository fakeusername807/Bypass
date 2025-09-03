import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from pyrogram import Client, filters
from pyrogram.enums import ParseMode

WORKER_URL = "https://air.botzs.workers.dev/?url="

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
    try:
        domain = urlparse(url).netloc.lower()
        for key, name in OTT_MAP.items():
            if key in domain:
                return name
        if "airtelxstream" in domain:
            return "Airtel Xstream"
    except Exception:
        pass
    return "OTT"

def extract_title_year(url: str) -> str:
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        title = soup.find("meta", property="og:title")
        title_text = title["content"] if title and title.get("content") else (
            soup.title.string if soup.title else "Unknown Movie"
        )

        year_match = re.search(r"\b(19|20)\d{2}\b", title_text)
        year = year_match.group(0) if year_match else "Unknown"

        clean_title = re.sub(r"\(\d{4}\)|\d{4}", "", title_text).strip()
        return f"{clean_title} ({year})"
    except Exception:
        return "Unknown Movie"

def extract_poster(url: str) -> str:
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content"):
            return og_image["content"]
    except Exception:
        pass
    return None


@Client.on_message(filters.command(["airtel", "airtelxstream"]))
async def airtel_handler(client, message):
    try:
        if len(message.command) < 2:
            await message.reply_text("❌ Usage: /airtel <movie_url>")
            return

        movie_url = message.command[1]

        ott_name = detect_ott(movie_url)
        movie_name = extract_title_year(movie_url)

        api_url = f"{WORKER_URL}{movie_url}"
        res = requests.get(api_url).json()
        poster_url = res.get("image")
        landscape_url = res.get("original")

        if not poster_url or "AddaFiles.jpg" in poster_url:
            poster_url = extract_poster(movie_url)

        if not poster_url:
            poster_url = "https://i.ibb.co/p6HVXFQm/AddaFiles.jpg"

        if not landscape_url:
            landscape_url = poster_url  # fallback

        text = (
            f"<b>{ott_name}</b> Poster: {poster_url}\n\n"
            f"🌄 <b>Landscape:</b> <a href=\"{landscape_url}\">Click Here</a>\n\n"
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
