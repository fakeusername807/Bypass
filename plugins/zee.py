from pyrogram import filters
from bot import app   # ← import your bot instance

@app.on_message(filters.command("zee5") & filters.private)
async def zee5_poster(client, message):
    url = message.text.split(None, 1)[1] if len(message.text.split()) > 1 else None
    if not url:
        await message.reply_text("Send /zee5 <ZEE5_URL>")
        return
    # Call your Cloudflare Worker API
    worker_api = f"https://zee.botzs.workers.dev/?url={url}"
    async with app.storage.session.get(worker_api) as r:  # or use aiohttp if needed
        data = await r.json()
    movie_name = data.get("movie_name")
    landscape = data.get("landscape", [])
    text = f"🎬 Zee Poster: {landscape[0] if landscape else 'N/A'}\n\n🌄 Landscape:\n1. Click Here\n\n{movie_name}"
    await message.reply_text(text)
