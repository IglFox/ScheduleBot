import locale
import os
import time
from typing import Dict, List, Any
from io import StringIO

import requests
from bs4 import BeautifulSoup
import pandas as pd

from app import config
from app.utils.LoggerHelp import logger_load

logger = logger_load(__name__)

retries = config.PARSER["ATTEMPTS"]
delay = config.PARSER["DELAY"]
file_path = config.PARSER["RAW_FILE_PATH"]
groups = config.GROUPS

def parse_schedule(url: str) -> List[Dict[str, Any]]:
    """
    Парсит таблицу расписания с указанного URL.
    :param url: Ссылка на страницу с расписанием (например, https://spb.ranepa.ru/raspisanie/2koch/)
    :return: Список словарей с данными или None при ошибке
    """
    for attempt in range(1, retries + 1):
        try:
            logger.info(f"🌐 Попытка {attempt} из {retries} — загрузка страницы: {url}")
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            response.encoding = 'utf-8'

            soup = BeautifulSoup(response.text, 'lxml')
            logger.info("✅ Страница успешно загружена. Поиск таблицы...")

            table = soup.find('table')
            if not table:
                logger.warning("❌ Таблица не найдена на странице.")
                return None

            logger.info("✅ Таблица найдена. Начинаем парсинг...")
            df = pd.read_html(StringIO(str(table)), encoding='utf-8')[0]
            schedule_data = df.to_dict(orient='records')

            logger.info(f"✅ Успешно распаршено {len(schedule_data)} строк расписания.")
            return schedule_data

        except requests.exceptions.Timeout:
            logger.warning(f"⏰ Таймаут при подключении (попытка {attempt}).")
        except requests.exceptions.ConnectionError:
            logger.warning(f"🔌 Ошибка соединения (попытка {attempt}).")
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Ошибка запроса (попытка {attempt}): {e}")
        except Exception as e:
            logger.error(f"🚨 Неожиданная ошибка при попытке {attempt}: {e}")

        # Если есть ещё попытки — ждём и пробуем снова
        if attempt < retries:
            logger.info(f"🔁 Ждём {delay} секунд перед повторной попыткой...")
            time.sleep(delay)
        else:
            logger.error("❌ Все попытки исчерпаны. Не удалось загрузить и распарсить страницу.")
            return None
    return None

def export_to_excel(data: List[Dict[str, Any]]):
    """Экспортирует данные в Excel файл."""
    if data:
        columns = [
            "Дата",
            "День недели",
            "Время",
            "Группы",
            "Предмет",
            "Преподаватель",
            "Аудитория",
            "ТипЗанятий"
        ]
        try:
            df = pd.DataFrame(data)
            logger.info("✅ Начинаем фильтрацию и экспорт в Excel...")
            filtered_rows = []
            for _, row in df.iterrows():
                groups_cell = str(row["Группы"])
                include = False
                for target_group in groups:
                    if target_group in groups_cell:
                        include = True
                        break
                if include:
                    filtered_rows.append(row)

            filtered_df = pd.DataFrame(filtered_rows)

            if filtered_df.empty:
                logger.warning("⚠️ Ни одна из целевых групп не найдена в расписании.")
                return

            final_df = filtered_df[columns]
            final_df.to_excel(file_path, index=False)

            size_mb = final_df.memory_usage(deep=True).sum() / (1024 ** 2)
            logger.info(f"📁 Расписание успешно экспортировано в файл: {file_path}. Размер: {size_mb:.2f} МБ")

        except Exception as e:
            logger.error(f"❌ Ошибка при экспорте в Excel: {e}")

def get_months():
    logger.info("📅 Получаем список месяцев...")
    locale.setlocale(locale.LC_TIME, 'russian')

    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        df['Дата'] = pd.to_datetime(df['Дата'], format='%d.%m.%Y')

        df['месяц'] = df['Дата'].dt.month  # номер месяца (1-12)
        df['месяц_название'] = df['Дата'].dt.strftime('%B') # название месяца
        months = df['месяц_название'].unique()
        months_num = df['месяц'].unique()
        logger.info(f"✅ Список месяцев: {months}")
        return list(months), list(months_num)
    logger.error("❌ Не удалось получить месяца.")
    return [], []