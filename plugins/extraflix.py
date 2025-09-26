from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
import aiohttp

API_URL = "https://hgbots.vercel.app/bypaas/extraflix.php?url="
DUMP_CHANNEL_ID = "-1002673922646"  # your dump channel ID

def to_list(x):
    """Ensure the API field is always a list"""
    if not x:
        return []
    if isinstance(x, list):
        return x
    return [x]

@Client.on_message(filters.command(["extraflix"]))
async def extraflix_scraper(client: Client, message: Message):
    # ------------------ Authorization Check ------------------
    OFFICIAL_GROUPS = [
        "-1002645306586",
        "-4806226644",
        "-1002998120105",
    ]
    if str(message.chat.id) not in OFFICIAL_GROUPS:
        await message.reply(
            "❌ This command only works in group.\nContact @MrSagar_RoBot For Group Link"
        )
        return
    # ---------------------------------------------------------

    if len(message.command) == 1:
        return await message.reply_text(
            "⚠️ Usage: `/extraflix <extraflix_url>`",
            disable_web_page_preview=True
        )

    extra_url = message.command[1]
    wait_msg = await message.reply_text("🔍 Fetching Extraflix links...")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL + extra_url, timeout=90) as resp:
                if resp.status != 200:
                    await wait_msg.edit_text("❌ Failed to fetch data from API.")
                    return
                data = await resp.json()

        # Normalize response (dict or list)
        results = [data] if isinstance(data, dict) else data

        text = "✅ **Extraflix Extracted Links:**\n\n"

        for idx, f in enumerate(results, start=1):
            title = f.get("title", "Unknown Title")
            size = f.get("size", "Unknown Size")

            text += f"┎ 📚 <b>Title {idx} :-</b>\n`{title}`\n\n"
            text += f"┠ 💾 <b>Size :-</b> `{size}`\n┃\n"

            for link in to_list(f.get("gdtot")):
                text += f"┠ 🔗 <b>GDTOT :-</b> <a href='{link}'>Link</a>\n┃\n"

            for link in to_list(f.get("vikings")):
                text += f"┠ 🔗 <b>Vikings :-</b> <a href='{link}'>Link</a>\n┃\n"

            for link in to_list(f.get("pixeldrain")):
                text += f"┠ 🔗 <b>Pixeldrain :-</b> <a href='{link}'>Link</a>\n┃\n"

            for link in to_list(f.get("others")):
                text += f"┖ 🔗 <b>Mirror :-</b> <a href='{link}'>Link</a>\n\n"

            text += "<b>━━━━━━━✦✗✦━━━━━━━</b>\n\n"

        # Requested By (once at bottom)
        if message.from_user:
            text += f"<b>🙋 Requested By :-</b> {message.from_user.mention}\n<b>(#ID_{message.from_user.id})</b>\n\n"

        update_button = InlineKeyboardMarkup(
            [[InlineKeyboardButton("📢 Uᴘᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ", url="https://t.me/MrSagarBots")]]
        )

        # Reply in chat
        await wait_msg.edit_text(
            text,
            disable_web_page_preview=True,
            reply_markup=update_button
        )

        # Send to dump channel
        await client.send_message(
            DUMP_CHANNEL_ID,
            f"📦 [Extraflix]\n\n{text}",
            disable_web_page_preview=True,
            reply_markup=update_button
        )

    except Exception as e:
        await wait_msg.edit_text(f"⚠️ Error:\n`{e}`")
