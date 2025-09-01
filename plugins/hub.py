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

    # Collect all links after the command (space, comma, newline separated)
    raw_links = " ".join(message.command[1:])
    hubcloud_urls = [u.strip() for u in raw_links.replace("\n", " ").replace(",", " ").split() if u.strip()]

    wait_msg = await message.reply_text("🔍 Fetching links...")

    try:
        async with aiohttp.ClientSession() as session:
            # Send multiple URLs joined with commas
            params = {"url": ",".join(hubcloud_urls)}
            async with session.get(WORKER_URL, params=params, timeout=90) as resp:
                data = await resp.json()

        files = data.get("files", [])

        if not files:
            await wait_msg.edit_text("❌ No links found in response.")
            return

        # Deduplicate by link
        seen_links = set()
        unique_files = []
        for f in files:
            link = f.get("link")
            if link not in seen_links:
                seen_links.add(link)
                unique_files.append(f)

        # Group mirrors under each movie
        grouped = {}
        for f in unique_files:
            name = f.get("name", "Unknown File")
            size = f.get("size", "Unknown Size")
            link = f.get("link", "")

            # Determine mirror type
            if "pixeldrain.dev" in link:
                mirror_type = "🟢 Pixeldrain"
            elif "fastcloud.casa" in link:
                mirror_type = "🔵 FSL"
            elif "hubcdn.fans" in link:
                mirror_type = "🟣 10GBs"
            else:
                mirror_type = "📁 Mirror"

            if name not in grouped:
                grouped[name] = {"size": size, "mirrors": []}
            grouped[name]["mirrors"].append({"type": mirror_type, "link": link})

        # Build final message
        text = "✅ **HubCloud Extracted Links:**\n\n"
        for movie_name, info in grouped.items():
            text += f"🎬 {movie_name}\n💾 {info['size']}\n\n"
            for mirror in info["mirrors"]:
                text += f"{mirror['type']}\n🔗 [Download Link]({mirror['link']})\n\n"

        await wait_msg.edit_text(text, disable_web_page_preview=True)

    except Exception as e:
        await wait_msg.edit_text(f"⚠️ Error:\n`{e}`")
