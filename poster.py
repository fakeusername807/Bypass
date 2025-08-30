import aiohttp
from aiohttp import web
from configs import *
from pyrogram import Client, filters, idle
from pyrogram.types import Message
import asyncio
import pyrogram

# ===== BOT INSTANCE =====
class ShortnerBot(Client):
    def __init__(self):
        super().__init__(
            "Scrapper",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="plugins"),
            workers=100,
        )


# ===== HEALTH CHECK =====
async def health_handler(request):
    return web.Response(text="ok")

async def start_webserver():
    app = web.Application()
    app.router.add_get("/", health_handler)  # Koyeb health ping
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()
    print("🌐 Health check server running on port 8080")



if __name__ == "__main__":
    ShortnerBot().run()
