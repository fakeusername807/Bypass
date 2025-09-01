from os import getenv as genv
from pymongo import MongoClient

# Telegram API credentials
API_ID = genv("API_ID", "7041911")
API_HASH = genv("API_HASH", "abab2561c71e3004a55d4ff9763d5383")
BOT_TOKEN = genv("BOT_TOKEN", "")

# Worker URL
WORKER_URL = "https://adda.botzs.workers.dev"

AUTH = genv("AUTH", "-1002311378229")
                 
# Owner ID
OWNER_ID = int(genv("OWNER_ID", "6390511215"))

# MongoDB Atlas URL
MONGO_URL = genv(
    "MONGO_URL",
    "mongodb+srv://scrape:scrape@cluster0.frrzcbo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)

# MongoDB Setup
mongo_client = MongoClient(MONGO_URL)
db = mongo_client["auth_db"]
groups_col = db["authorized_groups"]
