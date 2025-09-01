from pyrogram import Client, filters
from pyrogram.types import Message
import aiohttp

# Your Cloudflare Worker API
WORKER_URL = "https://hub.botzs.workers.dev/"

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
            "❌ Usage:\n`/hub <hubcloud_url>`\nor\n`/hubcloud <hubcloud_url1> <hubcloud_url2> ...`"
        )
        return

    # Collect all links after the command (space, comma, newline separated)
    raw_links = " ".join(message.command[1:])
    hubcloud_urls = [u.strip() for u in raw_links.replace("\n", " ").replace(",", " ").split() if u.strip()]

    wait_msg = await message.reply_text("🔍 Fetching links...")

    try:
        async with aiohttp.ClientSession() as session:
            params = {"url": ",".join(hubcloud_urls)}
            async with session.get(WORKER_URL, params=params, timeout=90) as resp:
                data = await resp.json()

        files = data.get("files", [])

        if not files:
            await wait_msg.edit_text("❌ No links found in response.")
            return

        text = "✅ **HubCloud Extracted Links:**\n\n"

        for f in files:
            movie_name = f.get("name", "Unknown File")
            movie_size = f.get("size", "Unknown Size")
            text += f"🎬 {movie_name}\n💾 {movie_size}\n\n"

            if f.get("pixeldrain"):
                text += f"🟢 Pixeldrain\n🔗 [Download Link]({f['pixeldrain']})\n\n"
            if f.get("fsl"):
                text += f"🔵 FSL\n🔗 [Download Link]({f['fsl']})\n\n"
            # ✅ Added 10GBs support
            if f.get("10gbs"):
                text += f"🟣 10GBs\n🔗 [Download Link]({f['10gbs']})\n\n"

        await wait_msg.edit_text(text, disable_web_page_preview=True)

    except Exception as e:
        await wait_msg.edit_text(f"⚠️ Error:\n`{e}`")
