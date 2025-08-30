from pyrogram import filters
from pyrogram.types import Message
import aiohttp

WORKER_URL = "https://hub.botzs.workers.dev/"

# This will be automatically registered by your main Client
@filters.command("hub") & filters.private
async def hubcloud_handler(client, message: Message):
    args = message.text.split()
    if len(args) < 2:
        await message.reply_text("Usage: /hub <Hubcloud URL>")
        return

    hubcloud_url = args[1].strip()
    await message.reply_text("🔍 Fetching Pixeldrain link...")

    try:
        async with aiohttp.ClientSession() as session:
            params = {"url": hubcloud_url}
            async with session.get(WORKER_URL, params=params, timeout=20) as resp:
                data = await resp.json()

        pixeldrain_link = data.get("pixeldrain")
        if pixeldrain_link:
            await message.reply_text(f"✅ Pixeldrain link:\n{pixeldrain_link}")
        else:
            await message.reply_text("❌ Pixeldrain link not found.")
    except Exception as e:
        await message.reply_text(f"⚠️ Error: {e}")
