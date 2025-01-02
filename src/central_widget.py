from functools import partial

import psutil
from PySide6.QtCore import QKeyCombination, Qt
from PySide6.QtGui import QShortcut
from PySide6.QtWidgets import QApplication, QSplitter, QVBoxLayout, QWidget

from components.ui.stack import Navigator
from menu import Menu
from screens import (
    CPU,
    Memory,
    boot_time,
    disk_io_counters,
    disk_partitions,
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
    users,
    win_service_iter,
)


class CentralWidget(QWidget):
    def __init__(self):
        super().__init__()

        q_v_box_layout = QVBoxLayout()
        q_v_box_layout.setContentsMargins(0, 0, 0, 0)
        q_v_box_layout.setSpacing(0)
        self.setLayout(q_v_box_layout)

        q_splitter = QSplitter()
        q_splitter.setHandleWidth(1)
        q_splitter.setChildrenCollapsible(False)

        self.menu = Menu()
        self.navigator = Navigator()
        self.menu.currentItemChanged.connect(
            lambda index: self.navigator.setCurrentIndex(int(index))
        )

        q_shortcut_0 = QShortcut(
            QKeyCombination(Qt.KeyboardModifier.ControlModifier, Qt.Key.Key_B), self
        )
        q_shortcut_0.activated.connect(
            lambda: self.menu.setVisible(not self.menu.isVisible())
        )
        q_shortcut_1 = QShortcut(
            QKeyCombination(
                Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.ShiftModifier,
                Qt.Key.Key_F,
            ),
            self,
        )
        q_shortcut_1.activated.connect(
            partial(self.menu.focusQLineEdit.emit, Qt.FocusReason.ShortcutFocusReason)
        )
        q_shortcut_2 = QShortcut(
            QKeyCombination(Qt.KeyboardModifier.ControlModifier, Qt.Key.Key_Q), self
        )
        q_shortcut_2.activated.connect(QApplication.quit)
        self.addWidget("boot_time", boot_time.Widget())

        # =====================================================================
        # --- CPU related functions
        # =====================================================================
        self.addWidget("cpu", CPU.CPU())

        # =====================================================================
        # --- system memory related functions
        # =====================================================================
        self.addWidget("memory", Memory.Memory())

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
        if psutil.LINUX or psutil.MACOS:
            self.addWidget("sensors_temperatures", sensors_temperatures.Widget())

        if psutil.LINUX:
            self.addWidget("sensors_fans", sensors_fans.Widget())

        if psutil.LINUX or psutil.WINDOWS or psutil.FREEBSD or psutil.MACOS:
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
        if psutil.WINDOWS:
            # TODO: Implement functionality
            self.addWidget("win_service_iter", win_service_iter.Widget())

        q_splitter.addWidget(self.menu)

        q_splitter.addWidget(self.navigator)
        index = q_splitter.indexOf(self.navigator)
        if index > -1:
            q_splitter.handle(index).setEnabled(False)

        q_v_box_layout.addWidget(q_splitter)

        # I/O
        self.addWidget("screen", q_screen.Widget())

        self.addWidget("camera_device", q_camera_device.Widget())

        self.addWidget("audio_device", q_audio_device.Widget())

        self.addWidget("input_device", q_input_device.Widget())

    def addWidget(self, accessible_text_role: str, q_widget: QWidget) -> None:
        index = self.navigator.addWidget(accessible_text_role, q_widget)
        self.menu.add(accessible_text_role, index)
