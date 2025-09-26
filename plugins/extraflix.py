from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
import aiohttp

# API URL template
API_URL = "https://hgbots.vercel.app/bypaas/extraflix.php?url="
DUMP_CHANNEL_ID = "-1002673922646"  # 🔹 your dump channel ID

@Client.on_message(filters.command(["extraflix"]))
async def extraflix_scraper(client: Client, message: Message):
    # ------------------ Authorization Check ------------------
    OFFICIAL_GROUPS = [
        "-1002645306586",
        "-4806226644",
        "-1002998120105",
    ]
    if str(message.chat.id) not in OFFICIAL_GROUPS:
        await message.reply("❌ This command only works in group.\nContact @MrSagar_RoBot For Group Link")
        return
    # ---------------------------------------------------------

    # Validate command
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

        # Start formatting
        text = "✅ **Extraflix Extracted Links:**\n\n"

        title = data.get("title", "Unknown Title")
        size = data.get("size", "Unknown Size")

        text += f"┎ 📚 <b>Title :-</b>\n`{title}`\n\n"
        text += f"┠ 💾 <b>Size :-</b> `{size}`\n┃\n"

        # gdtot links
        if data.get("gdtot"):
            for link in data["gdtot"]:
                text += f"┠ 🔗 <b>GDTOT :-</b> <a href='{link}'>Link</a>\n┃\n"

        # vikings links
        if data.get("vikings"):
            for link in data["vikings"]:
                text += f"┠ 🔗 <b>Vikings :-</b> <a href='{link}'>Link</a>\n┃\n"

        # pixeldrain links
        if data.get("pixeldrain"):
            for link in data["pixeldrain"]:
                text += f"┠ 🔗 <b>Pixeldrain :-</b> <a href='{link}'>Link</a>\n┃\n"

        # other links
        if data.get("others"):
            for link in data["others"]:
                text += f"┖ 🔗 <b>Mirror :-</b> <a href='{link}'>Link</a>\n\n"

        text += "<b>━━━━━━━✦✗✦━━━━━━━</b>\n\n"

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

        # Send to dump channel with prefix
        await client.send_message(
            DUMP_CHANNEL_ID,
            f"📦 [Extraflix]\n\n{text}",
            disable_web_page_preview=True,
            reply_markup=update_button
        )

    except Exception as e:
        await wait_msg.edit_text(f"⚠️ Error:\n`{e}`")
