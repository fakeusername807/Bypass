import aiohttp
from aiohttp import web
from configs import *
from pyrogram import Client, filters, idle
from pyrogram.types import Message
import asyncio
import pyrogram

# ===== BOT INSTANCE =====
client = Client(
    "ott_scraper_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ===== HEALTH CHECK =====
async def health_handler(request):
    return web.Response(text="ok")

async def start_webserver():
    app = web.Application()
    app.router.add_get("/", health_handler)  # Koyeb health ping
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()
    print("🌐 Health check server running on port 8080")

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

# ===== STARTUP =====
async def startup_message():
    try:
        await client.send_message(OWNER_ID, "🚀 Bot is Ready and Running on Koyeb!")
    except Exception as e:
        print(f"Could not send startup message: {e}")

async def main():
    await client.start()
    await startup_message()
    await start_webserver()
    print("✅ Bot is fully started and waiting for commands...")
    await idle()  # keep bot running

print("🚀 Bot Starting...")
asyncio.run(main())
