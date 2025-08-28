import aiohttp
from aiohttp import web
from pyrogram import Client, filters, idle
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
        year = data.get("year") or ""
        portrait = data.get("portrait")
        landscape = data.get("landscape")

        # Build caption
        caption = f"🎬 <b>{title}</b>"
        if year:
            caption += f" - ({year})"
        caption += "\n\n⚡ Powered By <a href='https://t.me/hgbotz'>𝙷𝙶𝙱𝙾𝚃ᶻ 🦋</a>"

        # Inline buttons
        buttons = [
            [InlineKeyboardButton("🖼️ Cover", url=landscape or portrait or "https://t.me/hgbotz")],
            [InlineKeyboardButton("📱 Portrait", url=portrait or landscape or "https://t.me/hgbotz")],
            [InlineKeyboardButton("😶‍🌫️ Updates", url="https://t.me/hgbotz")],
        ]

        if landscape:
            await msg.delete()
            await message.reply_photo(
                photo=landscape,
                caption=caption,
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        elif portrait:
            await msg.delete()
            await message.reply_photo(
                photo=portrait,
                caption=caption,
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        else:
            await msg.edit_text("⚠️ No poster image found.")

    except Exception as e:
        await msg.edit_text(f"❌ Error: {e}")


@client.on_message(filters.command("prime"))
async def prime_cmd(client, message: Message):
    if len(message.command) < 2:
        return await message.reply("🔗 Please provide a Prime OTT URL.\n\nExample:\n`/prime https://...`")

    ott_url = message.text.split(None, 1)[1].strip()
    api_url = f"https://adda.botzs.workers.dev/?url={ott_url}"
    await handle_ott_command(message, api_url)


# ===== HEALTH CHECK SERVER =====
async def health_check(request):
    return web.Response(text="OK", status=200)

async def start_web_app():
    app = web.Application()
    app.add_routes([web.get("/health", health_check)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()


# ===== MAIN ENTRYPOINT =====
async def main():
    await asyncio.gather(
        client.start(),
        start_web_app()
    )
    await idle()

if __name__ == "__main__":
    asyncio.run(main())
