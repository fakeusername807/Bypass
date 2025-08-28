import aiohttp
from aiohttp import web
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

# ===== CONFIG =====
API_ID = "7041911"
API_HASH = "abab2561c71e3004a55d4ff9763d5383"
BOT_TOKEN = ""

# ===== BOT INSTANCE =====
client = Client("ott_scraper_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ===== INLINE BUTTON =====
update_button = InlineKeyboardMarkup(
    [[InlineKeyboardButton("😶‍🌫️ Updates", url="https://t.me/hgbotz")]]
)

# ===== COMMON FUNCTION =====
async def fetch_ott_data(api_url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as resp:
            if resp.status != 200:
                return None
            return await resp.json()

async def handle_ott_command(message: Message, api_url: str):
    msg = await message.reply("🔍 Fetching...")
    try:
        data = await fetch_ott_data(api_url)
        if not data:
            return await msg.edit_text("❌ Failed to fetch data from API.")

        title = data.get("title") or "No Title"
        year = data.get("year") or "Unknown Year"
        poster = data.get("portrait") or "No poster"
        cover = data.get("landscape") or "No cover"

        text = (
            f"🎬 <b>{title} - ({year})</b>\n\n"
            f"🖼️ <b>Amazon Prime Poster:</b> {poster}\n"
            f"🖼️ <b>Cover:</b> {cover}\n"
            f"🖼️ <b>Portrait:</b> {poster}\n\n"
            "<b><blockquote>Powered By <a href='https://t.me/hgbotz'>𝙷𝙶𝙱𝙾𝚃ᶻ 🦋</a></blockquote></b>"
        )

        await msg.edit_text(
            text=text,
            disable_web_page_preview=False,
            reply_markup=update_button
        )

    except Exception as e:
        await msg.edit_text(f"❌ Error: {e}")

# ===== COMMAND =====
@client.on_message(filters.command("prime"))
async def prime_cmd(client, message: Message):
    if len(message.command) < 2:
        return await message.reply("🔗 Please provide a Prime OTT URL.\n\nExample:\n`/prime https://...`")

    ott_url = message.text.split(None, 1)[1].strip()
    api_url = f"https://adda.botzs.workers.dev/?url={ott_url}"
    await handle_ott_command(message, api_url)

# ===== HEALTH CHECK SERVER =====
async def health(request):
    return web.Response(text="OK")

async def run_health_server():
    app = web.Application()
    app.router.add_get("/health", health)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()

# ===== RUN BOTH BOT + SERVER =====
async def main():
    # Run health server in background
    asyncio.create_task(run_health_server())
    # Run telegram bot
    await client.start()
    print("Bot is running with health check ✅")
    await idle()  # keeps process alive

if __name__ == "__main__":
    from pyrogram import idle
    asyncio.run(main())
