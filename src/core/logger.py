import logging
import os

from logging.handlers import RotatingFileHandler

from core.settings import log_settings


def set_log_handler():
    if not os.path.exists(log_settings["dir_name"]):
        os.makedirs(log_settings["dir_name"])
    log_path = os.path.join(log_settings["dir_name"], log_settings["file_name"])

    file_handler = RotatingFileHandler(
        filename=log_path,
        maxBytes=log_settings["log_size"],
        backupCount=log_settings["backup_num"],
    )
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
        )
    )
    file_handler.setLevel(log_settings["log_level"])
    return file_handler


file_handler = set_log_handler()
logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
