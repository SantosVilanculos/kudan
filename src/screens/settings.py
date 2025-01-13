from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPainter, QPaintEvent
from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QScrollArea,
    QSizePolicy,
    QStyle,
    QStyleOption,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


class P(QWidget):
    def __init__(self) -> None:
        super().__init__()

        q_v_box_layout = QVBoxLayout(self)
        q_v_box_layout.setContentsMargins(0, 0, 0, 0)
        q_v_box_layout.setSpacing(24)

        q_line_edit = QLineEdit()
        q_line_edit.setTextMargins(14, 0, 14, 0)
        q_line_edit.setFixedHeight(40)
        q_line_edit.textChanged.connect(self.search)
        q_v_box_layout.addWidget(q_line_edit)

        self.q_form_layout = QFormLayout()
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
        q_v_box_layout.addLayout(self.q_form_layout)

    def paintEvent(self, event: QPaintEvent) -> None:
        q_style_option = QStyleOption()
        q_style_option.initFrom(self)
        q_painter = QPainter(self)

        self.style().drawPrimitive(
            QStyle.PrimitiveElement.PE_Widget, q_style_option, q_painter, self
        )

    def addRow(self, arg_1: list[str], arg_2: str):
        keybinding = QLabel(str.join("+", arg_1))
        q_font = keybinding.font()
        q_font.setWeight(QFont.Weight.Medium)
        keybinding.setFont(q_font)

        command = QLabel(arg_2)
        command.setWordWrap(True)
        command.setAlignment(Qt.AlignmentFlag.AlignJustify)
        self.q_form_layout.addRow(keybinding, command)

    def search(self, text: str):
        for row in reversed(range(self.q_form_layout.rowCount())):
            keybinding = self.q_form_layout.itemAt(
                row, QFormLayout.ItemRole.LabelRole
            ).widget()

            command = self.q_form_layout.itemAt(
                row, QFormLayout.ItemRole.FieldRole
            ).widget()

            if (not isinstance(keybinding, QLabel)) or (
                not isinstance(command, QLabel)
            ):
                continue

            if (
                keybinding.text().lower().find(text.lower()) == -1
                and command.text().lower().find(text.lower()) == -1
            ):
                self.q_form_layout.setRowVisible(row, False)
            else:
                self.q_form_layout.setRowVisible(row, True)


class Tab1(QWidget):
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
        q_h_box_layout.addWidget(q_widget_0, alignment=Qt.AlignmentFlag.AlignTop)
        q_scroll_area.setWidget(q_widget)
        q_v_box_layout.addWidget(q_scroll_area)


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
        q_form_layout = QFormLayout()
        q_form_layout.setContentsMargins(0, 0, 0, 0)
        q_form_layout.setSpacing(24)
        q_form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        q_line_edit_0 = QLineEdit()
        q_line_edit_0.setFixedHeight(40)
        q_form_layout.addRow("Lorem", q_line_edit_0)

        q_line_edit_1 = QLineEdit()
        q_line_edit_1.setFixedHeight(40)
        q_form_layout.addRow("Lorem ipsum", q_line_edit_1)

        q_line_edit_2 = QLineEdit()
        q_line_edit_2.setFixedHeight(40)
        q_form_layout.addRow("Lorem", q_line_edit_2)

        q_v_box_layout_0.addLayout(q_form_layout)
        q_h_box_layout.addWidget(q_widget_0, alignment=Qt.AlignmentFlag.AlignTop)
        q_scroll_area.setWidget(q_widget)
        q_v_box_layout.addWidget(q_scroll_area)


class Widget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        q_v_box_layout = QVBoxLayout(self)
        q_v_box_layout.setContentsMargins(0, 0, 0, 0)
        q_v_box_layout.setSpacing(0)
        self.q_tab_widget = QTabWidget()
        self.q_tab_bar = self.q_tab_widget.tabBar()
        self.q_tab_bar.setDocumentMode(True)
        self.q_tab_widget.addTab(Tab1(), "keyboard shortcut")
        self.q_tab_widget.addTab(Tab2(), "Lorem")
        q_v_box_layout.addWidget(self.q_tab_widget)
