from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import (
    QLabel,
    QListWidget,
    QListWidgetItem,
    QSplitter,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from network_interface_card import NetworkInterfaceCard
from socket_connections import SocketConnections


class Label(QLabel):
    def __init__(self, q_stacked_widget: QStackedWidget, index: int):
        super().__init__()
        self.q_stacked_widget = q_stacked_widget
        self.index = index

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.q_stacked_widget.setCurrentIndex(self.index)
        return super().mousePressEvent(event)


class CW(QWidget):
    def __init__(self) -> None:
        super().__init__()

        v = QVBoxLayout(self)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(0)

        q_splitter = QSplitter()
        q_splitter.setStyleSheet("QSplitter::handle{background-color:#e0e0e0}")
        q_splitter.setHandleWidth(1)

        q_widget = QWidget()
        q_widget.setFixedWidth(240)
        q_v_box_layout = QVBoxLayout(q_widget)
        q_v_box_layout.setContentsMargins(0, 0, 0, 0)
        q_v_box_layout.setSpacing(0)
        # h = QWidget()
        # h.setFixedHeight(44)
        # h.setStyleSheet(
        #     "QWidget{border-bottom:1px solid #e0e0e0;background-color:#fff}"
        # )
        # q_v_box_layout.addWidget(h)
        self.q_list_widget = QListWidget()
        # self.q_list_widget.setStyleSheet("QListWidget{border:0}")
        q_v_box_layout.addWidget(self.q_list_widget)
        q_splitter.addWidget(q_widget)

        self.q_stacked_widget = QStackedWidget()
        q_splitter.addWidget(self.q_stacked_widget)

        self.b("Socket connections", SocketConnections())
        self.b("Network Interface Cards", NetworkInterfaceCard())

        v.addWidget(q_splitter)

    def b(self, name: str, widget: QWidget) -> None:
        index = self.q_stacked_widget.addWidget(widget)

        q_list_widget_item = QListWidgetItem()
        q_list_widget_item.setSizeHint(QSize(0, 44))
        self.q_list_widget.addItem(q_list_widget_item)
        label = Label(self.q_stacked_widget, index)
        label.setStyleSheet("QLabel{padding-left:14px;padding-right:14px}")
        label.setText(name)
        self.q_list_widget.setItemWidget(q_list_widget_item, label)
