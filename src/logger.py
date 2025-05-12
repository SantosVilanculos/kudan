import sys
from logging import (
    DEBUG,
    Handler,
    Logger,
    StreamHandler,
    basicConfig,
    getLogger,
)
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import List

from PySide6.QtCore import QStandardPaths

from environment import APP_NAME

_handlers: List[Handler] = []

if not getattr(sys, "frozen", False):
    _handlers.append(StreamHandler())

_app_data_path = Path(
    QStandardPaths.writableLocation(
        QStandardPaths.StandardLocation.GenericDataLocation
    ),
    APP_NAME,
).resolve()
_app_data_path.mkdir(parents=True, exist_ok=True)

_handlers.append(
    RotatingFileHandler(filename=_app_data_path.joinpath(".log"), maxBytes=512)
)

basicConfig(
    force=True,
    level=DEBUG,
    encoding="UTF-8",
    format="%(asctime)s:%(levelname)s:%(filename)s:%(lineno)d:%(message)s",
    handlers=_handlers,
)

logger: Logger = getLogger()
