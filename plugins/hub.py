from pyrogram import Client, filters
from pyrogram.types import Message
import aiohttp

# Your Cloudflare Worker API
WORKER_URL = "https://hub.botzs.workers.dev/"

@Client.on_message(filters.command(["hub", "hubcloud"]))
async def hubcloud_handler(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text(
            "❌ Usage:\n`/hub <hubcloud_url>`\nor\n`/hubcloud <hubcloud_url>`"
        )
        return

    hubcloud_url = message.command[1].strip()
    await message.reply_text("🔍 Fetching Pixeldrain link...")

    try:
        async with aiohttp.ClientSession() as session:
            params = {"url": hubcloud_url}
            async with session.get(WORKER_URL, params=params, timeout=20) as resp:
                data = await resp.json()

        pixeldrain_link = data.get("pixeldrain")
        if pixeldrain_link:
            await message.reply_text(f"✅ **Pixeldrain link:**\n{pixeldrain_link}")
        else:
            await message.reply_text("❌ Pixeldrain link not found in response.")
    except Exception as e:
        await message.reply_text(f"⚠️ Error:\n`{e}`")
