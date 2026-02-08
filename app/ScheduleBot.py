import time
from os import getenv
import telebot
from dotenv import load_dotenv
from requests import ReadTimeout

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
    restart_attempts = 0
    max_restart_attempts = 10

    while True:
        try:
            logger.info("Бот запущен!")
            bot.infinity_polling()
            restart_attempts = 0

        except ReadTimeout as e:
            logger.warning(f"Таймаут соединения: {e}")
            restart_attempts += 1
            wait_time = min(2 ** restart_attempts, 60)
            logger.info(f"Перезапуск через {wait_time} секунд...")
            time.sleep(wait_time)

        except Exception as e:
            logger.error(f"Неожиданная ошибка: {e}")
            restart_attempts += 1
            time.sleep(5)


if __name__ == "__main__":
    run()
