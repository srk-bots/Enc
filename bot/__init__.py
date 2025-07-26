import os
from pyrogram import Client
from dotenv import load_dotenv

# ✅ Load environment variables from config.env if it exists
if os.path.exists('config.env'):
    load_dotenv('config.env')

# ✅ Read values from environment
api_id = int(os.environ.get("25874070"))
api_hash = os.environ.get("f1522f0124b736b5eb4df95291d4139c")
bot_token = os.environ.get("BOT_TOKEN")
download_dir = os.environ.get("DOWNLOAD_DIR", "downloads/")
sudo_users = list(set(int(x) for x in os.environ.get("SUDO_USERS").split()))

# ✅ Initialize Pyrogram client
app = Client(":memory:", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# ✅ Global task queue
data = []

# ✅ Ensure download directory exists and ends with slash
if not download_dir.endswith("/"):
    download_dir = download_dir + "/"
if not os.path.isdir(download_dir):
    os.makedirs(download_dir)
