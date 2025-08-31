from pyrogram import Client, filters
import requests

TMDB_API_KEY = "cc852a292bf192a833fd6cc5472e177b"
TMDB_BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/"

@Client.on_message(filters.command(["p", "poster"]) & filters.private)
async def fetch_all_images(client, message):
    if len(message.command) < 2:
        await message.reply_text("Send a movie name. Example:\n/p Inception")
        return

    movie_name = " ".join(message.command[1:])
    # Search movie
    search_url = f"{TMDB_BASE_URL}/search/movie?api_key={TMDB_API_KEY}&query={movie_name}"
    res = requests.get(search_url).json()
    results = res.get("results")
    if not results:
        await message.reply_text(f"No movie found for '{movie_name}'.")
        return

    movie = results[0]
    movie_id = movie.get("id")
    title = movie.get("title")

    # Get all images
    images_url = f"{TMDB_BASE_URL}/movie/{movie_id}/images?api_key={TMDB_API_KEY}"
    images = requests.get(images_url).json()

    msg = f"Movie: {title}\n\n"

    # Landscape
    backdrops = images.get("backdrops", [])
    if backdrops:
        msg += "• Landscape:\n"
        for i, img in enumerate(backdrops[:10], 1):  # Top 10
            msg += f"{i}. [Click Here]({IMAGE_BASE_URL}original{img['file_path']})\n"

    # Logos
    logos = images.get("logos", [])
    if logos:
        msg += "\n• Logos:\n"
        for i, img in enumerate(logos[:10], 1):
            msg += f"{i}. [Click Here]({IMAGE_BASE_URL}original{img['file_path']})\n"

    # Portrait Posters
    posters = images.get("posters", [])
    if posters:
        msg += "\n• Portrait Posters:\n"
        for i, img in enumerate(posters[:10], 1):
            msg += f"{i}. [Click Here]({IMAGE_BASE_URL}original{img['file_path']})\n"

    msg += "\nPowered by @ADDAFILES"

    await message.reply_text(msg, disable_web_page_preview=True)
