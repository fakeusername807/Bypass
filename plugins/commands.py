from configs import *
from pyrogram import Client, filters

# ===== BOT COMMANDS =====
@client.on_message(filters.command("start"))
async def start_cmd(_, message: Message):
    await message.reply_text(
        f"👋 Hello {message.from_user.first_name}!\n\n"
        "I am your **OTT Scraper Bot** 🎬\n\n"
        "Commands:\n"
        "✅ `/health` - Check bot status\n"
        "✅ `/prime <url>` - Scrape Prime Video details\n\n"
        "🚀 Running on Koyeb!"
    )

@client.on_message(filters.command("health"))
async def health(_, message: Message):
    await message.reply_text("✅ Bot is Alive & Healthy on Koyeb!")

@client.on_message(filters.command("prime"))
async def prime_scraper(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "⚠️ Please provide a Prime Video URL.\n\nExample:\n`/prime <prime-link>`"
        )

    prime_url = message.command[1]
    api_url = WORKER_URL + prime_url

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as resp:
                if resp.status != 200:
                    return await message.reply_text("❌ Error fetching from Worker API")

                data = await resp.json()

        # Format
        title = data.get("title", "N/A")
        year = data.get("year", "N/A")
        portrait = data.get("portrait")
        landscape = data.get("landscape")
        type_ = data.get("type", "N/A")

        caption = f"""
🎬 **{title}** ({year})
📺 Type: {type_.title()}

🖼 **Poster:** [Link]({portrait})
🖼 **Cover:** [Link]({landscape})
"""

        if portrait:
            await message.reply_photo(photo=portrait, caption=caption)
        else:
            await message.reply_text(caption)

    except Exception as e:
        await message.reply_text(f"⚠️ Error: `{e}`")
