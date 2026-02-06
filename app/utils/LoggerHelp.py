import logging

from app import config


def logger_load(name: str):
    """
    Созжаёт настроенный логгер с указанным именем
    :return:
    """
    logger = logging.getLogger(name)
    logger.setLevel(config.LOGGER["LEVEL"])

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt=config.LOGGER["FMT"],
        datefmt=config.LOGGER["DATEFMT"]
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(config.LOGGER["LEVEL"])

    logger.addHandler(console_handler)

    logger.info(f"Логгер '{name}' успешно настроен")
    return logger