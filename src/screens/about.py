from functools import partial

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices, QFont, QImage, QPixmap
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)

from custom.contents_path import contents_path
from environment import APP_PRODUCT_NAME, APP_URL, APP_VERSION


class Widget(QWidget):
    def __init__(self):
        super().__init__()
        q_stacked_layout = QStackedLayout(self)
        q_widget = QWidget()
        q_widget.setStyleSheet("background-color:#f6f6f6")
        q_v_box_layout = QVBoxLayout(q_widget)
        q_v_box_layout.setContentsMargins(0, 0, 0, 0)
        q_v_box_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        q_h_box_layout = QHBoxLayout()
        q_h_box_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        q_svg_widget = QLabel()
        q_svg_widget.setFixedSize(96, 96)
        q_image = QImage(96, 96, QImage.Format.Format_RGB32)
        q_image.load(str(contents_path("icon.png")))
        q_svg_widget.setPixmap(QPixmap(q_image))
        q_h_box_layout.addWidget(q_svg_widget)
        q_v_box_layout.addLayout(q_h_box_layout)
        q_label_0 = QLabel(APP_PRODUCT_NAME)
        q_font = q_label_0.font()
        q_font.setWeight(QFont.Weight.Medium)
        q_label_0.setFont(q_font)
        q_label_0.setAlignment(Qt.AlignmentFlag.AlignCenter)
        q_v_box_layout.addWidget(q_label_0)
        q_label_1 = QLabel(APP_VERSION)
        q_label_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        q_v_box_layout.addWidget(q_label_1)
        q_push_button = QPushButton("Homepage")
        q_push_button.setFixedHeight(36)
        q_push_button.pressed.connect(
            partial(QDesktopServices.openUrl, QUrl(APP_URL))
        )
        q_v_box_layout.addWidget(q_push_button)
        # Project Website
        # Report an issue
        q_label_3 = QLabel("Copyright © 2024 - 2025 Santos Vilanculos.")
        q_label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        q_v_box_layout.addWidget(q_label_3)
        q_stacked_layout.addWidget(q_widget)
        q_stacked_layout.addWidget(q_widget)
        q_stacked_layout.addWidget(q_widget)
        q_stacked_layout.addWidget(q_widget)
        q_stacked_layout.addWidget(q_widget)
        q_stacked_layout.addWidget(q_widget)
        q_stacked_layout.addWidget(q_widget)
        q_stacked_layout.addWidget(q_widget)
        q_stacked_layout.addWidget(q_widget)
        q_stacked_layout.addWidget(q_widget)
        q_stacked_layout.addWidget(q_widget)
        q_stacked_layout.addWidget(q_widget)
