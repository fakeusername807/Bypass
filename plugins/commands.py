from configs import *
from pyrogram import Client, filters
from pyrogram.types import Message
import aiohttp

# ===== BOT COMMANDS =====
@Client.on_message(filters.command("prime"))
async def prime_scraper(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "⚠️ Please provide a Prime Video URL.\n\nExample:\n`/prime <prime-link>`"
        )

    prime_url = message.command[1]
    api_url = f"{WORKER_URL}/?url={prime_url}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as resp:
                if resp.status != 200:
                    return await message.reply_text("❌ Error fetching from Worker API")

                data = await resp.json()

        # Extract details
        title = data.get("title", "N/A")
        year = data.get("year", "N/A")
        type_ = data.get("type", "N/A")
        prime_poster = data.get("primePoster")
        portrait = data.get("portrait")
        landscape = data.get("landscape")

        # === FORMAT CLEAN OUTPUT ===
        caption = f"""
🖼️ **Prime Poster :** {prime_poster if prime_poster else "N/A"}

🎬 **{title}** ({year})
📺 Type: {type_.title()}

🖼️ **Landscape :** {f"[Click Here]({landscape})" if landscape else "N/A"}
🖼️ **Portrait :** {f"[Click Here]({portrait})" if portrait else "N/A"}

__Powered By ADDABOTZ🦋__
"""

        await message.reply_text(caption, disable_web_page_preview=False)

    except Exception as e:
        await message.reply_text(f"⚠️ Error: `{e}`")
