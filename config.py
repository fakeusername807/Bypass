from os import getenv as genv

# Telegram API credentials
API_ID = int(genv("API_ID", "26334970"))
API_HASH = genv("API_HASH", "e7d1141cca9fbe1ab45804163b5080c8")
BOT_TOKEN = genv("BOT_TOKEN", "7928207862:AAFUk521pf1mHSGUxNf7WOxSm9NSJAR6w98")

# Worker URL
WORKER_URL = "https://adda.botzs.workers.dev"

# Authorized IDs (comma-separated)
AUTH = genv("AUTH", "-1002645306586")

# Owner ID
OWNER_ID = int(genv("OWNER_ID", "7965786027"))
