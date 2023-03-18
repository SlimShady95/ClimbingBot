from dotenv import load_dotenv
from os import getenv

# Load data from .env
load_dotenv()

# Telegram API credentials
telegram_api_key = getenv('telegram-api-key')
telegram_chat_id = getenv('telegram-chat-id')

# Path to the sqlite database
database_path = getenv('database-path')
