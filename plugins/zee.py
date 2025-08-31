from pyrogram import Client, filters
from pyrogram.types import Message
import aiohttp

# remove any "from bot import app"
# use Client directly in decorator
@Client.on_message(filters.command("zee5") & filters.private)
async def zee5_poster(client: Client, message: Message):
    if len(message.text.split()) < 2:
        await message.reply_text("Send the command as:\n/zee5 <ZEE5_URL>")
        return

    url = message.text.split(None, 1)[1].strip()
    worker_api = f"https://zee.botzs.workers.dev/?url={url}"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(worker_api) as resp:
                data = await resp.json()
        except Exception as e:
            await message.reply_text(f"Error: {e}")
            return

    movie_name = data.get("movie_name", "Unknown Movie")
    landscape = data.get("landscape", [])

    if not landscape:
        await message.reply_text(f"No poster found for {movie_name}.")
        return

    text = f"🎬 Zee Poster: {landscape[0]}\n\n🌄 Landscape:\n1. [Click Here]({landscape[0]})\n\n{movie_name}\n\nPowered By AddaFiles"
    await message.reply_text(text, disable_web_page_preview=False, parse_mode="markdown")
