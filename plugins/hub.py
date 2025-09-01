from pyrogram import Client, filters
from pyrogram.types import Message
import aiohttp

WORKER_URL = "https://hub.botzs.workers.dev/"

@Client.on_message(filters.command(["hub", "hubcloud"]))
async def hubcloud_handler(client: Client, message: Message):
    OFFICIAL_GROUPS = ["-1002311378229"]

    if str(message.chat.id) not in OFFICIAL_GROUPS:
        await message.reply("❌ This command only works in our official group.")
        return

    if len(message.command) < 2:
        await message.reply_text(
            "❌ Usage:\n`/hub <hubcloud_url>`\nor\n`/hubcloud <hubcloud_url1> <hubcloud_url2> ...`"
        )
        return

    raw_links = " ".join(message.command[1:])
    hubcloud_urls = [u.strip() for u in raw_links.replace("\n", " ").replace(",", " ").split() if u.strip()]

    wait_msg = await message.reply_text("🔍 Fetching links...")

    try:
        async with aiohttp.ClientSession() as session:
            params = {"url": ",".join(hubcloud_urls)}
            async with session.get(WORKER_URL, params=params, timeout=60) as resp:
                data = await resp.json()

        files = data.get("files", [])
        if not files:
            await wait_msg.edit_text("❌ No links found in response.")
            return

        # Group mirrors by movie name
        movies = {}
        for f in files:
            name = f.get("name", "Unknown File")
            size = f.get("size", "Unknown Size")
            link = f.get("link", "")
            if name not in movies:
                movies[name] = {"size": size, "mirrors": {}}

            if "pixeldrain.dev" in link:
                mirror = "🟢 Pixeldrain"
            elif "fastcloud.casa" in link:
                mirror = "🔵 FSL"
            elif "hubcdn.fans" in link:
                mirror = "🟣 10GBs"
            else:
                mirror = "📁 Mirror"

            # Deduplicate mirror links
            if mirror not in movies[name]["mirrors"]:
                movies[name]["mirrors"][mirror] = link

        # Build final text
        text = "✅ **HubCloud Extracted Links:**\n\n"
        for movie_name, info in movies.items():
            text += f"🎬 {movie_name}\n💾 {info['size']}\n\n"
            for mirror, link in info["mirrors"].items():
                text += f"{mirror}\n🔗 [Download Link]({link})\n\n"

        await wait_msg.edit_text(text, disable_web_page_preview=True)

    except Exception as e:
        await wait_msg.edit_text(f"⚠️ Error:\n`{e}`")
