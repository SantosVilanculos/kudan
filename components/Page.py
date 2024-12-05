from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QScrollArea,
    QSizePolicy,
    QStackedWidget,
    QWidget,
)


class Page(QScrollArea):
    def __init__(self):
        super().__init__()

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        q_widget = QWidget()
        q_h_box_layout = QHBoxLayout(q_widget)
        # q_h_box_layout.setContentsMargins(0, 0, 0, 0)
        q_h_box_layout.setSpacing(0)
        self.q_stacked_widget = QStackedWidget()
        self.q_stacked_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )
        self.q_stacked_widget.setMaximumWidth(640)
        q_h_box_layout.addWidget(self.q_stacked_widget)
        self.setWidget(q_widget)
