from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


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
        q_h_box_layout.addWidget(
            q_widget_0, alignment=Qt.AlignmentFlag.AlignTop
        )
        q_scroll_area.setWidget(q_widget)
        q_v_box_layout.addWidget(q_scroll_area)
