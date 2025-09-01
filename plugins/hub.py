from pyrogram import Client, filters
from pyrogram.types import Message
import aiohttp

# Your Cloudflare Worker API
WORKER_URL = "https://hub.botzs.workers.dev/"

# ===== HubCloud / Pixeldrain COMMAND =====
@Client.on_message(filters.command(["hub", "hubcloud"]))
async def hubcloud_handler(client: Client, message: Message):
    # ------------------ Authorization Check ------------------
    OFFICIAL_GROUPS = ["-1002311378229"]  # replace with your group IDs

    if str(message.chat.id) not in OFFICIAL_GROUPS:
        await message.reply("❌ This command only works in our official group.")
        return
    # ---------------------------------------------------------

    if len(message.command) < 2:
        await message.reply_text(
            "❌ Usage:\n`/hub <hubcloud_url>`\nor\n`/hubcloud <hubcloud_url>`"
        )
        return

    hubcloud_url = message.command[1].strip()
    wait_msg = await message.reply_text("🔍 Fetching Pixeldrain links...")

    try:
        async with aiohttp.ClientSession() as session:
            params = {"url": hubcloud_url}
            async with session.get(WORKER_URL, params=params, timeout=40) as resp:
                data = await resp.json()

        files = data.get("files", [])

        if not files:
            await wait_msg.edit_text("❌ No Pixeldrain links found in response.")
            return

        # Format and send each file info
        text = "✅ **Pixeldrain Results:**\n\n"
        for f in files:
            name = f.get("name", "Unknown File")
            size = f.get("size", "Unknown Size")
            link = f.get("link", "")
            text += f"🎬 **{name}**\n💾 `{size}`\n🔗 [Download Link]({link})\n\n"

        await wait_msg.edit_text(text, disable_web_page_preview=True)

    except Exception as e:
        await wait_msg.edit_text(f"⚠️ Error:\n`{e}`")
