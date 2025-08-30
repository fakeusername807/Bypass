from pyrogram import Client, filters
from pyrogram.types import Message
import aiohttp
import json

WORKER_URL = "https://gdflix.botzs.workers.dev/?url="

# ===== GD / GDFLIX COMMAND =====
@Client.on_message(filters.command(["gd", "gdflix"]))
async def gd_scraper(_, message: Message):
    if len(message.command) == 1:
        return await message.reply_text(
            "⚠️ Usage: `/gd <gdlink1> <gdlink2> ... (upto 5)`",
            disable_web_page_preview=True
        )

    links = message.command[1:]  # all links after command
    if len(links) > 5:
        return await message.reply_text("⚠️ You can only send up to 5 links at once!")

    final_output = ""

    try:
        async with aiohttp.ClientSession() as session:
            for idx, link in enumerate(links, start=1):
                if not link.startswith("http"):
                    final_output += f"\n❌ Link {idx} is invalid: {link}\n"
                    continue

                async with session.get(WORKER_URL + link) as resp:
                    if resp.status != 200:
                        final_output += f"\n❌ Error fetching Link {idx}: {link}\n"
                        continue
                    data = await resp.json()

                title = data.get("title", "Unknown Title")
                size = data.get("size", "Unknown Size")
                links_data = data.get("links", {})

                final_output += f"""
📁 𝚃𝚒𝚝𝚕𝚎 {idx}
{title}
📦 𝚂𝚒𝚣𝚎 :- {size}

⚡ INSTANT DL : [Click Here]({links_data.get('instantdl','')})
☁️ CLOUD DOWNLOAD : [Click Here]({links_data.get('clouddl','')})
📩 TELEGRAM FILE : [Click Here]({links_data.get('telegram','')})
🗂 GOFILE : [Click Here]({links_data.get('gofile','')})

━━━━━━━━━━━━━━━━━━
"""

        final_output += "\n⚡ Powered By @AddaFiles 🚀"
        await message.reply_text(final_output, disable_web_page_preview=True)

    except Exception as e:
        await message.reply_text(f"⚠️ Error: `{e}`")
