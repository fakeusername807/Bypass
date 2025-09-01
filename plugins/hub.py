from pyrogram import Client, filters
from pyrogram.types import Message
import aiohttp

# Your Cloudflare Worker API
WORKER_URL = "https://hub.botzs.workers.dev/"

# ===== HubCloud / Pixeldrain / FSL / 10GBs COMMAND =====
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

    # Collect all links after the command (can be space, comma, or newline separated)
    raw_links = " ".join(message.command[1:])
    hubcloud_urls = [u.strip() for u in raw_links.replace("\n", " ").replace(",", " ").split() if u.strip()]

    wait_msg = await message.reply_text("🔍 Fetching links...")

    try:
        async with aiohttp.ClientSession() as session:
            # Send multiple URLs joined with commas
            params = {"url": ",".join(hubcloud_urls)}
            async with session.get(WORKER_URL, params=params, timeout=60) as resp:
                data = await resp.json()

        files = data.get("files", [])

        if not files:
            await wait_msg.edit_text("❌ No links found in response.")
            return

        # Deduplicate links (avoid repeated mirrors)
        seen = set()
        unique_files = []
        for f in files:
            link = f.get("link")
            if link not in seen:
                seen.add(link)
                unique_files.append(f)

        # Format and send each file info
        text = "✅ **HubCloud Extracted Links:**\n\n"
        for f in unique_files:
            name = f.get("name", "Unknown File")
            size = f.get("size", "Unknown Size")
            link = f.get("link", "")

            # Detect mirror type
            if "pixeldrain.dev" in link:
                mirror = "🟢 **Pixeldrain**"
            elif "fastcloud.casa" in link:
                mirror = "🔵 **FSL**"
            elif "hubcdn.fans" in link:
                mirror = "🟣 **10GBs**"
            else:
                mirror = "📁 **Mirror**"

            text += f"{mirror}\n🎬 **{name}**\n💾 `{size}`\n🔗 [Download Link]({link})\n\n"

        await wait_msg.edit_text(text, disable_web_page_preview=True)

    except Exception as e:
        await wait_msg.edit_text(f"⚠️ Error:\n`{e}`")
