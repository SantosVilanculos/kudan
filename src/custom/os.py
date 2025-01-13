import platform
from datetime import datetime, timedelta
from locale import getencoding, getlocale
from pathlib import Path

import psutil
from PySide6.QtCore import QObject, QStandardPaths, QUrl
from PySide6.QtGui import QDesktopServices


class OS(QObject):
    UNIX = (
        psutil.LINUX
        or psutil.MACOS
        or psutil.OSX
        or psutil.BSD
        or psutil.SUNOS
        or psutil.AIX
    )
    POSIX = psutil.POSIX
    WINDOWS = psutil.WINDOWS
    LINUX = psutil.LINUX
    MACOS = psutil.MACOS
    OSX = psutil.OSX
    FREEBSD = psutil.FREEBSD
    OPENBSD = psutil.OPENBSD
    NETBSD = psutil.NETBSD
    BSD = psutil.BSD
    SUNOS = psutil.SUNOS
    AIX = psutil.AIX

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def system() -> str:
        return platform.uname().system

    @staticmethod
    def node() -> str:
        return platform.uname().node

    @staticmethod
    def release() -> str:
        return platform.uname().release

    @staticmethod
    def machine() -> str:
        return platform.uname().machine

    @staticmethod
    def processor() -> str:
        return platform.uname().processor

    @staticmethod
    def boot_time() -> datetime:
        return datetime.fromtimestamp(psutil.boot_time())

    @staticmethod
    def up_time() -> timedelta:
        return datetime.now() - datetime.fromtimestamp(psutil.boot_time())

    @staticmethod
    def locale() -> str | None:
        return getlocale()[0]

    @staticmethod
    def encoding() -> str:
        return getencoding()

    @staticmethod
    def open_url(q_url: QUrl | str) -> bool:
        return QDesktopServices.openUrl(q_url)

    @staticmethod
    def open_path(path: Path | str) -> bool:
        if isinstance(path, str):
            path = Path(path)

        return QDesktopServices.openUrl(path.resolve().as_uri())

    @staticmethod
    def generic_data_path(path: Path | str = "") -> Path:
        return (
            Path(
                QStandardPaths.writableLocation(
                    QStandardPaths.StandardLocation.GenericDataLocation
                )
            )
            .resolve()
            .joinpath(path)
        )

    @staticmethod
    def temp_path(path: Path | str = "") -> Path:
        return (
            Path(
                QStandardPaths.writableLocation(
                    QStandardPaths.StandardLocation.TempLocation
                )
            )
            .resolve()
            .joinpath(path)
        )
