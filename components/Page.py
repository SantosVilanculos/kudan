from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QHBoxLayout, QLabel, QScrollArea, QVBoxLayout, QWidget


class Page(QWidget):
    def __init__(self, label: str):
        super().__init__()
        q_v_box_layout = QVBoxLayout(self)
        q_v_box_layout.setContentsMargins(0, 0, 0, 0)
        q_v_box_layout.setSpacing(0)

        q_widget = QWidget()
        q_widget.setFixedHeight(44)
        q_h_box_layout = QHBoxLayout(q_widget)
        q_h_box_layout.setContentsMargins(24, 0, 24, 0)
        q_label = QLabel(label)
        q_font = q_label.font()
        q_font.setWeight(QFont.Weight.Medium)
        q_label.setFont(q_font)
        q_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        q_h_box_layout.addWidget(q_label)

        q_v_box_layout.addWidget(q_widget)

        self.q_scroll_area = QScrollArea()
        self.q_scroll_area.setStyleSheet("QScrollArea{border:0}")
        self.q_scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.q_scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.q_scroll_area.setWidgetResizable(True)
        q_v_box_layout.addWidget(self.q_scroll_area)

    def setWidget(self, q_widget: QWidget) -> None:
        self.q_scroll_area.setWidget(q_widget)
