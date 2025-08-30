from pyrogram import Client, filters
from pyrogram.types import Message
import aiohttp
import json

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
                data = await resp.json()

        title = data.get("title", "Unknown Title")
        size = data.get("size", "Unknown Size")
        links = data.get("links", {})

        text = f"""
📁 𝚃𝚒𝚝𝚕𝚎
{title}
📦 𝚂𝚒𝚣𝚎 :- {size}

⚡ INSTANT DL : [Click Here]({links.get('instantdl','')})
☁️ CLOUD DOWNLOAD : [Click Here]({links.get('clouddl','')})
📩 TELEGRAM FILE : [Click Here]({links.get('telegram','')})
🗂 GOFILE : [Click Here]({links.get('gofile','')})

━━━━━━━━━━━━━━━━━━
⚡ Powered By @AddaFiles 🚀
"""

        await message.reply_text(text, disable_web_page_preview=True)

    except Exception as e:
        await message.reply_text(f"⚠️ Error: `{e}`")
