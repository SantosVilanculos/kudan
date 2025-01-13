import sys
from logging import DEBUG, INFO, Logger, StreamHandler, basicConfig, getLogger
from logging.handlers import RotatingFileHandler
from pathlib import Path

from custom.os import OS

APP_NAME = "Kudan"
APP_VERSION = "0.0.3"
APP_URL = "http://github.com/santosvilanculos/kudan"
APP_ORGANIZATION_NAME = "Kudan"
APP_ORGANIZATION_DOMAIN = "Kudan"


def contents_path(path: Path | str = "") -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS).resolve().joinpath(path)
    else:
        return Path(".").resolve().joinpath(path)


def application_data_path(path: Path | str = "") -> Path:
    application_data_path = OS.generic_data_path(APP_NAME)
    application_data_path.mkdir(parents=True, exist_ok=True)
    return application_data_path.joinpath(path)


def application_temp_path(path: Path | str = "") -> Path:
    application_temp_path = OS.temp_path(APP_NAME)
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
