import psutil
import psutil._common
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QFont, QHideEvent, QShowEvent
from PySide6.QtWidgets import (QFormLayout, QHBoxLayout, QLabel, QScrollArea,
                               QSizePolicy, QStackedLayout, QVBoxLayout,
                               QWidget)


class ListItem(QWidget):
    def __init__(self, shwtemp: psutil._common.shwtemp) -> None:
        super().__init__()

        self.shwtemp = shwtemp

        q_stacked_layout = QStackedLayout(self)
        q_widget = QWidget()
        q_color = QColor(Qt.GlobalColor.lightGray)
        q_widget.setObjectName("name")
        q_widget.setStyleSheet(
            f"#name{{border:1px solid {q_color.name()};background-color:white}}"
        )
        q_form_layout = QFormLayout(q_widget)
        q_form_layout.setSpacing(24)
        self.label = QLabel(shwtemp.label or "―")
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("label", self.label)
        self.current = QLabel(self.temperature(shwtemp.current))
        self.current.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("current", self.current)
        self.high = QLabel(self.temperature(shwtemp.high))
        self.high.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("hight", self.high)
        self.critical = QLabel(self.temperature(shwtemp.critical))
        self.critical.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("critical", self.critical)

        q_stacked_layout.addWidget(q_widget)

    def update(self, shwtemp: psutil._common.shwtemp) -> None:
        self.label.setText(shwtemp.label or "―")
        self.current.setText(self.temperature(shwtemp.current))
        self.high.setText(self.temperature(shwtemp.high))
        self.current.setText(self.temperature(shwtemp.critical))

    def temperature(self, number: float | None) -> str:
        if number is None:
            return "―"

        return f"{number:.2f} ℃"  # ℉


class List(QWidget):
    def __init__(self, name: str) -> None:
        super().__init__()

        self.name = name
        self.q_v_box_layout = QVBoxLayout(self)
        self.q_v_box_layout.setContentsMargins(0, 0, 0, 0)
        q_label = QLabel(name)
        q_font = q_label.font()
        q_font.setWeight(QFont.Weight.Medium)
        q_label.setFont(q_font)
        self.q_v_box_layout.addWidget(q_label)

        for shwtemp in psutil.sensors_temperatures().get(self.name, list()):
            self.q_v_box_layout.addWidget(ListItem(shwtemp))

    def update(self) -> None:
        _A = psutil.sensors_temperatures().get(self.name, list())
        _B: list[str] = [shwtemp.label for shwtemp in _A]
        _C: list[str] = list()

        for index in range(self.q_v_box_layout.count()):
            q_layout_item = self.q_v_box_layout.itemAt(index)

            if not q_layout_item:
                continue

            q_widget = q_layout_item.widget()

            if not isinstance(q_widget, ListItem):
                continue

            if q_widget.shwtemp.label not in _B:
                self.q_v_box_layout.removeWidget(q_widget)
                q_widget.deleteLater()
            else:
                _C.append(q_widget.shwtemp.label)
                shwtemp = next(
                    (
                        shwtemp
                        for shwtemp in _A
                        if shwtemp.label == q_widget.shwtemp.label
                    ),
                    None,
                )
                if shwtemp:
                    q_widget.update(shwtemp)

        for shwtemp in _A:
            if shwtemp.label not in _C:
                self.q_v_box_layout.addWidget(ListItem(shwtemp))


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
            section = List(name)
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
