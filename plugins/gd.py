from pyrogram import Client, filters
from pyrogram.types import Message
import aiohttp

WORKER_URL = "https://gdflix.botzs.workers.dev/?url="

# ===== GD / GDFLIX COMMAND =====
@Client.on_message(filters.command(["gd", "gdflix"]))
async def gd_scraper(_, message: Message):
    # ------------------ Authorization Check ------------------
    OFFICIAL_GROUPS = ["-1002645306586"]

    if str(message.chat.id) not in OFFICIAL_GROUPS:
        await message.reply("❌ This command only works in our official group.")
        return
    # ---------------------------------------------------------

    # Validate links
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

                # Handle gofile (could be a list or string)
                gofile_links = links_data.get("gofile", [])
                if isinstance(gofile_links, str):
                    gofile_text = f"[Click Here]({gofile_links})"
                elif isinstance(gofile_links, list) and gofile_links:
                    gofile_text = "\n".join(
                        f"[Mirror {i+1}]({u})" for i, u in enumerate(gofile_links)
                    )
                else:
                    gofile_text = "Not Found"

                final_output += f"""
┎ 📚 <b>Title :-</b> {idx}
`{title}`

┠ 💾 <b>Size :- `{size}`
┃
┠  ⚡ INSTANT DL : [Click Here]({links_data.get('instantdl','')})
┃
┠  ☁️ CLOUD DOWNLOAD : [Click Here]({links_data.get('clouddl','')})
┃
┠  📩 TELEGRAM FILE : [Click Here]({links_data.get('telegram','')})
┃
┠  🗂 GOFILE : {gofile_text}
┃
┠  📥 PIXELDRAIN : [Click Here]({links_data.get('pixeldrain','')})
┃
┠  🤖 DRIVEBOT : [Click Here]({links_data.get('drivebot','')})
┃
┖  ⚡ INSTANTBOT : [Click Here]({links_data.get('instantbot','')})

<b>━━━━━━━✦✗✦━━━━━━━</b>

<b>Requested By :-</b> <b>{message.from_user.mention}</b>
<b>(#ID_{message.from_user.id})</b>
"""

        final_output += "\n⚡ Powered By @MrSagarBots 🚀"
        await message.reply_text(final_output, disable_web_page_preview=True)

    except Exception as e:
        await message.reply_text(f"⚠️ Error: `{e}`")
