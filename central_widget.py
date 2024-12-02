from psutil import FREEBSD, LINUX, MACOS, WINDOWS
from PySide6.QtWidgets import QSplitter, QStackedWidget, QVBoxLayout, QWidget

from menu import Menu
from screen import (
    cpu_freq,
    cpu_percent,
    cpu_stats,
    cpu_times,
    dashboard,
    disk_io_counters,
    disk_partitions,
    getloadavg,
    net_connections,
    net_if_stats,
    process_iter,
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
        self.addWidget("―", dashboard.Widget())

        # I/O
        self.addWidget("q_screen", q_screen.Widget())

        self.addWidget("q_camera_device", q_camera_device.Widget())

        self.addWidget("q_audio_device", q_input_device.Widget())

        self.addWidget("q_audio_device", q_input_device.Widget())

        self.addWidget("q_input_device", q_input_device.Widget())

        # =====================================================================
        # --- CPU related functions
        # =====================================================================
        self.addWidget("cpu_times", cpu_times.Widget())

        self.addWidget("cpu_percent", cpu_percent.Widget())

        self.addWidget("cpu_stats", cpu_stats.Widget())

        self.addWidget("cpu_freq", cpu_freq.Widget())

        self.addWidget("getloadavg", getloadavg.Widget())

        # =====================================================================
        # --- system memory related functions
        # =====================================================================
        self.addWidget("virtual_memory", virtual_memory.Widget())

        self.addWidget("swap_memory", swap_memory.Widget())

        # =====================================================================
        # --- disks/partitions related functions
        # =====================================================================
        self.addWidget("disk_partitions", disk_partitions.Widget())

        self.addWidget("disk_io_counters", disk_io_counters.Widget())

        # =====================================================================
        # --- network related functions
        # =====================================================================
        self.addWidget("net_if_stats", net_if_stats.Widget())

        self.addWidget("net_connections", net_connections.Widget())

        # =====================================================================
        # --- sensors
        # =====================================================================
        if LINUX or MACOS:
            self.addWidget("sensors_temperatures", sensors_temperatures.Widget())

        if LINUX:
            self.addWidget("sensors_fans", sensors_fans.Widget())

        if LINUX or WINDOWS or FREEBSD or MACOS:
            self.addWidget("sensors_battery", sensors_battery.Widget())

        # =====================================================================
        # --- other system related functions
        # =====================================================================
        self.addWidget("users", users.Widget())

        # Processes
        self.addWidget("process_iter", process_iter.Widget())

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

    def addWidget(self, accessible_text_role: str, q_widget: QWidget) -> None:
        q_stacked_widget_index = self.q_stacked_widget.addWidget(q_widget)
        self.menu.add(accessible_text_role, q_stacked_widget_index)
