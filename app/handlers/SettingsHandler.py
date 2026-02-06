from telebot import TeleBot
from telebot.types import Message

from app import config
from app.utils.LoggerHelp import logger_load

logger = logger_load(__name__)

def set_link_info(message: Message, bot: TeleBot, ):
    """
    set link with schedule
    :param bot:
    :param message:
    :return None:
    """

    if config.LINK["IS_SET"]:
        bot.send_message(message.chat.id, f"🔗 Ссылка уже установлена: {config.LINK["URL"]}. Переустановить: url=<ваша ссылка>")
    else:
        bot.send_message(message.chat.id, "📎 Ссылка не установлена. Отправьте ссылку на расписание в формате: url=<ваша ссылка>")

def set_link(message: Message, bot: TeleBot, ):
    """установка ссылки на расписание"""
    try:
        config.LINK["URL"] = message.text[4:]
        bot.send_message(message.chat.id, f"🔗 Ссылка установлена: {config.LINK['URL']}")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка. Попробуйте еще раз")
        logger.error(str(e))


