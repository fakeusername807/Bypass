from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config
from globals import AuthU

OWNER = Config.OWNER

# Helper function to check if user or chat is authorized
def is_authorized(user_id: int) -> bool:
    return str(user_id) in AuthU.split(",")

# Command to add a user or chat ID to AuthU
@Client.on_message(filters.command("addauth"))
async def add_auth(client, message: Message):
    global AuthU
    args = message.text.split(" ", 1)

    if str(message.from_user.id) not in OWNER:
        await message.reply("❌ You are not authorized to add users/chats!")
        return

    if len(args) < 2:
        await message.reply("⚠️ Usage: `/addauth user_or_chat_id`")
        return

    new_id = args[1].strip()
    if not new_id.lstrip("-").isdigit():
        await message.reply("⚠️ Please provide a valid numeric Telegram ID.")
        return

    if new_id in AuthU.split(","):
        await message.reply(f"✅ ID `{new_id}` is already authorized.")
    else:
        AuthU += f",{new_id}" if AuthU else new_id
        await message.reply(f"✅ ID `{new_id}` has been added to the authorized list.")

# Command to remove a user or chat ID from AuthU
@Client.on_message(filters.command("removeauth"))
async def remove_auth(client, message: Message):
    global AuthU
    args = message.text.split(" ", 1)

    if str(message.from_user.id) not in OWNER:
        await message.reply("❌ You are not authorized to remove users/chats!")
        return

    if len(args) < 2:
        await message.reply("⚠️ Usage: `/removeauth user_or_chat_id`")
        return

    remove_id = args[1].strip()
    if not remove_id.lstrip("-").isdigit():
        await message.reply("⚠️ Please provide a valid numeric Telegram ID.")
        return

    auth_list = AuthU.split(",")
    if remove_id in auth_list:
        auth_list.remove(remove_id)
        AuthU = ",".join(auth_list)
        await message.reply(f"✅ ID `{remove_id}` has been removed from the authorized list.")
    else:
        await message.reply(f"❌ ID `{remove_id}` is not in the authorized list.")

# View authorized IDs
@Client.on_message(filters.command("listauth"))
async def list_auth(client, message: Message):
    if str(message.from_user.id) not in OWNER:
        await message.reply("❌ You are not authorized to view the list!")
        return

    global AuthU
    auth_list = AuthU.split(",")
    valid_auth_list = [i for i in auth_list if i and i not in ["0", "0000000000"]]

    if not valid_auth_list:
        await message.reply("❌ No valid authorized IDs found.")
        return

    text_lines = []
    for i in valid_auth_list:
        mention = f"[Jump](tg://user?id={i})" if not i.startswith("-") else "Group/Channel"
        text_lines.append(f"🔹 `{i}` - {mention}")

    await message.reply("**🔐 Authorized IDs:**\n\n" + "\n".join(text_lines), disable_web_page_preview=True)

# Raw list of IDs
@Client.on_message(filters.command("checkauth"))
async def check_auth(client, message: Message):
    if str(message.from_user.id) not in OWNER:
        await message.reply("❌ You are not authorized to view the list!")
        return

    await message.reply(f"**🔐 Authorized IDs (raw):**\n\n`{AuthU}`")
