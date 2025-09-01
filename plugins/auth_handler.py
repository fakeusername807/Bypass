from pyrogram import Client, filters
from pyrogram.types import Message
from config import OWNER_ID, groups_col  # import from config

# ✅ Cache for quick checks
authorized_groups = set()


def load_groups():
    """Load authorized groups into memory"""
    global authorized_groups
    authorized_groups = {g["chat_id"] for g in groups_col.find()}


def add_group(chat_id: int):
    """Add a group to MongoDB + cache"""
    groups_col.update_one(
        {"chat_id": chat_id},
        {"$set": {"chat_id": chat_id}},
        upsert=True
    )
    authorized_groups.add(chat_id)


# ✅ Command: /auth or /authorize (Owner only)
@Client.on_message(filters.command(["auth", "authorize"]))
async def authorize_group(client: Client, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("❌ You are not authorized to use this command.")

    if message.chat.type in ["group", "supergroup"]:
        chat_id = message.chat.id
        if chat_id not in authorized_groups:
            add_group(chat_id)
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
    # ⚡ If group is authorized → other command handlers will work


# ✅ Load groups at startup
load_groups()
