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
