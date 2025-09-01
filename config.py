from os import getenv as genv

# Telegram API credentials
API_ID = int(genv("API_ID", "7041911"))
API_HASH = genv("API_HASH", "abab2561c71e3004a55d4ff9763d5383")
BOT_TOKEN = genv("BOT_TOKEN", "")

# Worker URL
WORKER_URL = "https://adda.botzs.workers.dev"

# Authorized IDs (comma-separated)
AUTH = genv("AUTH", "-1002311378229")

# Owner ID
OWNER_ID = int(genv("OWNER_ID", "6390511215"))
