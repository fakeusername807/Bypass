from pyrogram import Client, filters
from pyrogram.types import Message
import aiohttp
import re

# Your Cloudflare Worker API
WORKER_URL = "https://hub.botzs.workers.dev/"

@Client.on_message(filters.command(["hub", "hubcloud"]))
async def hubcloud_handler(client: Client, message: Message):
    # ------------------ Authorization Check ------------------
    OFFICIAL_GROUPS = ["-1002645306586"]  # replace with your group IDs
    if str(message.chat.id) not in OFFICIAL_GROUPS:
        await message.reply("❌ This command only works in our official group.")
        return
    # ---------------------------------------------------------

    hubcloud_urls = []

    # Case 1: Direct command with links
    if len(message.command) > 1:
        raw_links = " ".join(message.command[1:])
        hubcloud_urls.extend([u.strip() for u in raw_links.replace("\n", " ").replace(",", " ").split() if u.strip()])

    # Case 2: Reply to a message containing links
    if message.reply_to_message:
        reply_text = message.reply_to_message.text or message.reply_to_message.caption or ""
        found_links = re.findall(r"https?://hubcloud\.one/\S+", reply_text)
        hubcloud_urls.extend(found_links)

    if not hubcloud_urls:
        await message.reply_text(
            "❌ No HubCloud links found.\n\nUsage:\n`/hub <hubcloud_url>`\nor reply with `/hub` to a message containing HubCloud links."
        )
        return

    wait_msg = await message.reply_text("🔍 Fetching links...")

    try:
        async with aiohttp.ClientSession() as session:
            params = {"url": ",".join(hubcloud_urls)}
            async with session.get(WORKER_URL, params=params, timeout=90) as resp:
                data = await resp.json()

        # ✅ Worker now returns a list of results
        if isinstance(data, dict):
            results = [data]
        else:
            results = data

        if not results:
            await wait_msg.edit_text("❌ No links found in response.")
            return

        text = "✅ **HubCloud Extracted Links:**\n\n"

        for f in results:
            if not isinstance(f, dict):
                continue

            movie_name = f.get("movie") or f.get("title") or "Unknown File"
            movie_size = f.get("size") or "Unknown Size"

            # Box-style formatting
            out_text += f"┎ 📚 <b>Title :-</b> {html.escape(movie_name)}\n"
            out_text += f"┃\n"
            out_text += f"┠ 💾 <b>Size :-</b> {html.escape(movie_size)}\n"
            out_text += f"┃\n"

            # Add server links
            for key, label in [
                ("pixeldrain", "Pixeldrain"),
                ("fsl", "FSL Server"),
                ("zipdisk", "ZipDisk Server"),
                ("10gbps", "10Gbps Server"),
            ]:
                links = f.get(key) or []
                if isinstance(links, str):
                    links = [links]
                for link in links:
                    out_text += f"┠ 🔗 <b>{label} :-</b> <a href='{html.escape(link)}'>Link</a>\n"
                    out_text += f"┃\n"

            out_text = out_text.rstrip("┃\n") + "\n\n━━━━━━━✦✗✦━━━━━━━\n\n"

        if message.from_user:
            out_text += f"Requested By :- {message.from_user.mention} (#ID_{message.from_user.id})"
                
        await wait_msg.edit_text(text, disable_web_page_preview=True)

    except Exception as e:
        await wait_msg.edit_text(f"⚠️ Error:\n`{e}`")
