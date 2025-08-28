import aiohttp
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

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
    msg = await message.reply("🔍 Fetching from Cloudflare Worker...")
    try:
        data = await fetch_ott_data(api_url)
        if not data:
            return await msg.edit_text("❌ Failed to fetch data from API.")

        title = data.get("title") or "No Title"
        year = data.get("year") or "N/A"
        poster = data.get("portrait")
        cover = data.get("landscape")

        if not title and not poster:
            return await msg.edit_text("⚠️ No title or poster found for this URL.")

        # final formatted text
        text = (
            f"🎬 <b>Amazon Prime Poster:</b> {poster}\n\n"
            f"🖼️ <b>Cover:</b> {cover}\n"
            f"🖼️ <b>Portrait:</b> {poster}\n\n"
            f"📌 <b>{title} - ({year})</b>\n\n"
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
        return await message.reply(
            "🔗 Please provide a Prime OTT URL.\n\nExample:\n`/prime https://www.primevideo.com/detail/...`"
        )

    ott_url = message.text.split(None, 1)[1].strip()
    # 🔥 now bot calls your Cloudflare worker
    api_url = f"https://adda.botzs.workers.dev/?url={ott_url}"
    await handle_ott_command(message, api_url)

# ===== RUN BOT =====
client.run()
