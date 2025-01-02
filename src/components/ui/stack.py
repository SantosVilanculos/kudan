from PySide6.QtWidgets import QStackedWidget, QWidget


class Navigator(QStackedWidget):
    HISTSIZE = 24

    def __init__(self):
        super().__init__()
        self._screens: dict[str, int] = dict()
        self._history: list[int] = list()

        self.currentChanged.connect(self._current_changed)
        self.widgetRemoved.connect(self._widget_removed)

    def addWidget(self, name: str, q_widget: QWidget) -> int:
        index = super().addWidget(q_widget)
        self._screens[name] = index
        return index

    def navigate(self, name: str) -> None:
        index = self._screens.get(name, None)

        if index is None:
            raise ValueError()

        self.setCurrentIndex(index)

    def currentName(self) -> str | None:
        name = None
        for k, v in self._screens.items():
            if v == self.currentIndex():
                name = k
        return name

    def _current_changed(self, index: int) -> None:
        if len(self._history) >= self.HISTSIZE:
            self._history.pop(0)
        self._history.append(index)

    def _widget_removed(self, index: int) -> None:
        _d: dict[str, int] = dict()
        for k, v in self._screens.items():
            if v != index:
                _d[k] = v
        self._screens = _d

        self._history = [
            self._history[i]
            for i in range(len(self._history))
            if self._history[i] != index
        ]
