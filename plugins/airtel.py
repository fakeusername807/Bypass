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

        # Normal OTT detection for non-Airtel links
        for key, name in OTT_MAP.items():
            if key in domain:
                return name

        # Special case for AirtelXstream
        if "airtelxstream" in domain:
            last_part = url.rstrip("/").split("/")[-1]
            ott_code = last_part.split("_")[0].lower()  # e.g., SUNNXT_MOVIE_12968 → sunnxt

            # Map to proper name if available
            for key, name in OTT_MAP.items():
                if key in ott_code:
                    return name

            return "Airtel Xstream"  # fallback if no match
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

        if not poster_url:  # No poster → skip
            text = f"🎬 {movie_name}\n\n<b>{ott_name}</b>\n\n⚡ Powered By @ADDAFILES"
        else:
            text = (
                f"<b>{ott_name}</b> Poster: <a href=\"{poster_url}\">Click Here</a>\n\n"
                f"🌄 <b>Landscape Posters:</b>\n"
                f"1. <a href=\"{poster_url}\">Click Here</a>\n\n"
                f"🎬 {movie_name}\n\n"
                f"⚡ Powered By @ADDAFILES"
            )

        await message.reply_text(
            text=text,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False
        )

    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")
