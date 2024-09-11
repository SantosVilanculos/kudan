import sys
from logging import DEBUG, INFO, Logger, StreamHandler, basicConfig, getLogger
from logging.handlers import RotatingFileHandler
from pathlib import Path

from PySide6.QtCore import QStandardPaths

# from os import getenv
# from dotenv import load_dotenv
# load_dotenv()


def contents_directory_path() -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS).resolve()
    else:
        return Path(".").resolve()


GENERIC_DATA_LOCATION_PATH = Path(
    QStandardPaths.writableLocation(QStandardPaths.StandardLocation.GenericDataLocation)
)


def application_data_location_path() -> Path:
    APPLICATION_DATA_LOCATION_PATH = GENERIC_DATA_LOCATION_PATH.joinpath("")
    APPLICATION_DATA_LOCATION_PATH.mkdir(parents=True, exist_ok=True)
    return APPLICATION_DATA_LOCATION_PATH


def logger() -> Logger:
    rotating_file_handler = RotatingFileHandler(
        filename=application_data_location_path().joinpath(".log"),
        maxBytes=512,
        backupCount=2,
    )
    rotating_file_handler.setLevel(INFO)
    basicConfig(
        level=DEBUG,
        encoding="UTF-8",
        format="%(asctime)s:%(levelname)s:%(filename)s:%(lineno)d:%(message)s",
        handlers=[StreamHandler(), rotating_file_handler],
    )
    return getLogger()
