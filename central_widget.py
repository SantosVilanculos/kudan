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

from screen import (
    boot_time,
    cpu_count,
    cpu_freq,
    cpu_percent,
    cpu_stats,
    cpu_times,
    disk_io_counters,
    disk_partitions,
    getloadavg,
    net_connections,
    net_if_stats,
    process_iter,
    q_input_device,
    q_screen,
    sensors_battery,
    sensors_fans,
    sensors_temperatures,
    swap_memory,
    test,
    users,
    virtual_memory,
)


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

        # Test
        q_stacked_widget_index = self.q_stacked_widget.addWidget(test.Widget())
        self.q_list_widget_add_item("test", q_stacked_widget_index)

        # I/O
        q_stacked_widget_index = self.q_stacked_widget.addWidget(q_screen.Widget())
        self.q_list_widget_add_item("q_screen", q_stacked_widget_index)

        q_stacked_widget_index = self.q_stacked_widget.addWidget(
            q_input_device.Widget()
        )
        self.q_list_widget_add_item("q_input_device", q_stacked_widget_index)

        # CPU
        q_stacked_widget_index = self.q_stacked_widget.addWidget(cpu_times.Widget())
        self.q_list_widget_add_item("cpu_times", q_stacked_widget_index)

        q_stacked_widget_index = self.q_stacked_widget.addWidget(cpu_percent.Widget())
        self.q_list_widget_add_item("cpu_percent", q_stacked_widget_index)

        q_stacked_widget_index = self.q_stacked_widget.addWidget(cpu_count.Widget())
        self.q_list_widget_add_item("cpu_count", q_stacked_widget_index)

        q_stacked_widget_index = self.q_stacked_widget.addWidget(cpu_stats.Widget())
        self.q_list_widget_add_item("cpu_stats", q_stacked_widget_index)

        q_stacked_widget_index = self.q_stacked_widget.addWidget(cpu_freq.Widget())
        self.q_list_widget_add_item("cpu_freq", q_stacked_widget_index)

        q_stacked_widget_index = self.q_stacked_widget.addWidget(getloadavg.Widget())
        self.q_list_widget_add_item("getloadavg", q_stacked_widget_index)

        # Memory
        q_stacked_widget_index = self.q_stacked_widget.addWidget(
            virtual_memory.Widget()
        )
        self.q_list_widget_add_item("virtual_memory", q_stacked_widget_index)

        q_stacked_widget_index = self.q_stacked_widget.addWidget(swap_memory.Widget())
        self.q_list_widget_add_item("swap_memory", q_stacked_widget_index)

        # Disk
        q_stacked_widget_index = self.q_stacked_widget.addWidget(
            disk_partitions.Widget()
        )
        self.q_list_widget_add_item("disk_partitions", q_stacked_widget_index)

        q_stacked_widget_index = self.q_stacked_widget.addWidget(
            disk_io_counters.Widget()
        )
        self.q_list_widget_add_item("disk_io_counters", q_stacked_widget_index)

        # Network
        q_stacked_widget_index = self.q_stacked_widget.addWidget(net_if_stats.Widget())
        self.q_list_widget_add_item("net_if_stats", q_stacked_widget_index)

        q_stacked_widget_index = self.q_stacked_widget.addWidget(
            net_connections.Widget()
        )
        self.q_list_widget_add_item("net_connections", q_stacked_widget_index)

        # Sensors
        q_stacked_widget_index = self.q_stacked_widget.addWidget(
            sensors_temperatures.Widget()
        )
        self.q_list_widget_add_item("sensors_temperatures", q_stacked_widget_index)

        q_stacked_widget_index = self.q_stacked_widget.addWidget(sensors_fans.Widget())
        self.q_list_widget_add_item("sensors_fans", q_stacked_widget_index)

        q_stacked_widget_index = self.q_stacked_widget.addWidget(
            sensors_battery.Widget()
        )
        self.q_list_widget_add_item("sensors_battery", q_stacked_widget_index)

        # Other system info
        q_stacked_widget_index = self.q_stacked_widget.addWidget(boot_time.Widget())
        self.q_list_widget_add_item("boot_time", q_stacked_widget_index)

        q_stacked_widget_index = self.q_stacked_widget.addWidget(users.Widget())
        self.q_list_widget_add_item("users", q_stacked_widget_index)

        # Processes
        q_stacked_widget_index = self.q_stacked_widget.addWidget(process_iter.Widget())
        self.q_list_widget_add_item("process_iter", q_stacked_widget_index)

        # Windows services
        if WINDOWS:
            q_stacked_widget_index = self.q_stacked_widget.addWidget(QWidget())
            self.q_list_widget_add_item("win_service_iter", q_stacked_widget_index)

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
