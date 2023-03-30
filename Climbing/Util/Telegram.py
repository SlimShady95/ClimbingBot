from typing import Union

from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.parsemode import ParseMode


class Telegram:
    # Api key
    _api_key = None

    # ID to group or normal chat
    _chat_id = None

    # The updater of the telegram api
    _updater = None

    def __init__(self, api_key: str, chat_id: str) -> None:
        """
            Sets up api key and chat id

            :param api_key: str
                The key for using the api
            :param chat_id: str
                The id of the chat
            :return None
        """
        self._api_key = api_key
        self._chat_id = chat_id
        self._init_updater()

    def _init_updater(self) -> None:
        """
            Initializes the updater of the telegram bot

            :return None
        """
        self._updater = Updater(self._api_key)

        # If the bot crashes, which happens from time to time and I cannot figure out why this happens, we just create
        # a new instance and start polling again
        try:
            self._updater.start_polling()
        except Exception as e:
            print(e)
            print('Restarting updater...')
            self._init_updater()

    def add_command(self, handler: Union[CommandHandler, MessageHandler]) -> 'Telegram':
        """
            Adds a command to the dispatcher

            :param handler: CommandHandler
                The handler to add
            :return Telegram
                Returns the instance of the telegram object to allow chaining
        """
        self._updater.dispatcher.add_handler(handler)

        return self

    def send_message(self, message: str, disable_preview: bool = True) -> None:
        """
            Sends a telegram message
            :param message: str
                The message to send
            :param disable_preview: bool
                If set to true, it will disable the preview
            :return None
        """
        self._updater.bot.send_message(self._chat_id, message, disable_web_page_preview=disable_preview, parse_mode=ParseMode.MARKDOWN_V2)
