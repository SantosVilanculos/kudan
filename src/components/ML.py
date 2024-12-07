from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel


class ML(QLabel):
    def __init__(self):
        super().__init__()
        q_font = QFont("GitLab Mono")
        q_font.setPixelSize(13)
        q_font.setWeight(QFont.Weight.Normal)
        q_font.setStyleStrategy(QFont.StyleStrategy.PreferQuality)
        self.setFont(q_font)
