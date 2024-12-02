from psutil import FREEBSD, LINUX, MACOS, WINDOWS
from PySide6.QtWidgets import QSplitter, QStackedWidget, QVBoxLayout, QWidget

from menu import Menu
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

        self.menu = Menu()
        self.q_stacked_widget = QStackedWidget()
        self.menu.itemActivated.connect(
            lambda user_data: self.q_stacked_widget.setCurrentIndex(int(user_data))
        )
        q_splitter = QSplitter()
        q_splitter.setHandleWidth(1)
        q_splitter.setStyleSheet("QSplitter::handle{background-color:#E0E0E0}")

        # index
        q_stacked_widget_index = self.q_stacked_widget.addWidget(QWidget())
        self.menu.add("―", q_stacked_widget_index)

        # I/O
        q_stacked_widget_index = self.q_stacked_widget.addWidget(q_screen.Widget())
        self.menu.add("q_screen", q_stacked_widget_index)

        q_stacked_widget_index = self.q_stacked_widget.addWidget(
            q_camera_device.Widget()
        )
        self.menu.add("q_camera_device", q_stacked_widget_index)

        q_stacked_widget_index = self.q_stacked_widget.addWidget(
            q_audio_device.Widget()
        )
        self.menu.add("q_audio_device", q_stacked_widget_index)

        q_stacked_widget_index = self.q_stacked_widget.addWidget(
            q_input_device.Widget()
        )
        self.menu.add("q_input_device", q_stacked_widget_index)

        # =====================================================================
        # --- CPU related functions
        # =====================================================================
        q_stacked_widget_index = self.q_stacked_widget.addWidget(cpu_times.Widget())
        self.menu.add("cpu_times", q_stacked_widget_index)

        q_stacked_widget_index = self.q_stacked_widget.addWidget(cpu_percent.Widget())
        self.menu.add("cpu_percent", q_stacked_widget_index)

        q_stacked_widget_index = self.q_stacked_widget.addWidget(cpu_count.Widget())
        self.menu.add("cpu_count", q_stacked_widget_index)

        q_stacked_widget_index = self.q_stacked_widget.addWidget(cpu_stats.Widget())
        self.menu.add("cpu_stats", q_stacked_widget_index)

        q_stacked_widget_index = self.q_stacked_widget.addWidget(cpu_freq.Widget())
        self.menu.add("cpu_freq", q_stacked_widget_index)

        q_stacked_widget_index = self.q_stacked_widget.addWidget(getloadavg.Widget())
        self.menu.add("getloadavg", q_stacked_widget_index)

        # =====================================================================
        # --- system memory related functions
        # =====================================================================
        q_stacked_widget_index = self.q_stacked_widget.addWidget(
            virtual_memory.Widget()
        )
        self.menu.add("virtual_memory", q_stacked_widget_index)

        q_stacked_widget_index = self.q_stacked_widget.addWidget(swap_memory.Widget())
        self.menu.add("swap_memory", q_stacked_widget_index)

        # =====================================================================
        # --- disks/partitions related functions
        # =====================================================================
        q_stacked_widget_index = self.q_stacked_widget.addWidget(
            disk_partitions.Widget()
        )
        self.menu.add("disk_partitions", q_stacked_widget_index)

        q_stacked_widget_index = self.q_stacked_widget.addWidget(
            disk_io_counters.Widget()
        )
        self.menu.add("disk_io_counters", q_stacked_widget_index)

        # =====================================================================
        # --- network related functions
        # =====================================================================
        q_stacked_widget_index = self.q_stacked_widget.addWidget(net_if_stats.Widget())
        self.menu.add("net_if_stats", q_stacked_widget_index)

        q_stacked_widget_index = self.q_stacked_widget.addWidget(
            net_connections.Widget()
        )
        self.menu.add("net_connections", q_stacked_widget_index)

        # =====================================================================
        # --- sensors
        # =====================================================================
        if LINUX or MACOS:
            q_stacked_widget_index = self.q_stacked_widget.addWidget(
                sensors_temperatures.Widget()
            )
            self.menu.add("sensors_temperatures", q_stacked_widget_index)

        if LINUX:
            q_stacked_widget_index = self.q_stacked_widget.addWidget(
                sensors_fans.Widget()
            )
            self.menu.add("sensors_fans", q_stacked_widget_index)

        if LINUX or WINDOWS or FREEBSD or MACOS:
            q_stacked_widget_index = self.q_stacked_widget.addWidget(
                sensors_battery.Widget()
            )
            self.menu.add("sensors_battery", q_stacked_widget_index)

        # =====================================================================
        # --- other system related functions
        # =====================================================================
        q_stacked_widget_index = self.q_stacked_widget.addWidget(boot_time.Widget())
        self.menu.add("boot_time", q_stacked_widget_index)

        q_stacked_widget_index = self.q_stacked_widget.addWidget(users.Widget())
        self.menu.add("users", q_stacked_widget_index)

        # Processes
        q_stacked_widget_index = self.q_stacked_widget.addWidget(process_iter.Widget())
        self.menu.add("process_iter", q_stacked_widget_index)

        # =====================================================================
        # --- Windows services
        # =====================================================================
        if WINDOWS:
            # TODO: Implement functionality
            q_stacked_widget_index = self.q_stacked_widget.addWidget(QWidget())
            self.menu.add("win_service_iter", q_stacked_widget_index)

        q_splitter.addWidget(self.menu)

        q_splitter.addWidget(self.q_stacked_widget)
        q_splitter_index = q_splitter.indexOf(self.q_stacked_widget)
        if q_splitter_index > -1:
            q_splitter.setCollapsible(q_splitter_index, False)
            q_splitter.handle(1).setEnabled(False)

        q_v_box_layout.addWidget(q_splitter)
