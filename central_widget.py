from functools import partial
from typing import Callable

from psutil import WINDOWS
from PySide6.QtCore import QMargins, QSize, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QSplitter,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from screen.network_interface_card import NetworkInterfaceCard
from screen.socket_connections import SocketConnections


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


class HStack(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.q_h_box_layout = QHBoxLayout(self)
        self.q_h_box_layout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.q_h_box_layout.setSpacing(0)

    def addWidget(self, q_widget: QWidget) -> None:
        self.q_h_box_layout.addWidget(q_widget)

    def removeWidget(self, q_widget: QWidget) -> None:
        self.q_h_box_layout.removeWidget(q_widget)

    def setContentsMargins(self, q_margins: QMargins):
        self.q_h_box_layout.setContentsMargins(q_margins)

    def setSpacing(self, spacing: int):
        self.q_h_box_layout.setSpacing(spacing)


class CentralWidget(QWidget):
    def __init__(self):
        super().__init__()
        q_v_box_layout = QVBoxLayout()
        q_v_box_layout.setContentsMargins(0, 0, 0, 0)
        q_v_box_layout.setSpacing(0)
        self.setLayout(q_v_box_layout)

        self.q_stacked_widget = QStackedWidget()

        q_splitter = QSplitter()
        q_splitter.setHandleWidth(1)
        q_splitter.setStyleSheet("QSplitter::handle{background-color:#E0E0E0}")

        self.q_list_widget = QListWidget()
        self.q_list_widget.setFixedWidth(256)
        self.q_list_widget.setStyleSheet("QListWidget{border:0}")
        self.q_list_widget.currentRowChanged.connect(
            self.q_list_widget_current_row_changed
        )
        q_stacked_widget_index = self.q_stacked_widget.addWidget(SocketConnections())
        self.q_list_widget_add_item("net_connections", q_stacked_widget_index)
        q_stacked_widget_index = self.q_stacked_widget.addWidget(NetworkInterfaceCard())
        self.q_list_widget_add_item("net_if_stats", q_stacked_widget_index)
        if WINDOWS:
            q_stacked_widget_index = self.q_stacked_widget.addWidget(QWidget())
            self.q_list_widget_add_item("win_service_iter", q_stacked_widget_index)
        q_stacked_widget_index = self.q_stacked_widget.addWidget(QWidget())
        self.q_list_widget_add_item("process_iter", q_stacked_widget_index)
        q_stacked_widget_index = self.q_stacked_widget.addWidget(QWidget())
        self.q_list_widget_add_item("cpu_stats", q_stacked_widget_index)
        q_stacked_widget_index = self.q_stacked_widget.addWidget(QWidget())
        self.q_list_widget_add_item("virtual_memory", q_stacked_widget_index)
        q_stacked_widget_index = self.q_stacked_widget.addWidget(QWidget())
        self.q_list_widget_add_item("swap_memory", q_stacked_widget_index)
        q_stacked_widget_index = self.q_stacked_widget.addWidget(QWidget())
        self.q_list_widget_add_item("disk_partitions", q_stacked_widget_index)
        q_stacked_widget_index = self.q_stacked_widget.addWidget(QWidget())
        self.q_list_widget_add_item("disk_io_counters", q_stacked_widget_index)
        q_splitter.addWidget(self.q_list_widget)

        q_splitter.addWidget(self.q_stacked_widget)
        q_splitter_index = q_splitter.indexOf(self.q_stacked_widget)
        if q_splitter_index > -1:
            q_splitter.setCollapsible(q_splitter_index, False)
            q_splitter.handle(1).setEnabled(False)

        q_v_box_layout.addWidget(q_splitter)

    def q_list_widget_current_row_changed(self, q_list_widget_row: int) -> None:
        q_list_widget_item = self.q_list_widget.item(q_list_widget_row)
        print(f'q_list_widget_item_tool_tip="{q_list_widget_item.toolTip()}"')

    def q_list_widget_add_item(self, text: str, q_stacked_widget_index: int) -> None:
        q_list_widget_item = QListWidgetItem()
        q_list_widget_item.setToolTip(text)
        q_list_widget_item.setSizeHint(QSize(0, 44))
        self.q_list_widget.addItem(q_list_widget_item)
        q_label = Label(
            partial(self.q_stacked_widget.setCurrentIndex, q_stacked_widget_index)
        )
        q_label.setText(text)
        self.q_list_widget.setItemWidget(q_list_widget_item, q_label)
        if self.q_list_widget.row(q_list_widget_item) == 0:
            q_list_widget_item.setSelected(True)
