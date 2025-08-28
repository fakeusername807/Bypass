import aiohttp
from pyrogram import Client, filters
from pyrogram.types import Message

# ===== CONFIG =====
API_ID = "7041911"  # your API_ID
API_HASH = "abab2561c71e3004a55d4ff9763d5383"
BOT_TOKEN = ""

# Cloudflare Worker endpoint
WORKER_URL = "https://adda.botzs.workers.dev/?url="

# ===== BOT INSTANCE =====
client = Client(
    "ott_scraper_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ===== KOYEB HEALTH CHECK =====
@client.on_message(filters.command("health"))
async def health(_, message: Message):
    await message.reply_text("✅ Bot is Alive & Healthy on Koyeb!")

# ===== PRIME VIDEO SCRAPER =====
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

        # Format message
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

        # Send with poster if available
        if portrait:
            await message.reply_photo(photo=portrait, caption=caption)
        else:
            await message.reply_text(caption)

    except Exception as e:
        await message.reply_text(f"⚠️ Error: `{e}`")

# ===== START BOT =====
print("🚀 Bot Started...")
client.run()
