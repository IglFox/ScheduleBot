from _ast import Dict

import requests
from bs4 import BeautifulSoup
import pandas as pd

from app.utils.LoggerHelp import logger_load

logger = logger_load(__name__)

def parse_schedule(url: str) -> Dict:
    """
    Парсит таблицу расписания с указанного URL.
    :param url: Ссылка на страницу с расписанием (например, https://spb.ranepa.ru/raspisanie/2koch/)
    :return: Список словарей с данными или None при ошибке
    """
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find('table')
        if not table:
            logger.WARNING("❌ Таблица не найдена на странице.")
            return None

        df = pd.read_html(str(table), encoding='utf-8')[0]

        schedule_data = df.to_dict(orient='records')

        logger.info(f"✅ Успешно распаршено {len(schedule_data)} строк расписания.")
        return schedule_data

    except requests.RequestException as e:
        logger.ERROR(f"❌ Ошибка загрузки страницы: {e}")
        return None

    except Exception as e:
        logger.ERROR(f"❌ Ошибка: {e}")
        return None