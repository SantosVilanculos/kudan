from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QFrame


class Divider(QFrame):
    def __init__(
        self,
        orientation: Qt.Orientation = Qt.Orientation.Horizontal,
        q_color: QColor = QColor(Qt.GlobalColor.lightGray),
    ):
        super().__init__()
        if orientation == Qt.Orientation.Vertical:
            self.setFrameShape(QFrame.Shape.VLine)
        else:
            self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Plain)
        self.setStyleSheet(f"QFrame{{color:{q_color.name()}}}")
        self.setContentsMargins(0, 0, 0, 0)
