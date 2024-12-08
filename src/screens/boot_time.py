from datetime import datetime

import psutil
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QHideEvent, QShowEvent
from PySide6.QtWidgets import QLabel, QStackedLayout, QVBoxLayout, QWidget


class Widget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        q_stacked_layout = QStackedLayout(self)
        q_widget = QWidget()
        q_widget.setStyleSheet("background-color:#f6f6f6")
        q_v_box_layout = QVBoxLayout(q_widget)
        q_v_box_layout.setContentsMargins(0, 0, 0, 0)
        q_v_box_layout.setSpacing(0)

        self.q_label = QLabel()
        q_v_box_layout.addWidget(self.q_label, alignment=Qt.AlignmentFlag.AlignCenter)
        q_stacked_layout.addWidget(q_widget)

        self.q_timer = QTimer(self)
        self.q_timer.setInterval(1_000)
        self.q_timer.timeout.connect(self.update)

    def update(self) -> None:
        a = datetime.fromtimestamp(psutil.boot_time())
        b = datetime.now() - a
        self.q_label.setText(f"{a.strftime("%Y-%m-%d %H:%M:%S")}\n{b}")

    def showEvent(self, event: QShowEvent) -> None:
        self.q_timer.start()
        return super().showEvent(event)

    def hideEvent(self, event: QHideEvent) -> None:
        self.q_timer.stop()
        return super().hideEvent(event)
