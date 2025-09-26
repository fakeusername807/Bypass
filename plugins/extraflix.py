from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
import aiohttp

API_URL = "https://hgbots.vercel.app/bypaas/extraflix.php?url="
DUMP_CHANNEL_ID = "-1002673922646"

@Client.on_message(filters.command(["extraflix"]))
async def extraflix_scraper(client: Client, message: Message):
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

        text = "✅ Extraflix Extracted Links:\n\n"

        update_button = InlineKeyboardMarkup(
            [[InlineKeyboardButton("📢 Uᴘᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ", url="https://t.me/MrSagarBots")]]
        )

        for f in data:
            movie_name = f.get("fileName", "Unknown File")
            links = f.get("links", {})

            text += f"┎ 📚 Title :- `{movie_name}`\n\n"

            gdtot = links.get("gdtotLink")
            vidhide = links.get("vidhideLink")
            pixeldrain = links.get("pixeldrainLink")
            viking = links.get("vikingLink")

            if gdtot:
                text += f"┠ 🔗 <b>GDToT</b> :- <a href='{gdtot}'><b>Link</b></a>\n┃\n"
            if vidhide:
                text += f"┠ 🔗 <b>VidHide</b> :- <a href='{vidhide}'><b>Link</b></a>\n┃\n"
            if pixeldrain:
                text += f"┠ 🔗 <b>PixelDrain</b> :- <a href='{pixeldrain}'><b>Link</b></a>\n┃\n"
            if viking:
                text += f"┖ 🔗 <b>Viking</b> :- <a href='{viking}'><b>Link</b></a>\n\n"

            text += "<b>━━━━━━━✦✗✦━━━━━━━</b>\n\n"

        if message.from_user:
            text += f"<b>🙋 Requested By :-</b> <b>{message.from_user.mention}</b>\n<b>(#ID_{message.from_user.id})</b>\n\n"

        # Reply in chat
        await wait_msg.edit_text(
            text,
            disable_web_page_preview=True,
            reply_markup=update_button
        )

        # Send to dump channel
        await client.send_message(
            DUMP_CHANNEL_ID,
            text,
            disable_web_page_preview=True,
            reply_markup=update_button
        )

    except Exception as e:
        await wait_msg.edit_text(f"⚠️ Error:\n`{e}`")
