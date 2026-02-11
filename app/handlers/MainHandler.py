from telebot import TeleBot
from telebot.types import Message

from app.utils.LoggerHelp import logger_load
from app.utils.UseData import write_to_file

logger = logger_load(__name__)

def get_help(message: Message, bot: TeleBot, ):
    logger.info(f"Пользователь @{message.from_user.username} вызвал /help")
    write_to_file(f"Пользователь @{message.from_user.username} вызвал /help")
    bot.send_message(message.chat.id, "Привет! Я бот, который скинет тебе расписание. Мои команды: \n /link https://... - для привязки ссылки\n /get <номер месяца> - для получения расписания \n /help - для вызова этого сообщения 😊")