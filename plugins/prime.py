from config import *
from pyrogram import Client, filters
from pyrogram.types import Message
import aiohttp

# ===== START COMMAND =====
@Client.on_message(filters.command("start"))
async def start_cmd(_, message: Message):
    await message.reply_text(
        f"👋 Hello {message.from_user.first_name}!\n\n"
        "I am your **OTT Scraper Bot** 🎬\n\n"
        "Commands:\n"
        "✅ `/health` - Check bot status\n"
        "✅ `/prime <url>` - Scrape Prime Video details\n\n"
        "👉 Example:\n`/prime https://www.primevideo.com/detail/...`\n\n"
        "🚀 Running on successfully 😂!"
    )


# ===== HEALTH COMMAND =====
@Client.on_message(filters.command("health"))
async def health(_, message: Message):
    await message.reply_text("✅ Bot is Alive & Healthy on SERVER 😂!")


# ===== PRIME SCRAPER =====
@Client.on_message(filters.command("prime"))
async def prime_scraper(_, message: Message):
    # If no URL is given after /prime
    if len(message.command) == 1:
        return await message.reply_text(
            "⚠️ Please provide a Prime Video URL.\n\n"
            "👉 Example:\n`/prime https://www.primevideo.com/detail/...`",
            disable_web_page_preview=True
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

        # Send with preview enabled (poster will show if link works)
        await message.reply_text(caption, disable_web_page_preview=False)

    except Exception as e:
        await message.reply_text(f"⚠️ Error: `{e}`")
