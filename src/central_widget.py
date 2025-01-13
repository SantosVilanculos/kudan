from functools import partial

import psutil
from PySide6.QtCore import QKeyCombination, QSize, Qt, Signal
from PySide6.QtGui import QShortcut
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QGridLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSplitter,
    QSplitterHandle,
    QVBoxLayout,
    QWidget,
)

from screens import (
    about,
    cpu,
    disk_io_counters,
    disk_partitions,
    initial,
    memory,
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
    settings,
    users,
    win_service_iter,
)
from ui.stack import Stack


class Menu(QListWidget):
    itemSelected = Signal(str)

    def __init__(self):
        super().__init__()

        self.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.itemActivated.connect(
            lambda q_list_widget_item: self.itemSelected.emit(
                str(q_list_widget_item.data(Qt.ItemDataRole.UserRole))
            )
        )
        self.itemClicked.connect(
            lambda q_list_widget_item: self.itemSelected.emit(
                str(q_list_widget_item.data(Qt.ItemDataRole.UserRole))
            )
        )

    def add(self, user_role: str, accessible_text_role: str) -> None:
        q_list_widget_item = QListWidgetItem(self)
        q_list_widget_item.setData(
            Qt.ItemDataRole.AccessibleTextRole, accessible_text_role
        )
        q_list_widget_item.setData(Qt.ItemDataRole.UserRole, user_role)
        q_list_widget_item.setSizeHint(QSize(0, 44))

        q_label = QLabel(accessible_text_role.upper())
        # q_font = q_label.font()
        # q_font.setWeight(QFont.Weight.Medium)
        # q_label.setFont(q_font)
        q_label.setContentsMargins(14, 0, 14, 0)

        self.setItemWidget(q_list_widget_item, q_label)

    def find(self, q_string: str) -> None:
        for index in range(self.count()):
            q_list_widget_item = self.item(index)

            accessible_text_role = q_list_widget_item.data(
                Qt.ItemDataRole.AccessibleTextRole
            )

            if not isinstance(accessible_text_role, str):
                return None

            q_list_widget_item.setHidden(
                accessible_text_role.lower().find(q_string.lower()) == -1
            )

    def setSelected(self, q_string: str) -> None:
        self.clearSelection()

        for index in range(self.count()):
            q_list_widget_item = self.item(index)

            user_role = q_list_widget_item.data(Qt.ItemDataRole.UserRole)

            if not isinstance(user_role, str):
                return None

            if user_role == q_string:
                q_list_widget_item.setSelected(True)
                self.scrollToItem(
                    q_list_widget_item, QAbstractItemView.ScrollHint.EnsureVisible
                )


class Navigation(QWidget):
    toRoute = Signal(str)
    focusQLineEdit = Signal(Qt.FocusReason)
    redirectedTo = Signal(str)

    def __init__(self):
        super().__init__()
        self.setFixedWidth(240)

        q_v_box_layout = QVBoxLayout(self)
        q_v_box_layout.setContentsMargins(0, 0, 0, 0)
        q_v_box_layout.setSpacing(0)

        q_line_edit = QLineEdit()
        q_line_edit.setFixedHeight(40)
        q_line_edit.setTextMargins(14, 0, 14, 0)
        self.focusQLineEdit.connect(q_line_edit.setFocus)
        q_v_box_layout.addWidget(q_line_edit, alignment=Qt.AlignmentFlag.AlignTop)

        menu = Menu()
        q_line_edit.textChanged.connect(menu.find)
        self.redirectedTo.connect(menu.setSelected)
        menu.itemSelected.connect(lambda user_role: self.toRoute.emit(user_role))
        menu.add("cpu", "cpu")
        menu.add("memory", "memory")
        menu.add("disk_partitions", "Disk Partition")
        menu.add("disk_io_counters", "Disk IO Counter")
        menu.add("net_if_stats", "NIC")
        menu.add("net_connections", "Socket connection")
        if psutil.LINUX or psutil.FREEBSD:
            menu.add("sensors_temperatures", "Temperature")
        if psutil.LINUX:
            menu.add("sensors_fans", "Fan")
        if psutil.LINUX or psutil.WINDOWS or psutil.FREEBSD or psutil.MACOS:
            menu.add("sensors_battery", "Battery")
        menu.add("users", "User")
        menu.add("process_iter", "Process")
        if psutil.WINDOWS:
            menu.add("win_service_iter", "Windows service")
        menu.add("screen", "Screen")
        menu.add("camera_device", "Camera device")
        menu.add("audio_device", "Audio device")
        menu.add("input_device", "Input device")
        q_v_box_layout.addWidget(menu)

        q_grid_layout = QGridLayout()
        q_push_button_0 = QPushButton()
        q_push_button_0.clicked.connect(partial(self.toRoute.emit, "initial"))
        q_push_button_0.setFixedHeight(40)
        q_grid_layout.addWidget(q_push_button_0, 0, 0)
        q_push_button_1 = QPushButton()
        q_push_button_1.clicked.connect(partial(self.toRoute.emit, "settings"))
        q_push_button_1.setFixedHeight(40)
        q_grid_layout.addWidget(q_push_button_1, 0, 1)
        q_push_button_2 = QPushButton()
        q_push_button_2.clicked.connect(partial(self.toRoute.emit, "about"))
        q_push_button_2.setFixedHeight(40)
        q_grid_layout.addWidget(q_push_button_2, 0, 2)
        q_v_box_layout.addLayout(q_grid_layout)


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
        q_splitter_handle = QSplitterHandle(q_splitter.orientation(), q_splitter)
        q_splitter_handle.setEnabled(False)
        q_splitter.createHandle = lambda: q_splitter_handle

        self.navigation = Navigation()
        q_splitter.addWidget(self.navigation)

        self.stack = Stack(initialRouteName="initial")
        self.stack.currentChanged.connect(
            lambda _: self.navigation.redirectedTo.emit(self.stack.currentName())
        )
        self.navigation.toRoute.connect(lambda q_string: self.stack.navigate(q_string))

        self.stack.addWidget("initial", initial.Widget())

        # =====================================================================
        # --- CPU related functions
        # =====================================================================
        self.stack.addWidget("cpu", cpu.Widget())

        # =====================================================================
        # --- system memory related functions
        # =====================================================================
        self.stack.addWidget("memory", memory.Widget())

        # =====================================================================
        # --- disks/partitions related functions
        # =====================================================================
        self.stack.addWidget("disk_partitions", disk_partitions.Widget())
        self.stack.addWidget("disk_io_counters", disk_io_counters.Widget())

        # =====================================================================
        # --- network related functions
        # =====================================================================
        self.stack.addWidget("net_if_stats", net_if_stats.Widget())
        self.stack.addWidget("net_connections", net_connections.Widget())

        # =====================================================================
        # --- sensors
        # =====================================================================
        if psutil.LINUX or psutil.FREEBSD:
            self.stack.addWidget("sensors_temperatures", sensors_temperatures.Widget())

        if psutil.LINUX:
            self.stack.addWidget("sensors_fans", sensors_fans.Widget())

        if psutil.LINUX or psutil.WINDOWS or psutil.FREEBSD:
            self.stack.addWidget("sensors_battery", sensors_battery.Widget())

        # =====================================================================
        # --- other system related functions
        # =====================================================================
        self.stack.addWidget("users", users.Widget())

        # Processes
        # =====================================================================
        # --- Processes
        # =====================================================================
        self.stack.addWidget("process_iter", process_iter.Widget())

        # =====================================================================
        # --- Windows services
        # =====================================================================
        if psutil.WINDOWS:
            self.stack.addWidget("win_service_iter", win_service_iter.Widget())

        # =====================================================================
        # --- I/O
        # =====================================================================

        self.stack.addWidget("screen", q_screen.Widget())
        self.stack.addWidget("camera_device", q_camera_device.Widget())
        self.stack.addWidget("audio_device", q_audio_device.Widget())
        self.stack.addWidget("input_device", q_input_device.Widget())

        # =====================================================================
        # --- others
        # =====================================================================

        self.stack.addWidget("about", about.Widget())
        self.stack.addWidget("settings", settings.Widget())

        q_splitter.addWidget(self.stack)

        q_v_box_layout.addWidget(q_splitter)

        #
        q_shortcut_0 = QShortcut(
            QKeyCombination(Qt.KeyboardModifier.ControlModifier, Qt.Key.Key_B), self
        )
        q_shortcut_0.activated.connect(
            lambda: self.navigation.setVisible(not self.navigation.isVisible())
        )
        q_shortcut_1 = QShortcut(
            QKeyCombination(
                Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.ShiftModifier,
                Qt.Key.Key_F,
            ),
            self,
        )
        q_shortcut_1.activated.connect(
            partial(self.focus, Qt.FocusReason.ShortcutFocusReason)
        )
        q_shortcut_2 = QShortcut(
            QKeyCombination(Qt.KeyboardModifier.ControlModifier, Qt.Key.Key_Q), self
        )
        q_shortcut_2.activated.connect(QApplication.quit)
        q_shortcut_3 = QShortcut(
            QKeyCombination(Qt.KeyboardModifier.ControlModifier, Qt.Key.Key_Comma), self
        )
        q_shortcut_3.activated.connect(lambda: self.stack.navigate("settings"))

    def focus(self, focus_reason: Qt.FocusReason):
        if self.navigation.isHidden():
            self.navigation.setVisible(True)
        self.navigation.focusQLineEdit.emit(focus_reason)
