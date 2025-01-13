from typing import Any

from PySide6.QtCore import QSettings, Signal


class Configuration(QSettings):
    created = Signal(str, Any)
    updated = Signal(str, Any)
    deleted = Signal(str)

    def __init__(self) -> None:
        super().__init__()

    def setValue(self, key: str, value: Any) -> None:
        if self.contains(key):
            self.updated.emit(key, value)
        else:
            self.created.emit(key, value)

        super().setValue(key, value)
