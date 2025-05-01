import psutil
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QHideEvent, QPainter, QPaintEvent, QShowEvent
from PySide6.QtWidgets import (QFormLayout, QHBoxLayout, QLabel, QProgressBar,
                               QScrollArea, QSizePolicy, QStyle, QStyleOption,
                               QVBoxLayout, QWidget)


class Item(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setObjectName("undefined")
        q_color = QColor(Qt.GlobalColor.lightGray)
        self.setStyleSheet(
            f"#undefined{{border: 1px solid {
                q_color.name()};background-color:white}}"
        )
        q_form_layout = QFormLayout(self)
        q_form_layout.setVerticalSpacing(24)
        self.q_progress_bar = QProgressBar()
        self.q_progress_bar.setFixedHeight(24)
        self.q_progress_bar.setMaximum(100)
        self.q_progress_bar.setTextVisible(False)
        q_form_layout.addRow(self.q_progress_bar)
        self.percent = QLabel("―")
        self.percent.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("percent", self.percent)
        self.secsleft = QLabel("―")
        self.secsleft.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("secsleft", self.secsleft)
        self.power_plugged = QLabel("―")
        self.power_plugged.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("powerPlugged", self.power_plugged)

    def paintEvent(self, event: QPaintEvent) -> None:
        q_style_option = QStyleOption()
        q_style_option.initFrom(self)
        q_painter = QPainter(self)
        self.style().drawPrimitive(
            QStyle.PrimitiveElement.PE_Widget, q_style_option, q_painter, self
        )

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


class Widget(QScrollArea):
    def __init__(self):
        super().__init__()

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        q_widget = QWidget()
        q_h_box_layout = QHBoxLayout(q_widget)
        q_h_box_layout.setContentsMargins(24, 24, 24, 24)
        q_h_box_layout.setSpacing(0)
        main = QWidget()
        main.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )
        main.setMaximumWidth(568)
        q_v_box_layout = QVBoxLayout(main)
        q_v_box_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        q_v_box_layout.setContentsMargins(0, 0, 0, 0)
        self.item = Item()
        q_v_box_layout.addWidget(self.item)
        q_h_box_layout.addWidget(main)

        self.setWidget(q_widget)

        self.q_timer = QTimer(self)
        self.q_timer.setInterval(1_000)
        self.q_timer.timeout.connect(self.update)

    def showEvent(self, event: QShowEvent) -> None:
        self.q_timer.start()
        return super().showEvent(event)

    def hideEvent(self, event: QHideEvent) -> None:
        self.q_timer.stop()
        return super().hideEvent(event)

    def update(self) -> None:
        self.item.update()
