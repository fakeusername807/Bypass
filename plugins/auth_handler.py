from pyrogram import Client, filters
from pyrogram.types import Message
from configs import OWNER_ID, groups_col  # import OWNER_ID and MongoDB collection

# ✅ In-memory cache for authorized groups
authorized_groups = set()


def load_groups():
    """Load authorized groups from MongoDB into memory"""
    global authorized_groups
    try:
        authorized_groups = {g["chat_id"] for g in groups_col.find()}
        print(f"✅ Loaded {len(authorized_groups)} authorized groups from MongoDB")
    except Exception as e:
        print(f"❌ Failed to load authorized groups: {e}")
        authorized_groups = set()


def add_group(chat_id: int):
    """Add a group to MongoDB and cache"""
    try:
        groups_col.update_one(
            {"chat_id": chat_id},
            {"$set": {"chat_id": chat_id}},
            upsert=True
        )
        authorized_groups.add(chat_id)
        print(f"✅ Added group {chat_id} to authorized groups")
    except Exception as e:
        print(f"❌ Failed to add group {chat_id}: {e}")


# ✅ Command: /auth or /authorize (Owner only)
@Client.on_message(filters.command(["auth", "authorize"]))
async def authorize_group(client: Client, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("❌ You are not authorized to use this command.")

    chat_id = None

    # Command sent inside a group → use that group
    if message.chat.type in ["group", "supergroup"]:
        chat_id = message.chat.id

    # Command sent in private → check for argument
    elif message.chat.type == "private":
        if not hasattr(message, "command") or len(message.command) < 2:
            return await message.reply_text(
                "⚠️ Please provide the group ID to authorize.\nExample: /auth -1001234567890"
            )
        try:
            chat_id = int(message.command[1])
        except ValueError:
            return await message.reply_text("❌ Invalid group ID. Make sure it's a number.")

    # Add the group
    if chat_id:
        if chat_id not in authorized_groups:
            add_group(chat_id)
            await message.reply_text(
                f"✅ Group `{chat_id}` has been authorized to use the bot.",
                parse_mode="markdown"
            )
        else:
            await message.reply_text(
                f"⚡ Group `{chat_id}` is already authorized.",
                parse_mode="markdown"
            )


# ✅ Restrict usage of commands to authorized groups only
ALLOWED_COMMANDS = ["prime", "gd", "gdflix", "p", "poster", "hub", "zee5"]

@Client.on_message(filters.command(ALLOWED_COMMANDS) & filters.group)
async def check_group_auth(client: Client, message: Message):
    if message.chat.id not in authorized_groups:
        return await message.reply_text(
            "🚫 This group is not authorized to use the bot.\n"
            "Only the owner can authorize with /auth"
        )
    # ⚡ If authorized → other command handlers will work normally


# ✅ Load groups from MongoDB at startup
load_groups()
