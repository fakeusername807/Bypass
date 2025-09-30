from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
import aiohttp, asyncio

API_URL = "https://hgbots.vercel.app/bypaas/extraflix.php?url="
DUMP_CHANNEL_ID = "-1002673922646"

async def show_progress(msg):
    for i in range(0, 101, 20):
        bar = "■" * (i // 10) + "□" * (10 - i // 10)
        await msg.edit_text(f"[{bar}] {i}%")
        await asyncio.sleep(0.5)

@Client.on_message(filters.command(["extraflix"]))
async def extraflix_scraper(client: Client, message: Message):
    OFFICIAL_GROUPS = ["-1002645306586","-4806226644","-1002998120105"]
    if str(message.chat.id) not in OFFICIAL_GROUPS:
        await message.reply("❌ This command only works in group.\nContact @MrSagar_RoBot For Group Link")
        return

    if len(message.command) == 1:
        return await message.reply_text("⚠️ Usage: `/extraflix <extraflix_url>`", disable_web_page_preview=True)

    extra_url = message.command[1]
    wait_msg = await message.reply_text("[□□□□□□□□□□] 0%")
    asyncio.create_task(show_progress(wait_msg))

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL + extra_url, timeout=90) as resp:
                if resp.status != 200:
                    await wait_msg.edit_text("❌ Failed to fetch data from API.")
                    return
                data = await resp.json()

        results = [data] if isinstance(data, dict) else data
        text = "✅ **Extraflix Extracted Links:**\n\n"

        for f in results:
            movie_name = f.get("fileName", "Unknown File")
            links = f.get("links", {})
            text += f"┎ 📚 Title :- `{movie_name}`\n\n"
            if links.get("gdtotLink"):
                text += f"┠ 🔗 <b>GDToT :-</b> <a href='{links['gdtotLink']}'>Link</a>\n┃\n"
            if links.get("vidhideLink"):
                text += f"┠ 🔗 <b>VidHide :-</b> <a href='{links['vidhideLink']}'>Link</a>\n┃\n"
            if links.get("pixeldrainLink"):
                text += f"┠ 🔗 <b>PixelDrain :-</b> <a href='{links['pixeldrainLink']}'>Link</a>\n┃\n"
            if links.get("vikingLink"):
                text += f"┖ 🔗 <b>Viking :-</b> <a href='{links['vikingLink']}'>Link</a>\n\n"
            text += "<b>━━━━━━━✦✗✦━━━━━━━</b>\n\n"

        if message.from_user:
            text += f"<b>🙋 Requested By :-</b> {message.from_user.mention}\n<b>(#ID_{message.from_user.id})</b>\n\n"

        update_button = InlineKeyboardMarkup(
            [[InlineKeyboardButton("📢 Uᴘᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ", url="https://t.me/MrSagarBots")]]
        )

        await wait_msg.edit_text(text, disable_web_page_preview=True, reply_markup=update_button)
        await client.send_message(DUMP_CHANNEL_ID, f"📦 [Extraflix]\n\n{text}", disable_web_page_preview=True, reply_markup=update_button)

    except Exception as e:
        await wait_msg.edit_text(f"⚠️ Error:\n`{e}`")
