from pyrogram import Client, filters
import requests

API_KEY = "cc852a292bf192a833fd6cc5472e177b"
TMDB_API = "https://api.themoviedb.org/3"
IMG_BASE = "https://image.tmdb.org/t/p/original"

@Client.on_message(filters.command(["p", "poster"]) & filters.private)
async def fetch_images(client, message):
    if len(message.command) < 2:
        await message.reply_text("Usage: `/poster Movie Name 2025`", quote=True)
        return

    query = " ".join(message.command[1:])
    year = None

    # detect if last word is year
    parts = query.rsplit(" ", 1)
    if len(parts) == 2 and parts[1].isdigit() and len(parts[1]) == 4:
        query, year = parts[0], parts[1]

    params = {"api_key": API_KEY, "query": query}
    if year:
        params["year"] = year

    # Search Movie
    res = requests.get(f"{TMDB_API}/search/movie", params=params).json()
    if not res.get("results"):
        return await message.reply_text(f"No movie found for `{query}`")

    movie = res["results"][0]
    movie_id = movie["id"]
    title = movie["title"]
    release_year = movie.get("release_date", "N/A")[:4]

    # Get Images
    img_res = requests.get(f"{TMDB_API}/movie/{movie_id}/images", params={"api_key": API_KEY}).json()

    backdrops = img_res.get("backdrops", [])
    logos = img_res.get("logos", [])
    posters = img_res.get("posters", [])

    msg = f"🎬 **{title} ({release_year})**\n\n"

    # Landscape
    if backdrops:
        msg += "🖼 **Landscape Posters:**\n"
        for i, img in enumerate(backdrops[:6], 1):
            link = f"{IMG_BASE}{img['file_path']}"
            msg += f"{i}. [Click Here]({link})\n"

    # Logos
    if logos:
        msg += "\n🔖 **Logos:**\n"
        for i, img in enumerate(logos[:6], 1):
            link = f"{IMG_BASE}{img['file_path']}"
            msg += f"{i}. [Click Here]({link})\n"

    # Portrait Posters
    if posters:
        msg += "\n📌 **Portrait Posters:**\n"
        for i, img in enumerate(posters[:6], 1):
            link = f"{IMG_BASE}{img['file_path']}"
            msg += f"{i}. [Click Here]({link})\n"

    msg += "\n⚡ Powered By @AddaFiles"

    # ✅ enable preview
    await message.reply_text(msg, disable_web_page_preview=False)
