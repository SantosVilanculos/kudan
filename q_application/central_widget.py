from psutil import WINDOWS
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
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
    q_audio_device,
    q_camera_device,
    q_input_device,
    q_screen,
    sensors_battery,
    sensors_fans,
    sensors_temperatures,
    swap_memory,
    users,
    virtual_memory,
)


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

        self.q_list_widget.itemActivated.connect(
            lambda q_list_widget_item: self.q_stacked_widget.setCurrentIndex(
                int(q_list_widget_item.data(Qt.ItemDataRole.UserRole))
            )
        )

        self.q_list_widget.itemClicked.connect(
            lambda q_list_widget_item: self.q_stacked_widget.setCurrentIndex(
                int(q_list_widget_item.data(Qt.ItemDataRole.UserRole))
            )
        )

        # index
        q_stacked_widget_index = self.q_stacked_widget.addWidget(QWidget())
        self.q_list_widget_add_item("index", q_stacked_widget_index)

        # I/O
        q_stacked_widget_index = self.q_stacked_widget.addWidget(q_screen.Widget())
        self.q_list_widget_add_item("q_screen", q_stacked_widget_index)

        q_stacked_widget_index = self.q_stacked_widget.addWidget(
            q_camera_device.Widget()
        )
        self.q_list_widget_add_item("q_camera_device", q_stacked_widget_index)

        q_stacked_widget_index = self.q_stacked_widget.addWidget(
            q_audio_device.Widget()
        )
        self.q_list_widget_add_item("q_audio_device", q_stacked_widget_index)

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
            # TODO: Implement functionality
            q_stacked_widget_index = self.q_stacked_widget.addWidget(QWidget())
            self.q_list_widget_add_item("win_service_iter", q_stacked_widget_index)

        q_splitter.addWidget(self.q_list_widget)

        q_splitter.addWidget(self.q_stacked_widget)
        q_splitter_index = q_splitter.indexOf(self.q_stacked_widget)
        if q_splitter_index > -1:
            q_splitter.setCollapsible(q_splitter_index, False)
            q_splitter.handle(1).setEnabled(False)

        q_v_box_layout.addWidget(q_splitter)

    def q_list_widget_add_item(self, text: str, q_stacked_widget_index: int) -> None:
        q_list_widget_item = QListWidgetItem()
        q_list_widget_item.setData(Qt.ItemDataRole.UserRole, q_stacked_widget_index)
        q_list_widget_item.setToolTip(text)
        q_list_widget_item.setSizeHint(QSize(0, 44))
        self.q_list_widget.addItem(q_list_widget_item)
        q_label = QLabel(text)
        q_label.setStyleSheet("QLabel{padding-left:4px;padding-right:4px}")
        self.q_list_widget.setItemWidget(q_list_widget_item, q_label)
        if self.q_list_widget.row(q_list_widget_item) == 0:
            q_list_widget_item.setSelected(True)
