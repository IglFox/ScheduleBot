from pathlib import Path

from telebot import TeleBot
from telebot.types import Message

from app import config
from app.utils.LoggerHelp import logger_load
from app.utils.ScheduleCleaner import clean
from app.utils.ScheduleParse import parse_schedule, export_to_excel, get_months
from app.utils.UseData import write_to_file

logger = logger_load(__name__)


def get_line(months: list, months_nums: list):
    result = ""
    for i in range(len(months)):
        result += f"{months_nums[i]} - {months[i]}\n"
    return result

def get_schedule(message: Message, bot: TeleBot, ):
    logger.info(f"Пользователь @{message.from_user.username} вызвал /get")
    write_to_file(f"Пользователь @{message.from_user.username} вызвал /get")
    if config.LINK["URL"] is not None:
        month = message.text.split()[1] if len(message.text.split()) > 1 else None

        if month is None:
            months, months_nums = get_months()
            line = get_line(months, months_nums)
            bot.reply_to(message, f"❌ Не указан месяц. В расписании присутствуют данные за месяца: \n{line}")
        bot.send_chat_action(message.chat.id, 'upload_document')

        dict_schedule = parse_schedule(config.LINK["URL"])
        if dict_schedule:
            export_to_excel(dict_schedule)
            clean(month)
            file_path = Path(config.PARSER["FILE_PATH"])
            if file_path.exists():
                with open(file_path, 'rb') as doc:
                    bot.send_document(
                        chat_id=message.chat.id,
                        document=doc,
                        caption="📄 Ваше расписание готово!"
                    )
                logger.info("✅ Расписание успешно отправлено пользователю.")
            else:
                bot.reply_to(message, "❌ Файл не найден после генерации. Попробуйте ещё раз")
                logger.error("❌ Файл не найден после генерации.")
        else:
            bot.reply_to(message, "❌ Не удалось получить расписание. Попробуйте ещё раз.")
            logger.error("❌ Не удалось получить расписание.")
    else:
        bot.reply_to(message, "❌ Не указан URL для парсинга. Воспользуйтесь /link")