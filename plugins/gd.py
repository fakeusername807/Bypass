import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "YOUR_BOT_TOKEN"
WORKER_URL = "https://gdflix.botzs.workers.dev/?url="

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a GDLink URL and I'll fetch details for you 🚀")

async def gdflix(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Usage: `/gdflix <GDLink URL>`", parse_mode="MarkdownV2")
        return

    user_input = context.args[0].strip()
    if not user_input.startswith("http"):
        await update.message.reply_text("⚠️ Please send a valid GDLink URL")
        return

    try:
        # Call your Cloudflare Worker
        resp = requests.get(WORKER_URL + user_input)
        text = resp.text

        # Send Worker response
        await update.message.reply_text(text, parse_mode="HTML", disable_web_page_preview=True)

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def fetch_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()
    if not user_input.startswith("http"):
        return  # Ignore non-links

    try:
        resp = requests.get(WORKER_URL + user_input)
        text = resp.text
        await update.message.reply_text(text, parse_mode="HTML", disable_web_page_preview=True)

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gd", gdflix))
    app.add_handler(CommandHandler("gdflix", gdflix))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fetch_file))
    app.run_polling()

if __name__ == "__main__":
    main()
