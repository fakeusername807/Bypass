from pyrogram import Client, filters
from pyrogram.types import Message
import aiohttp
import re

@Client.on_message(filters.command("zee5") & filters.private)
async def zee5_poster(client: Client, message: Message):
    if len(message.text.split()) < 2:
        await message.reply_text("Send the command as:\n/zee5 <ZEE5_URL>")
        return

    url = message.text.split(None, 1)[1].strip()
    worker_api = f"https://zee.botzs.workers.dev/?url={url}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(worker_api) as resp:
                data = await resp.json()
    except Exception as e:
        await message.reply_text(f"Error fetching poster: {e}")
        return

    movie_name = data.get("movie_name", "Unknown Movie")
    landscape = data.get("landscape", [])

    if not landscape:
        await message.reply_text(f"No poster found for {movie_name}.")
        return

    # Escape Markdown v2 special characters in movie name
    def escape_md_v2(text):
        return re.sub(r'([_*\[\]()~`>#+-=|{}.!])', r'\\\1', text)

    movie_name_escaped = escape_md_v2(movie_name)
    landscape_url_escaped = escape_md_v2(landscape[0])

    text = f"🎬 Zee Poster: {landscape_url_escaped}\n\n" \
           f"🌄 Landscape:\n" \
           f"1. [Click Here]({landscape_url_escaped})\n\n" \
           f"{movie_name_escaped}\n\n" \
           f"Powered By AddaFiles"

    await message.reply_text(
        text,
        disable_web_page_preview=False,
        parse_mode="markdown_v2"
    )
