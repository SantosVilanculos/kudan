from PySide6.QtWidgets import QStackedLayout, QVBoxLayout, QWidget


class Widget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        q_stacked_layout = QStackedLayout(self)
        q_widget = QWidget()
        q_widget.setStyleSheet("background-color:#cc0000")
        q_v_box_layout = QVBoxLayout(q_widget)
        q_v_box_layout.setContentsMargins(0, 0, 0, 0)
        q_v_box_layout.setSpacing(0)
        q_stacked_layout.addWidget(q_widget)
