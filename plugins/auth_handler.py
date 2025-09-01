from pyrogram import Client, filters
from pyrogram.types import Message
from config import OWNER_ID, AUTH  # import variables directly
from globals import AuthU

OWNER = str(OWNER_ID)
AuthU = AUTH  # initialize AuthU from config

# ---------------------------
# Helper functions
# ---------------------------

def is_authorized(user_id: int, chat_id: int = None) -> bool:
    """
    Check if a user or a chat is authorized.
    """
    auth_list = AuthU.split(",")
    if str(user_id) in auth_list:
        return True
    if chat_id and str(chat_id) in auth_list:
        return True
    return False

def auth_required(func):
    """
    Decorator to enforce authorization on commands.
    """
    async def wrapper(client, message: Message):
        user_id = message.from_user.id
        chat_id = message.chat.id
        if not is_authorized(user_id, chat_id):
            await message.reply(
                "❌ You are not authorized to use this command!\n\n"
                "Now you can use it after authorization ✅"
            )
            return
        return await func(client, message)
    return wrapper

# ---------------------------
# Auth management commands
# ---------------------------

@Client.on_message(filters.command("addauth"))
async def add_auth(client, message: Message):
    global AuthU
    args = message.text.split(" ", 1)

    if str(message.from_user.id) != OWNER:
        await message.reply("❌ Only the owner can add users/groups!")
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

@Client.on_message(filters.command("removeauth"))
async def remove_auth(client, message: Message):
    global AuthU
    args = message.text.split(" ", 1)

    if str(message.from_user.id) != OWNER:
        await message.reply("❌ Only the owner can remove users/groups!")
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

@Client.on_message(filters.command("listauth"))
async def list_auth(client, message: Message):
    if str(message.from_user.id) != OWNER:
        await message.reply("❌ Only the owner can view the list!")
        return

    global AuthU
    auth_list = [i for i in AuthU.split(",") if i and i not in ["0", "0000000000"]]

    if not auth_list:
        await message.reply("❌ No authorized IDs found.")
        return

    text_lines = []
    for i in auth_list:
        mention = f"[Jump](tg://user?id={i})" if not i.startswith("-") else "Group/Channel"
        text_lines.append(f"🔹 `{i}` - {mention}")

    await message.reply("**🔐 Authorized IDs:**\n\n" + "\n".join(text_lines), disable_web_page_preview=True)

@Client.on_message(filters.command("checkauth"))
async def check_auth(client, message: Message):
    if str(message.from_user.id) != OWNER:
        await message.reply("❌ Only the owner can view the raw list!")
        return

    await message.reply(f"**🔐 Authorized IDs (raw):**\n\n`{AuthU}`")

# ---------------------------
# User commands (protected)
# ---------------------------

@Client.on_message(filters.command("start"))
@auth_required
async def start(client, message: Message):
    await message.reply("✅ Bot is alive and you are authorized!")

@Client.on_message(filters.command("prime"))
@auth_required
async def prime_posters(client, message: Message):
    await message.reply("✅ Now u can use")

@Client.on_message(filters.command("gd"))
@auth_required
async def gd_links(client, message: Message):
    await message.reply("✅ Now u can use")

@Client.on_message(filters.command("gdflix"))
@auth_required
async def gdflix_links(client, message: Message):
    await message.reply("✅ Now u can use")

@Client.on_message(filters.command("p"))
@auth_required
async def p_posters(client, message: Message):
    await message.reply("✅ Now u can use")

@Client.on_message(filters.command("poster"))
@auth_required
async def poster_command(client, message: Message):
    await message.reply("✅ Now u can use")

@Client.on_message(filters.command("hub"))
@auth_required
async def hub_command(client, message: Message):
    await message.reply("✅ Now u can use")

@Client.on_message(filters.command("zee5"))
@auth_required
async def zee5_command(client, message: Message):
    await message.reply("✅ Now u can use")
