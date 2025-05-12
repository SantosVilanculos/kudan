from PySide6.QtWidgets import (
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from screens.about import Tab3

# from screens.general import Tab1
from screens.keybindings import Tab2


class Widget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        q_v_box_layout = QVBoxLayout(self)
        q_v_box_layout.setContentsMargins(0, 0, 0, 0)
        q_v_box_layout.setSpacing(0)
        self.q_tab_widget = QTabWidget()
        self.q_tab_bar = self.q_tab_widget.tabBar()
        self.q_tab_bar.setDocumentMode(True)
        # self.q_tab_widget.addTab(Tab1(), "General")
        self.q_tab_widget.addTab(Tab2(), "Keyboard shortcuts")
        self.q_tab_widget.addTab(Tab3(), "About")
        q_v_box_layout.addWidget(self.q_tab_widget)
