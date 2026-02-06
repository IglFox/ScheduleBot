from logging import getLogger
from os import getenv
import telebot
from dotenv import load_dotenv

from handlers.SettingsHandler import *

logger = getLogger(__name__)

load_logger()
load_dotenv()

bot = telebot.TeleBot(token=getenv("API_KEY"))

def register_handlers():
    bot.register_message_handler(callback=set_link, regexp=r"^url=https?://[^\s]+$", pass_bot=True)
    bot.register_message_handler(callback=set_link_info, commands=["link"], pass_bot=True)

