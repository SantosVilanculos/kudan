from PySide6.QtCore import QSize
from PySide6.QtWidgets import QMainWindow

from central_widget import CW


class Window(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setMinimumSize(QSize(640, 360))
        self.setCentralWidget(CW())
