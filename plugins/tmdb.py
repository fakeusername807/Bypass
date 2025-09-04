from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import requests
from datetime import datetime  # for sorting by release date

API_KEY = "cc852a292bf192a833fd6cc5472e177b"
TMDB_API = "https://api.themoviedb.org/3"
IMG_BASE = "https://image.tmdb.org/t/p/original"


# ===== TMDB POSTER COMMAND =====
@Client.on_message(filters.command(["p", "poster"]))
async def fetch_images(client, message):
    OFFICIAL_GROUPS = ["-1002311378229"]  # your group ID
    if str(message.chat.id) not in OFFICIAL_GROUPS:
        await message.reply("❌ This command only works in our official group.")
        return

    if len(message.command) < 2:
        await message.reply_text("Usage: `/poster Movie Name 2025`", quote=True)
        return

    query = " ".join(message.command[1:])
    year = None

    # detect if last word is year (e.g., /p Inception 2010)
    parts = query.rsplit(" ", 1)
    if len(parts) == 2 and parts[1].isdigit() and len(parts[1]) == 4:
        query, year = parts[0], parts[1]

    params = {"api_key": API_KEY, "query": query}
    if year:
        params["year"] = year

    # 🔍 Search Movie
    res = requests.get(f"{TMDB_API}/search/movie", params=params).json()
    results = res.get("results", [])

    if not results:
        return await message.reply_text(f"No movie found for `{query}`")

    # ✅ Sort by release date (newest first)
    def parse_date(d):
        try:
            return datetime.strptime(d, "%Y-%m-%d")
        except:
            return datetime.min

    results.sort(key=lambda x: parse_date(x.get("release_date", "")), reverse=True)

    # If year provided → directly send that movie
    if year:
        await send_movie_links(client, message.chat.id, results[0]["id"])
        return

    # If multiple movies → show inline buttons
    buttons = []
    for movie in results[:10]:  # top 10 results
        title = movie["title"]
        release = movie.get("release_date", "N/A")[:4]
        buttons.append([InlineKeyboardButton(f"{title} ({release})", callback_data=f"movie_{movie['id']}")])

    await message.reply_text(
        "Multiple movies found. Please select one:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# ===== Show Posters as Links (No Media Uploads) =====
async def send_movie_links(client, chat_id, movie_id):
    # Get movie info + images
    movie_res = requests.get(f"{TMDB_API}/movie/{movie_id}", params={"api_key": API_KEY}).json()
    img_res = requests.get(f"{TMDB_API}/movie/{movie_id}/images", params={"api_key": API_KEY}).json()

    title = movie_res["title"]
    release_year = movie_res.get("release_date", "N/A")[:4]

    backdrops = img_res.get("backdrops", [])
    logos = img_res.get("logos", [])
    posters = img_res.get("posters", [])

    # ✅ Caption with Clickable Links
    msg = f"🎬 **{title} ({release_year})**\n\n"

    if backdrops:
        msg += "🖼 **Landscape Posters:**\n"
        for i, img in enumerate(backdrops[:10], 1):
            msg += f"{i}. [Click Here]({IMG_BASE}{img['file_path']})\n"

    if logos:
        msg += "\n🔖 **Logos:**\n"
        for i, img in enumerate(logos[:10], 1):
            msg += f"{i}. [Click Here]({IMG_BASE}{img['file_path']})\n"

    if posters:
        msg += "\n📌 **Portrait Posters:**\n"
        for i, img in enumerate(posters[:10], 1):
            msg += f"{i}. [Click Here]({IMG_BASE}{img['file_path']})\n"

    msg += "\n⚡ Powered By @AddaFiles"

    await client.send_message(chat_id, msg, disable_web_page_preview=False)


# ===== Callback Handler =====
@Client.on_callback_query(filters.regex(r"^movie_"))
async def movie_callback(client, callback_query: CallbackQuery):
    movie_id = callback_query.data.split("_")[1]
    await send_movie_links(client, callback_query.message.chat.id, movie_id)
    await callback_query.answer()
