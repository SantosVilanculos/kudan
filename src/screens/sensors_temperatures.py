import psutil
import psutil._common
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QHideEvent, QShowEvent
from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QSizePolicy,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)


class SHWTEMP(QWidget):
    def __init__(self, shwtemp: psutil._common.shwtemp) -> None:
        super().__init__()

        self.shwtemp = shwtemp

        q_stacked_layout = QStackedLayout(self)
        q_widget = QWidget()
        q_widget.setObjectName("name")
        q_widget.setStyleSheet(
            "QWidget#name{border:1px solid rgba(0,0,0,0.12);background-color:#ffffff}"
        )
        q_form_layout = QFormLayout(q_widget)
        q_form_layout.setContentsMargins(14, 14, 14, 14)
        q_form_layout.setSpacing(12)
        self.label = QLabel(shwtemp.label)
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("label", self.label)
        self.current = QLabel(str(shwtemp.current))
        self.current.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("current", self.current)
        self.high = QLabel(str(shwtemp.high))
        self.high.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("high", self.high)
        self.critical = QLabel(str(shwtemp.critical))
        self.critical.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("critical", self.critical)
        q_stacked_layout.addWidget(q_widget)

    def update(self, shwtemp: psutil._common.shwtemp) -> None:
        self.label.setText(shwtemp.label)
        self.current.setText(str(shwtemp.current))
        self.high.setText(str(shwtemp.high))
        self.critical.setText(str(shwtemp.critical))


class Section(QWidget):
    def __init__(self, name: str) -> None:
        super().__init__()

        self.name = name
        self.li: list[SHWTEMP] = list()

        q_v_box_layout_0 = QVBoxLayout(self)
        q_v_box_layout_0.setContentsMargins(0, 0, 0, 0)
        # q_v_box_layout_0.setSpacing(0)

        q_label = QLabel(name)
        q_font = q_label.font()
        q_font.setWeight(QFont.Weight.Medium)
        q_label.setFont(q_font)
        q_v_box_layout_0.addWidget(q_label)

        self.q_v_box_layout = QVBoxLayout()
        self.q_v_box_layout.setContentsMargins(0, 0, 0, 0)
        # self.q_v_box_layout.setSpacing(0)

        for shwtemp in psutil.sensors_temperatures().get(self.name, list()):
            a = SHWTEMP(shwtemp)
            self.li.append(a)
            self.q_v_box_layout.addWidget(a)

        q_v_box_layout_0.addLayout(self.q_v_box_layout)

    def update(self) -> None:
        l = psutil.sensors_temperatures().get(self.name, list())

        for c in self.li:
            if c.shwtemp.label not in [item.label for item in l]:
                self.q_v_box_layout.removeWidget(c)
                self.li.remove(c)
                c.deleteLater()

        for item in l:
            existing_c = next(
                (c for c in self.li if c.shwtemp.label == item.label), None
            )

            if existing_c is None:
                a = SHWTEMP(item)
                self.li.append(a)
                self.q_v_box_layout.addWidget(a)
            else:
                existing_c.update(item)


class Widget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.q_timer = QTimer(self)
        self.q_timer.setInterval(1_000)

        q_v_box_layout = QVBoxLayout(self)
        q_v_box_layout.setContentsMargins(0, 0, 0, 0)
        q_v_box_layout.setSpacing(0)
        q_scroll_area = QScrollArea()
        q_scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        q_scroll_area.setWidgetResizable(True)
        q_widget = QWidget()
        q_h_box_layout = QHBoxLayout(q_widget)
        q_h_box_layout.setContentsMargins(24, 24, 24, 24)
        q_h_box_layout.setSpacing(0)
        q_widget_0 = QWidget()
        q_widget_0.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )
        q_widget_0.setMaximumWidth(568)

        q_v_box_layout_0 = QVBoxLayout(q_widget_0)
        q_v_box_layout_0.setContentsMargins(0, 0, 0, 0)
        q_v_box_layout_0.setSpacing(8)
        for name in psutil.sensors_temperatures().keys():
            section = Section(name)
            self.q_timer.timeout.connect(section.update)
            q_v_box_layout_0.addWidget(section)

        q_h_box_layout.addWidget(q_widget_0, alignment=Qt.AlignmentFlag.AlignTop)
        q_scroll_area.setWidget(q_widget)
        q_v_box_layout.addWidget(q_scroll_area)

    def showEvent(self, event: QShowEvent) -> None:
        self.q_timer.start()
        return super().showEvent(event)

    def hideEvent(self, event: QHideEvent) -> None:
        self.q_timer.stop()
        return super().hideEvent(event)
