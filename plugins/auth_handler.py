from pyrogram import Client, filters
from pyrogram.types import Message
from config import OWNER_ID, groups_col  # MongoDB collection
from globals import AuthU  # dynamic user/chat authorization

# ---------------------- In-memory cache ----------------------
authorized_groups = set()

# ---------------------- Helper Functions ----------------------
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

def is_authorized(user_id: int) -> bool:
    """Check if user or chat is authorized via AuthU"""
    return str(user_id) in AuthU.split(",")

# ---------------------- /auth or /authorize Command ----------------------
@Client.on_message(filters.command(["auth", "authorize"]))
async def authorize_group(client: Client, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("❌ You are not authorized to use this command.")

    chat_id = None

    # Group message → use current group
    if message.chat.type in ["group", "supergroup"]:
        chat_id = message.chat.id

    # Private message → use argument
    elif message.chat.type == "private":
        parts = message.text.split()
        if len(parts) < 2:
            return await message.reply_text(
                "⚠️ Provide the group ID to authorize.\nExample: /auth -1001234567890"
            )
        try:
            chat_id = int(parts[1])
        except ValueError:
            return await message.reply_text("❌ Invalid group ID. Must be a number.")

    if chat_id:
        if chat_id not in authorized_groups:
            add_group(chat_id)
            await message.reply_text(
                f"✅ Group `{chat_id}` has been authorized.",
                parse_mode="markdown"
            )
        else:
            await message.reply_text(
                f"⚡ Group `{chat_id}` is already authorized.",
                parse_mode="markdown"
            )

# ---------------------- /addauth Command ----------------------
@Client.on_message(filters.command("addauth"))
async def add_auth(client, message: Message):
    global AuthU
    args = message.text.split(" ", 1)

    if message.from_user.id != OWNER_ID:
        return await message.reply("❌ You are not authorized to add users/chats!")

    if len(args) < 2:
        return await message.reply("⚠️ Usage: `/addauth user_or_chat_id`")

    new_id = args[1].strip()
    if not new_id.lstrip("-").isdigit():
        return await message.reply("⚠️ Please provide a valid numeric Telegram ID.")

    if new_id in AuthU.split(","):
        await message.reply(f"✅ ID `{new_id}` is already authorized.")
    else:
        AuthU += f",{new_id}" if AuthU else new_id
        await message.reply(f"✅ ID `{new_id}` has been added to the authorized list.")

# ---------------------- /removeauth Command ----------------------
@Client.on_message(filters.command("removeauth"))
async def remove_auth(client, message: Message):
    global AuthU
    args = message.text.split(" ", 1)

    if message.from_user.id != OWNER_ID:
        return await message.reply("❌ You are not authorized to remove users/chats!")

    if len(args) < 2:
        return await message.reply("⚠️ Usage: `/removeauth user_or_chat_id`")

    remove_id = args[1].strip()
    if not remove_id.lstrip("-").isdigit():
        return await message.reply("⚠️ Please provide a valid numeric Telegram ID.")

    auth_list = AuthU.split(",")
    if remove_id in auth_list:
        auth_list.remove(remove_id)
        AuthU = ",".join(auth_list)
        await message.reply(f"✅ ID `{remove_id}` has been removed from the authorized list.")
    else:
        await message.reply(f"❌ ID `{remove_id}` is not in the authorized list.")

# ---------------------- /listauth Command ----------------------
@Client.on_message(filters.command("listauth"))
async def list_auth(client, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("❌ You are not authorized to view the list!")

    global AuthU
    auth_list = AuthU.split(",")
    valid_auth_list = [i for i in auth_list if i and i not in ["0", "0000000000"]]

    if not valid_auth_list:
        return await message.reply("❌ No valid authorized IDs found.")

    text_lines = []
    for i in valid_auth_list:
        mention = f"[Jump](tg://user?id={i})" if not i.startswith("-") else "Group/Channel"
        text_lines.append(f"🔹 `{i}` - {mention}")

    await message.reply("**🔐 Authorized IDs:**\n\n" + "\n".join(text_lines), disable_web_page_preview=True)

# ---------------------- /checkauth Command ----------------------
@Client.on_message(filters.command("checkauth"))
async def check_auth(client, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("❌ You are not authorized to view the list!")

    await message.reply(f"**🔐 Authorized IDs (raw):**\n\n`{AuthU}`")

# ---------------------- Restrict usage of commands to authorized groups ----------------------
ALLOWED_COMMANDS = ["prime", "gd", "gdflix", "p", "poster", "hub", "zee5"]

@Client.on_message(filters.command(ALLOWED_COMMANDS) & filters.group)
async def check_group_auth(client: Client, message: Message):
    if message.chat.id not in authorized_groups and not is_authorized(message.from_user.id):
        return await message.reply_text(
            "🚫 This group/user is not authorized to use the bot.\n"
            "Only the owner can authorize with /auth or /addauth"
        )

# ---------------------- Load groups at startup ----------------------
load_groups()
