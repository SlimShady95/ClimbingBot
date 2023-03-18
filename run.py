from Climbing.Bot.Bot import Bot
from Climbing.Bot.Database import Database
from Climbing.Util.Telegram import Telegram
from Config import database_path, telegram_api_key, telegram_chat_id

if __name__ == '__main__':
    # Instance of the bot which does all the heavy work
    bot = Bot(
        Telegram(telegram_api_key, telegram_chat_id),
        Database(database_path)
    )
