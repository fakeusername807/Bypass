from pyrogram import filters
import requests, json, re

API_URL = "https://freeseptemberapi.vercel.app/bypass"

def bypass_link(url: str) -> str:
    try:
        res = requests.post(API_URL, json={"url": url}, timeout=20)
        _data = res.text
        if "message" in _data:
            return f"❌ {url} → {_data}"
        _j = json.loads(_data)
        return f"✅ {url} → {_j.get('url', '❌ Failed')}"
    except Exception as e:
        return f"⚠️ {url} → Error: {str(e)}"

# Handler (this will be auto-loaded by Pyrogram plugin system)
@Client.on_message(filters.command("bypass") & filters.private)
async def bypass_handler(_, message):
    if len(message.command) < 2:
        return await message.reply_text("⚡ Send like:\n`/bypass <link1> <link2> ...`")

    raw_text = " ".join(message.command[1:])
    links = re.findall(r'https?://\S+', raw_text)

    if not links:
        return await message.reply_text("❌ No valid links found!")

    await message.reply_text(f"⏳ Bypassing {len(links)} link(s)... please wait")

    results = [bypass_link(link) for link in links]
    final_msg = "🚀 **Bypass Results:**\n\n" + "\n".join(results)

    await message.reply_text(final_msg)
