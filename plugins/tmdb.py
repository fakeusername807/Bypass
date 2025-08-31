from pyrogram import Client, filters
from pyrogram.types import Message
import requests

# Your TMDb API key
TMDB_API_KEY = "cc852a292bf192a833fd6cc5472e177b"
TMDB_BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/"

@Client.on_message(filters.command(["p", "poster"]) & filters.private)
async def fetch_posters(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text(
            "Send a movie name after the command. Example:\n`/p Inception`"
        )
        return

    movie_name = " ".join(message.command[1:])
    search_url = f"{TMDB_BASE_URL}/search/movie?api_key={TMDB_API_KEY}&query={movie_name}"

    try:
        response = requests.get(search_url).json()
        results = response.get("results")

        if not results:
            await message.reply_text(f"No movie found for '{movie_name}'.")
            return

        movie = results[0]
        title = movie.get("title")
        movie_id = movie.get("id")

        # Get images
        images_url = f"{TMDB_BASE_URL}/movie/{movie_id}/images?api_key={TMDB_API_KEY}"
        images = requests.get(images_url).json()

        # Build message
        msg = f"Movie: {title}\n\n"

        # Landscape Posters
        landscapes = images.get("backdrops", [])[:6]  # top 6
        msg += "•English Landscape:\n"
        for i, img in enumerate(landscapes, 1):
            msg += f"{i}. [Click Here]({IMAGE_BASE_URL}original{img['file_path']})\n"

        # Logos
        logos = images.get("logos", [])[:6]
        if logos:
            msg += "\n•Logos Png:\n"
            for i, img in enumerate(logos, 1):
                msg += f"{i}. [Click Here]({IMAGE_BASE_URL}original{img['file_path']})\n"

        # Portrait Posters
        portraits = images.get("posters", [])[:6]
        if portraits:
            msg += "\n•Portrait Posters:\n"
            for i, img in enumerate(portraits, 1):
                msg += f"{i}. [Click Here]({IMAGE_BASE_URL}original{img['file_path']})\n"

        msg += "\nPowered By ADDAFILES"

        await message.reply_text(msg, disable_web_page_preview=True)

    except Exception as e:
        await message.reply_text(f"Error occurred: {e}")
