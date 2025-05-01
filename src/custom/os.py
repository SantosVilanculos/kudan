from datetime import datetime, timedelta
from locale import getencoding, getlocale
from pathlib import Path
from platform import uname

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
        return uname().system

    @staticmethod
    def node() -> str:
        return uname().node

    @staticmethod
    def release() -> str:
        return uname().release

    @staticmethod
    def machine() -> str:
        return uname().machine

    @staticmethod
    def processor() -> str:
        return uname().processor

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
    def open_uri(uri: QUrl | str) -> bool:
        return QDesktopServices.openUrl(uri)

    @staticmethod
    def open_path(path: Path | str) -> bool:
        if isinstance(path, str):
            path = Path(path)

        return QDesktopServices.openUrl(path.resolve().as_uri())

    @staticmethod
    def standard_path(
        standard_location: QStandardPaths.StandardLocation, path: Path | str = ""
    ) -> Path:
        return (
            Path(QStandardPaths.writableLocation(standard_location))
            .resolve()
            .joinpath(path)
        )
