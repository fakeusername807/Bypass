from pyrogram import Client, filters
from pyrogram.types import Message
import aiohttp

WORKER_URL = "https://zee.botzs.workers.dev/"

@Client.on_message(filters.command("zee5") & filters.private)
async def zee5_poster(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text(
            "Send a ZEE5 movie URL like:\n/zee5 https://www.zee5.com/movies/details/krack/0-0-1z51604"
        )
        return

    movie_url = message.command[1]

    if "zee5.com" not in movie_url:
        await message.reply_text("Please provide a valid ZEE5 movie URL.")
        return

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{WORKER_URL}?url={movie_url}") as resp:
                data = await resp.json()

        movie_name = data.get("movie_name", "Unknown Movie")
        landscape = data.get("landscape", [])

        if not landscape:
            await message.reply_text(f"No poster found for {movie_name}.")
            return

        # Prepare text with clickable link for landscape
        text = f"🌄 <b>Landscape Poster:</b>\n" \
               f'1. <a href="{landscape[0]}">Click Here</a>\n\n' \
               f"🎬 <b>{movie_name}</b>\n\n" \
               f"Powered By AddaFiles"

        # Send the first landscape image as actual photo with caption
        await client.send_photo(
            chat_id=message.chat.id,
            photo=landscape[0],
            caption=text,
            parse_mode="html"
        )

    except Exception as e:
        await message.reply_text(f"Error fetching poster: {e}")
