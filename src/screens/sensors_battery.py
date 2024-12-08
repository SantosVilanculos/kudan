import psutil
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QHideEvent, QShowEvent
from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QSizePolicy,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)

from components.ML import ML
from components.Page import Page


class SensorsBattery(QWidget):
    def __init__(self):
        super().__init__()

        q_stacked_layout = QStackedLayout(self)
        q_widget = QWidget()
        q_widget.setObjectName("form")
        q_widget.setStyleSheet(
            "#form{border:1px solid #e0e0e0;background-color:#ffffff}"
        )
        q_v_box_layout = QVBoxLayout(q_widget)
        q_v_box_layout.setContentsMargins(24, 24, 24, 24)
        q_v_box_layout.setSpacing(24)

        q_label = QLabel("sensors_battery")
        q_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        q_font = q_label.font()
        q_font.setWeight(QFont.Weight.Medium)
        q_label.setFont(q_font)
        q_v_box_layout.addWidget(q_label)

        self.q_progress_bar = QProgressBar()
        self.q_progress_bar.setStyleSheet(
            "QProgressBar{border:1px solid #e0e0e0;background-color:#f6f6f6}"
        )
        self.q_progress_bar.setFixedHeight(24)
        self.q_progress_bar.setMaximum(100)
        self.q_progress_bar.setTextVisible(False)
        self.q_progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        q_v_box_layout.addWidget(self.q_progress_bar)

        q_form_layout = QFormLayout()
        q_form_layout.setVerticalSpacing(12)

        self.percent = ML()
        self.percent.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("percent", self.percent)

        self.secsleft = ML()
        self.secsleft.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("secsleft", self.secsleft)

        self.power_plugged = ML()
        self.power_plugged.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("power_plugged", self.power_plugged)

        q_v_box_layout.addLayout(q_form_layout)
        q_stacked_layout.addWidget(q_widget)

    def update(self) -> None:
        sbattery = psutil.sensors_battery()

        if not sbattery:
            return None

        if int(sbattery.percent) > 100:
            self.q_progress_bar.setValue(100)
        else:
            self.q_progress_bar.setValue(int(sbattery.percent))

        self.percent.setText(f"{sbattery.percent}%")
        if sbattery.secsleft == psutil.POWER_TIME_UNLIMITED:
            self.secsleft.setText("POWER_TIME_UNLIMITED")
        elif sbattery.secsleft == psutil.POWER_TIME_UNKNOWN:
            self.secsleft.setText("POWER_TIME_UNKNOWN")
        else:
            self.secsleft.setText(str(sbattery.secsleft))
        self.power_plugged.setText(str(sbattery.power_plugged))


class Widget(Page):
    def __init__(self):
        super().__init__("sensors_battery")

        q_widget = QWidget()
        q_h_box_layout = QHBoxLayout(q_widget)
        q_h_box_layout.setContentsMargins(0, 0, 0, 0)
        q_h_box_layout.setSpacing(0)
        c = QWidget()
        c.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )
        c.setMaximumWidth(640)
        q_v_box_layout = QVBoxLayout(c)
        q_v_box_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        q_v_box_layout.setContentsMargins(24, 24, 24, 24)
        q_v_box_layout.setSpacing(24)
        self.sensors_battery = SensorsBattery()
        q_v_box_layout.addWidget(
            self.sensors_battery, alignment=Qt.AlignmentFlag.AlignTop
        )
        q_h_box_layout.addWidget(c)
        self.setWidget(q_widget)
        self.q_timer = QTimer(self)
        self.q_timer.setInterval(1_000)
        self.q_timer.timeout.connect(self.update)

    def update(self) -> None:
        self.sensors_battery.update()

    def showEvent(self, event: QShowEvent) -> None:
        self.update()
        self.q_timer.start()
        return super().showEvent(event)

    def hideEvent(self, event: QHideEvent) -> None:
        self.q_timer.stop()
        return super().hideEvent(event)
