from config import *
from pyrogram import Client, filters
from pyrogram.types import Message
import aiohttp

# ===== START COMMAND =====
@Client.on_message(filters.command("start"))
async def start_cmd(_, message: Message):
    await message.reply_text(
        f"<b>👋 Hello {message.from_user.first_name}!</b>\n\n"
        "<b>This Bot Only Works in Group</b>\n\n"
        "<b>Contact @MrSagar_RoBot For Group Link</b>"
    )
