from pyrogram import Client, filters
from pyrogram.types import Message
import aiohttp

WORKER_URL = "https://gdflix.botzs.workers.dev/?url="

# ===== GD / GDFLIX COMMAND =====
@Client.on_message(filters.command(["gd", "gdflix"]))
async def gd_scraper(_, message: Message):
    if len(message.command) == 1:
        return await message.reply_text(
            "⚠️ Usage: `/gd <gdlink>`",
            disable_web_page_preview=True
        )

    link = message.command[1]
    if not link.startswith("http"):
        return await message.reply_text("⚠️ Please send a valid GDLink URL")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(WORKER_URL + link) as resp:
                if resp.status != 200:
                    return await message.reply_text("❌ Error fetching from Worker API")
                text = await resp.text()

        await message.reply_text(text, disable_web_page_preview=True)

    except Exception as e:
        await message.reply_text(f"⚠️ Error: `{e}`")
