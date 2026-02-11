from telebot import TeleBot
from telebot.types import Message

from app import config
from app.utils.LoggerHelp import logger_load
from app.utils.UseData import write_to_file

logger = logger_load(__name__)

def get_link_info(message: Message, bot: TeleBot, ):
    """
    set link with schedule
    :param bot:
    :param message:
    :return None:
    """

    if config.LINK["IS_SET"]:
        bot.send_message(message.chat.id, f"🔗 До этого была установлена ссылка: {config.LINK["URL"]}. Устанавливаю новую...")
    else:
        bot.send_message(message.chat.id, "📎 До этого ссылка не была установлена. Устанавливаю...")

def set_link(message: Message, bot):
    """
    Устанавливает ссылку по команде: /link <url>
    Пример: /link https://spb.ranepa.ru/raspisanie/2koch/
    """
    try:
        logger.info(f"Пользователь @{message.from_user.username} отправил команду /link")
        write_to_file(f"Пользователь @{message.from_user.username} вызвал /link")
        bot.send_chat_action(message.chat.id, 'typing')
        # Разделяем сообщение на части
        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            bot.reply_to(
                message,
                "❌ Не указана ссылка. Используйте:\n`/link <ссылка>`",
                parse_mode='Markdown'
            )
            return

        new_url = parts[1].strip()

        if not (new_url.startswith("http://") or new_url.startswith("https://")):
            bot.reply_to(
                message,
                "❌ Некорректная ссылка. Должна начинаться с `http://` или `https://`",
                parse_mode='Markdown'
            )
            return

        config.LINK["URL"] = new_url
        config.LINK["IS_SET"] = True

        bot.reply_to(
            message,
            f"✅ Ссылка успешно установлена:\n`{new_url}`",
            parse_mode='Markdown'
        )
        logger.info(f"Ссылка установлена: {new_url}")

    except Exception as e:
        logger.error(f"Ошибка при установке ссылки: {e}")
        bot.reply_to(message, "❌ Произошла ошибка при сохранении ссылки.")

