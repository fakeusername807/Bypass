import requests
from io import BytesIO
from PIL import Image, ImageEnhance
from pyrogram import filters

# Predefined positions
def get_position(bg_w, bg_h, logo_w, logo_h, position, x_offset=0, y_offset=0):
    if position == "top-left":
        return (0 + x_offset, 0 + y_offset)
    elif position == "top-right":
        return (bg_w - logo_w + x_offset, 0 + y_offset)
    elif position == "bottom-left":
        return (0 + x_offset, bg_h - logo_h + y_offset)
    elif position == "bottom-right":
        return (bg_w - logo_w + x_offset, bg_h - logo_h + y_offset)
    elif position == "center":
        return ((bg_w - logo_w)//2 + x_offset, (bg_h - logo_h)//2 + y_offset)
    elif position == "middle-left":
        return (0 + x_offset, (bg_h - logo_h)//2 + y_offset)
    elif position == "middle-right":
        return (bg_w - logo_w + x_offset, (bg_h - logo_h)//2 + y_offset)
    return (0, 0)

@bot.on_message(filters.command("overlap"))
async def overlap_handler(client, message):
    try:
        args = message.text.split()
        if len(args) < 4:
            return await message.reply("Usage: /overlap bg_url logo_url size position [x_offset] [y_offset] [left-right_opacity] [up-down_opacity]")

        bg_url, logo_url = args[1], args[2]
        size = int(args[3])
        position = args[4]

        x_offset = int(args[5]) if len(args) > 5 else 0
        y_offset = int(args[6]) if len(args) > 6 else 0
        lr_opacity = float(args[7]) if len(args) > 7 else 1.0
        ud_opacity = float(args[8]) if len(args) > 8 else 1.0

        bg = Image.open(BytesIO(requests.get(bg_url).content)).convert("RGBA")
        logo = Image.open(BytesIO(requests.get(logo_url).content)).convert("RGBA")
        logo = logo.resize((size*10, size*10))

        alpha = logo.split()[3]
        enhancer = ImageEnhance.Brightness(alpha)
        logo.putalpha(enhancer.enhance((lr_opacity + ud_opacity) / 2))

        pos = get_position(bg.width, bg.height, logo.width, logo.height, position, x_offset, y_offset)
        bg.paste(logo, pos, logo)

        output = BytesIO()
        output.name = "overlay.png"
        bg.save(output, format="PNG")
        output.seek(0)

        await message.reply_photo(output, caption="Here is your overlapped image ✅")
    except Exception as e:
        await message.reply(f"❌ Error: {e}")

@bot.on_message(filters.command("upload"))
async def upload_handler(client, message):
    try:
        args = message.text.split()
        if len(args) < 2:
            return await message.reply("Usage: /upload <image_url>")

        url = args[1]
        filename = url.split("/")[-1]
        r = requests.get(url, stream=True)
        r.raise_for_status()

        files = {"file": (filename, r.raw, "image/jpeg")}
        res = requests.post("https://envs.sh/", files=files)

        if res.status_code == 200:
            await message.reply(f"Uploaded ✅\n{res.text.strip()}/{filename}")
        else:
            await message.reply("❌ Upload failed")
    except Exception as e:
        await message.reply(f"❌ Error: {e}")

@bot.on_message(filters.command("sticker"))
async def sticker_handler(client, message):
    try:
        args = message.text.split()
        if len(args) < 2:
            return await message.reply("Usage: /sticker <image_url>")

        url = args[1]
        img = Image.open(BytesIO(requests.get(url).content)).convert("RGBA")
        output = BytesIO()
        output.name = "sticker.webp"
        img.save(output, format="WEBP")
        output.seek(0)

        await message.reply_sticker(output)
    except Exception as e:
        await message.reply(f"❌ Error: {e}")
