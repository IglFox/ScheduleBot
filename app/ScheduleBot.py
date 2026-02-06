from os import getenv
import telebot
from dotenv import load_dotenv

from app.handlers.MainHandler import get_help
from app.handlers.ScheduleHandler import get_schedule
from app.utils.LoggerHelp import logger_load
from app.handlers.LinkHandler import set_link

logger = logger_load(__name__)

load_dotenv()

bot = telebot.TeleBot(token=getenv("API_KEY"), num_threads=5)

def register_handlers():
    try:
        bot.register_message_handler(callback=set_link, commands=["link"], pass_bot=True)
        bot.register_message_handler(callback=get_schedule, commands=["get"], pass_bot=True)
        bot.register_message_handler(callback=get_help, commands=["start", "help"], pass_bot=True)
        logger.info("✅ Регистрация обработчиков завершена.")
    except Exception as e:
        logger.error(str(e))

register_handlers()

def run():
    logger.info("Бот запущен!")
    bot.infinity_polling()


if __name__ == "__main__":
    run()
