import sys
from logging import DEBUG, INFO, Logger, StreamHandler, basicConfig, getLogger
from logging.handlers import RotatingFileHandler

# from os import getenv
from pathlib import Path

from dotenv import load_dotenv
from PySide6.QtCore import QStandardPaths

load_dotenv()

GITHUB_REPOSITORY_URL = "https://github.com/quollouq/kudan"

APPLICATION_NAME = "Kudan"


def contents_path() -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS).resolve()
    else:
        return Path(".").resolve()


GENERIC_DATA_PATH = Path(
    QStandardPaths.writableLocation(QStandardPaths.StandardLocation.GenericDataLocation)
)


def application_data_path() -> Path:
    application_data_path = GENERIC_DATA_PATH.joinpath(APPLICATION_NAME)
    application_data_path.mkdir(parents=True, exist_ok=True)
    return application_data_path


def application_temp_path() -> Path:
    application_temp_path = Path(
        QStandardPaths.writableLocation(QStandardPaths.StandardLocation.TempLocation)
    ).joinpath(APPLICATION_NAME)
    application_temp_path.mkdir(parents=True, exist_ok=True)
    return application_temp_path


def logger() -> Logger:
    rotating_file_handler = RotatingFileHandler(
        filename=application_data_path().joinpath(".log"),
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
