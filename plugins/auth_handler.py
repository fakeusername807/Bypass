# auth_handler.py
import os
from pyrogram import Client, filters
from pyrogram.types import Message
from pymongo import MongoClient

# ✅ Owner ID
OWNER_ID = int(os.environ.get("OWNER_ID", "123456789"))

# ✅ MongoDB Setup
MONGO_URL = os.environ.get("MONGO_URL", "mongodb+srv://username:password@cluster/dbname")
mongo_client = MongoClient(MONGO_URL)
db = mongo_client["auth_db"]  # Database
groups_col = db["authorized_groups"]  # Collection

# ✅ Get all authorized groups as a set (cached)
def get_authorized_groups():
    return {g["chat_id"] for g in groups_col.find()}

authorized_groups = get_authorized_groups()


def add_authorized_group(chat_id: int):
    """Add group to MongoDB + cache"""
    groups_col.update_one({"chat_id": chat_id}, {"$set": {"chat_id": chat_id}}, upsert=True)
    authorized_groups.add(chat_id)


# ✅ Command: /auth or /authorize (Owner only)
@Client.on_message(filters.command(["auth", "authorize"]))
async def authorize_group(client: Client, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("❌ You are not authorized to use this command.")

    if message.chat.type in ["group", "supergroup"]:
        chat_id = message.chat.id
        if chat_id not in authorized_groups:
            add_authorized_group(chat_id)
            await message.reply_text("✅ This group has been authorized to use the bot.")
        else:
            await message.reply_text("⚡ This group is already authorized.")
    else:
        await message.reply_text("⚠️ Use this command inside a group.")


# ✅ Restrict usage of commands to authorized groups only
ALLOWED_COMMANDS = ["prime", "gd", "gdflix", "p", "poster", "hub", "zee5"]

@Client.on_message(filters.command(ALLOWED_COMMANDS) & filters.group)
async def check_group_auth(client: Client, message: Message):
    if message.chat.id not in authorized_groups:
        return await message.reply_text(
            "🚫 This group is not authorized to use the bot.\n"
            "Only the owner can authorize with /auth"
        )
    # ⚡ If authorized → command handlers from plugins will run normally
