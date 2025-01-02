import sys
from logging import DEBUG, INFO, Logger, StreamHandler, basicConfig, getLogger
from logging.handlers import RotatingFileHandler
from pathlib import Path

import psutil
from dotenv import load_dotenv
from PySide6.QtCore import QStandardPaths

load_dotenv()

APP_NAME = "Kudan"
APP_VERSION = ""
APP_ORGANIZATION_NAME = ""
APP_ORGANIZATION_DOMAIN = ""


def contents_path(path: str = "") -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS).resolve().joinpath(path)
    else:
        return Path(".").resolve().joinpath(path)


GENERIC_DATA_PATH = Path(
    QStandardPaths.writableLocation(QStandardPaths.StandardLocation.GenericDataLocation)
)


def application_data_path(path: str = "") -> Path:
    application_data_path = GENERIC_DATA_PATH.joinpath(APP_NAME)
    application_data_path.mkdir(parents=True, exist_ok=True)
    return application_data_path.joinpath(path)


def application_temp_path(path: str = "") -> Path:
    application_temp_path = Path(
        QStandardPaths.writableLocation(QStandardPaths.StandardLocation.TempLocation)
    ).joinpath(APP_NAME)
    application_temp_path.mkdir(parents=True, exist_ok=True)
    return application_temp_path.joinpath(path)


def logger() -> Logger:
    rotating_file_handler = RotatingFileHandler(
        filename=application_data_path().joinpath("application.log"),
        maxBytes=512,
        backupCount=2,
    )
    rotating_file_handler.setLevel(INFO)
    basicConfig(
        force=True,
        level=DEBUG,
        encoding="UTF-8",
        format="%(asctime)s:%(levelname)s:%(filename)s:%(lineno)d:%(message)s",
        handlers=[StreamHandler(), rotating_file_handler],
    )
    return getLogger()


UNIX = (
    psutil.LINUX
    or psutil.MACOS
    or psutil.OSX
    or psutil.BSD
    or psutil.SUNOS
    or psutil.AIX
)
