from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
import aiohttp
import re

# Your Cloudflare Worker API
WORKER_URL = "https://hub.botzs.workers.dev/"

@Client.on_message(filters.command(["hub", "hubcloud"]))
async def hubcloud_handler(client: Client, message: Message):
    # ------------------ Authorization Check ------------------
    OFFICIAL_GROUPS = ["-1002645306586"]  # replace with your group IDs
    if str(message.chat.id) not in OFFICIAL_GROUPS:
        await message.reply("❌ This command only works in our official group.")
        return
    # ---------------------------------------------------------

    hubcloud_urls = []

    # Case 1: Direct command with links
    if len(message.command) > 1:
        raw_links = " ".join(message.command[1:])
        hubcloud_urls.extend([u.strip() for u in raw_links.replace("\n", " ").replace(",", " ").split() if u.strip()])

    # Case 2: Reply to a message containing links
    if message.reply_to_message:
        reply_text = message.reply_to_message.text or message.reply_to_message.caption or ""
        found_links = re.findall(r"https?://hubcloud\.one/\S+", reply_text)
        hubcloud_urls.extend(found_links)

    if not hubcloud_urls:
        await message.reply_text(
            "❌ No HubCloud links found.\n\nUsage:\n`/hub <hubcloud_url>`\nor reply with `/hub` to a message containing HubCloud links."
        )
        return

    wait_msg = await message.reply_text("🔍 Fetching links...")

    try:
        async with aiohttp.ClientSession() as session:
            params = {"url": ",".join(hubcloud_urls)}
            async with session.get(WORKER_URL, params=params, timeout=90) as resp:
                data = await resp.json()

        # ✅ Worker now returns a list of results
        if isinstance(data, dict):
            results = [data]
        else:
            results = data

        if not results:
            await wait_msg.edit_text("❌ No links found in response.")
            return

        text = "✅ **HubCloud Extracted Links:**\n\n"

        for f in results:
            movie_name = f.get("movie", "Unknown File")
            movie_size = f.get("size", "Unknown Size")
            text += f"┎ 📚 <b>Title :-</b> `{movie_name}`\n\n┠ 💾 <b>Size :-</b> `{movie_size}`\n┃\n"

            if f.get("pixeldrain"):
                for link in f["pixeldrain"]:
                    text += f"┠ 🔗 <b>Pixeldrain :-</b> <a href='{link}'><b>Link</b></a>\n┃\n"
            if f.get("fsl"):
                for link in f["fsl"]:
                    text += f"┠ 🔗 <b>FSL Server :-</b> <a href='{link}'><b>Link</b></a>\n┃\n"
            if f.get("zipdisk"):
                for link in f["zipdisk"]:
                    text += f"┖ 🔗 <b>ZipDisk Server :-</b> <a href='{link}'><b>Link</b></a>\n\n<b>━━━━━━━✦✗✦━━━━━━━</b>\n\n"

        # ✅ Requested By (only once, after loop)
        if message.from_user:
            text += f"<b>Requested By :-</b> {message.from_user.mention}\n<b>(#ID_{message.from_user.id})</b>\n\n"

        # ✅ Add button
        await wait_msg.edit_text(
            text,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("📢 Uᴘᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ", url="https://t.me/MrSagarBots")]
                ]
            )
        )


    except Exception as e:
        await wait_msg.edit_text(f"⚠️ Error:\n`{e}`")
