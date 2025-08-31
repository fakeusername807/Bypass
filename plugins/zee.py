from pyrogram import filters
from pyrogram.types import Message
import aiohttp

@app.on_message(filters.command("zee5") & filters.private)
async def zee5(client, message: Message):
    if len(message.command) < 2:
        await message.reply_text(
            "Please provide a ZEE5 URL.\nExample:\n/zee5 https://www.zee5.com/movies/details/your-movie"
        )
        return

    zee5_url = message.command[1]
    if "zee5.com" not in zee5_url:
        await message.reply_text("Please provide a valid ZEE5 URL.")
        return

    msg = await message.reply_text("Fetching poster... ⏳")

    try:
        CLOUDFLARE_WORKER_URL = "https://zee.botzs.workers.dev/?url="

        async with aiohttp.ClientSession() as session:
            async with session.get(CLOUDFLARE_WORKER_URL + zee5_url, timeout=15) as resp:
                data = await resp.json()

        if "error" in data:
            await msg.edit(f"Error: {data['error']}")
            return

        images = data.get("images", [])
        if not images:
            await msg.edit("No images found for this URL.")
            return

        # Use the first image as landscape
        landscape = images[0]

        # Movie name from URL
        movie_name = zee5_url.rstrip("/").split("/")[-1].replace("-", " ").title()

        # Build message
        text = f"Zee Poster: {landscape}\n\n"
        text += f"🌄 Landscape Posters:\n1. [Click Here]({landscape})\n\n"
        text += f"🎬 {movie_name}\n\nPowered By AddaFiles"

        await msg.edit(text, disable_web_page_preview=False)

    except Exception as e:
        await msg.edit(f"Failed to fetch poster.\nError: {e}")
