import logging

from app.utils.DateHelper import get_today_date

LINK = {
    "IS_SET": False,
    "URL": None
}

USERS = {
    
}


LOGGER = {
    "IS_SET": True,
    "LEVEL": logging.INFO,
    "FMT": "%(asctime)s [%(levelname)s] %(name)s::%(funcName)s() - %(message)s",
    "DATEFMT": "%d.%m.%Y %H:%M"
}

PARSER = {
    "ATTEMPTS": 5,
    "DELAY": 3,
    "FILE_PATH": f"output/schedule_{get_today_date()}.xlsx",
    "CURRENT_FILE": None,
    "RAW_FILE_PATH": "output/raw.xlsx"
}

GROUPS = ['ГМУ-3-24-06', 'ГМУ-3-24-05-08']

