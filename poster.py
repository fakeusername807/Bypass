import aiohttp
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# ===== CONFIG =====
API_ID = 
API_HASH = "  "
BOT_TOKEN = "  "


# ===== BOT INSTANCE =====
client = Client("ott_scraper_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ===== INLINE BUTTON =====
update_button = InlineKeyboardMarkup(
    [[InlineKeyboardButton("😶‍🌫️ Updates", url ="https://t.me/hgbotz")]]
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
        image_url = data.get("poster") or data.get("landscape")

        if not title and not image_url:
            return await msg.edit_text("⚠️ No title or poster found for this URL.")

            #Don't Remove Credit @Hgbotz 

        text = (
            f"🎬 <b>{title}</b>\n\n"
            f"🖼️ Poster: {image_url}\n\n"

            "<b><blockquote>Powered By <a href='https://t.me/hgbotz'>𝙷𝙶𝙱𝙾𝚃ᶻ 🦋</a></blockquote></b>"
        )

        await msg.edit_text(
            text=text,
            disable_web_page_preview=False,
            reply_markup=update_button
        )

    except Exception as e:
        await msg.edit_text(f"❌ Error: {e}")


@client.on_message(filters.command("prime"))
async def prime_cmd(client, message: Message):
    if len(message.command) < 2:
        return await message.reply("🔗 Please provide a Prime OTT URL.\n\nExample:\n`/prime https://...`")

    ott_url = message.text.split(None, 1)[1].strip()
    api_url = f"https://primevideo.pbx1bots.workers.dev/?url={ott_url}"
    await handle_ott_command(message, api_url)
#Don't Remove Credit @Hgbotz 
# ===== RUN BOT =====
client.run()
