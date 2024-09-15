from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow

from env import APPLICATION_NAME, contents_path
from root import Root


class Window(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        cp = contents_path()

        self.setWindowIcon(QIcon(str(cp.joinpath("icon.ico"))))
        self.setWindowTitle(APPLICATION_NAME)
        self.setMinimumSize(QSize(640, 360))

        self.setCentralWidget(Root())
