from pyrogram import Client, filters
from pyrogram.types import Message
import aiohttp

# Your Cloudflare Worker API
WORKER_URL = "https://hub.botzs.workers.dev/"

@Client.on_message(filters.command(["hub", "hubcloud"]))
async def hubcloud_handler(client: Client, message: Message):
    # ------------------ Authorization Check ------------------
    OFFICIAL_GROUPS = ["-1002311378229"]
    if str(message.chat.id) not in OFFICIAL_GROUPS:
        await message.reply("❌ This command only works in our official group.")
        return
    # ---------------------------------------------------------

    if len(message.command) < 2:
        return await message.reply_text(
            "❌ Usage:\n`/hub <hubcloud_url>`\nor\n`/hubcloud <hubcloud_url1> <hubcloud_url2> ...`"
        )

    # Collect all links after the command
    raw_links = " ".join(message.command[1:])
    hubcloud_urls = [
        u.strip() for u in raw_links.replace("\n", " ").replace(",", " ").split() if u.strip()
    ]

    wait_msg = await message.reply_text("🔍 Fetching links...")

    try:
        async with aiohttp.ClientSession() as session:
            params = {"url": ",".join(hubcloud_urls)}
            async with session.get(WORKER_URL, params=params, timeout=60) as resp:
                data = await resp.json()

        files = data.get("files", [])

        if not files:
            return await wait_msg.edit_text("❌ No links found in response.")

        # Deduplicate by name + link
        seen = set()
        grouped = {}
        for f in files:
            key = f"{f.get('name', '')}"
            if key not in grouped:
                grouped[key] = []
            # avoid duplicate mirrors
            if f.get("link") not in [x["link"] for x in grouped[key]]:
                grouped[key].append(f)

        # Format the output
        text = "✅ **HubCloud Extracted Links:**\n\n"
        for movie, mirrors in grouped.items():
            # Movie name + first available size
            movie_name = mirrors[0].get("name", "Unknown File")
            movie_size = mirrors[0].get("size", "Unknown Size")
            text += f"🎬 **{movie_name}**\n💾 `{movie_size}`\n\n"

            # List mirrors under movie
            for f in mirrors:
                link = f.get("link", "")
                if "pixeldrain.dev" in link:
                    mirror = "🟢 **Pixeldrain**"
                elif "fastcloud.casa" in link:
                    mirror = "🔵 **FSL**"
                elif "hubcdn.fans" in link:
                    mirror = "🟣 **10GBs**"
                else:
                    mirror = "📁 **Mirror**"
                text += f"{mirror}\n🔗 [Download Link]({link})\n\n"

        await wait_msg.edit_text(text, disable_web_page_preview=True)

    except Exception as e:
        await wait_msg.edit_text(f"⚠️ Error:\n`{e}`")
