from functools import partial
from typing import Callable

from PySide6.QtCore import QMargins, QSize, Qt
from PySide6.QtGui import QIcon, QMouseEvent
from PySide6.QtWidgets import (
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QSplitter,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from env import APPLICATION_NAME, contents_directory_path
from network_interface_card import NetworkInterfaceCard
from socket_connections import SocketConnections


class Label(QLabel):
    def __init__(self, function: Callable) -> None:
        super().__init__()

        self.function = function

        self.setStyleSheet("QLabel{padding-left:4px;padding-right:4px}")

    def mousePressEvent(self, q_mouse_event: QMouseEvent) -> None:
        if q_mouse_event.button() == Qt.MouseButton.LeftButton:
            self.function()
        return super().mousePressEvent(q_mouse_event)


class VStack(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.q_v_box_layout = QVBoxLayout(self)
        self.q_v_box_layout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.q_v_box_layout.setSpacing(0)

    def addWidget(self, q_widget: QWidget) -> None:
        self.q_v_box_layout.addWidget(q_widget)

    def removeWidget(self, q_widget: QWidget) -> None:
        self.q_v_box_layout.removeWidget(q_widget)

    def setContentsMargins(self, q_margins: QMargins):
        self.q_v_box_layout.setContentsMargins(q_margins)

    def setSpacing(self, spacing: int):
        self.q_v_box_layout.setSpacing(spacing)


class Window(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        cdp = contents_directory_path()

        self.setWindowIcon(QIcon(str(cdp.joinpath("icon.ico"))))
        self.setWindowTitle(APPLICATION_NAME)
        self.setMinimumSize(QSize(640, 360))

        self.q_stacked_widget = QStackedWidget()

        q_splitter = QSplitter()
        q_splitter.setHandleWidth(1)
        q_splitter.setStyleSheet("QSplitter::handle{background-color:#E0E0E0}")

        v_stack = VStack()
        v_stack.setFixedWidth(256)
        _ = QWidget()
        _.setStyleSheet(
            "QWidget{border-bottom:1px solid #E0E0E0;background-color:#FAFAFA}"
        )
        _.setFixedHeight(44)
        v_stack.addWidget(_)
        self.q_list_widget = QListWidget()
        self.q_list_widget.setStyleSheet("QListWidget{border:0}")
        q_stacked_widget_index = self.q_stacked_widget.addWidget(SocketConnections())
        self.q_list_widget_add_item("net_connections()", q_stacked_widget_index)
        q_stacked_widget_index = self.q_stacked_widget.addWidget(NetworkInterfaceCard())
        self.q_list_widget_add_item("net_if_stats()", q_stacked_widget_index)
        v_stack.addWidget(self.q_list_widget)
        q_splitter.addWidget(v_stack)

        v_stack = VStack()
        _ = QWidget()
        _.setStyleSheet(
            "QWidget{border-bottom:1px solid #E0E0E0;background-color:#FAFAFA}"
        )
        _.setFixedHeight(44)
        v_stack.addWidget(_)
        v_stack.addWidget(self.q_stacked_widget)
        q_splitter.addWidget(v_stack)
        q_splitter_index = q_splitter.indexOf(v_stack)
        if q_splitter_index > -1:
            q_splitter.setCollapsible(q_splitter_index, False)

        self.setCentralWidget(q_splitter)

    def q_list_widget_add_item(self, text: str, q_stacked_widget_index: int) -> None:
        q_list_widget_item = QListWidgetItem()
        q_list_widget_item.setSizeHint(QSize(0, 44))
        self.q_list_widget.addItem(q_list_widget_item)
        q_label = Label(
            partial(self.q_stacked_widget.setCurrentIndex, q_stacked_widget_index)
        )
        q_label.setText(text)
        self.q_list_widget.setItemWidget(q_list_widget_item, q_label)
        if self.q_list_widget.row(q_list_widget_item) == 0:
            q_list_widget_item.setSelected(True)
