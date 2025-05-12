from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPainter, QPaintEvent
from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QSizePolicy,
    QStyle,
    QStyleOption,
    QVBoxLayout,
    QWidget,
)


class P(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.q_form_layout = QFormLayout(self)
        self.q_form_layout.setContentsMargins(0, 0, 0, 0)
        self.q_form_layout.setSpacing(24)
        self.addRow(
            ["Ctrl", "B"],
            "Toggle Primary Side Bar Visibility",
        )
        self.addRow(["Ctrl", "Q"], "Quit")
        self.addRow(
            ["Ctrl", ","],
            "Open Settings",
        )
        self.addRow(
            ["Ctrl", "Shift", "F"],
            "Focus Search Input",
        )

    def paintEvent(self, event: QPaintEvent) -> None:
        q_style_option = QStyleOption()
        q_style_option.initFrom(self)
        q_painter = QPainter(self)

        self.style().drawPrimitive(
            QStyle.PrimitiveElement.PE_Widget, q_style_option, q_painter, self
        )

    def addRow(self, arg_1: list[str], arg_2: str):
        keybind = QLabel(str.join("+", arg_1))
        q_font = keybind.font()
        q_font.setWeight(QFont.Weight.Medium)
        keybind.setFont(q_font)

        command = QLabel(arg_2)
        command.setWordWrap(True)
        command.setAlignment(Qt.AlignmentFlag.AlignJustify)
        self.q_form_layout.addRow(keybind, command)


class Tab2(QWidget):
    def __init__(self) -> None:
        super().__init__()

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
        q_v_box_layout_0.setSpacing(0)
        q_v_box_layout_0.addWidget(P())
        q_h_box_layout.addWidget(
            q_widget_0, alignment=Qt.AlignmentFlag.AlignTop
        )
        q_scroll_area.setWidget(q_widget)
        q_v_box_layout.addWidget(q_scroll_area)
