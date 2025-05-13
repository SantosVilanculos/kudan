from functools import partial

import psutil
from PySide6.QtCore import QKeyCombination, QSize, Qt, QXmlStreamReader, Signal
from PySide6.QtGui import QKeySequence, QMouseEvent, QShortcut
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QSplitter,
    QSplitterHandle,
    QVBoxLayout,
    QWidget,
)

from screens import (
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

    def find_(self, q_string: str) -> None:
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
                    q_list_widget_item,
                    QAbstractItemView.ScrollHint.EnsureVisible,
                )


class SettingsButton(QFrame):
    pressed = Signal()

    def __init__(self):
        super().__init__()
        self.setFixedSize(40, 40)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setAttribute(Qt.WidgetAttribute.WA_NoMousePropagation)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        q_v_box_layout = QVBoxLayout(self)

        q_v_box_layout.setContentsMargins(0, 0, 0, 0)
        q_v_box_layout.setSpacing(0)

        q_svg_widget = QSvgWidget()
        q_svg_widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        q_svg_widget.setFixedSize(20, 20)

        q_svg_renderer = q_svg_widget.renderer()
        q_svg_renderer.load(
            QXmlStreamReader(
                """
<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true" data-slot="icon">
  <path stroke-linecap="round" stroke-linejoin="round" d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.325.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 0 1 1.37.49l1.296 2.247a1.125 1.125 0 0 1-.26 1.431l-1.003.827c-.293.241-.438.613-.43.992a7.723 7.723 0 0 1 0 .255c-.008.378.137.75.43.991l1.004.827c.424.35.534.955.26 1.43l-1.298 2.247a1.125 1.125 0 0 1-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.47 6.47 0 0 1-.22.128c-.331.183-.581.495-.644.869l-.213 1.281c-.09.543-.56.94-1.11.94h-2.594c-.55 0-1.019-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 0 1-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 0 1-1.369-.49l-1.297-2.247a1.125 1.125 0 0 1 .26-1.431l1.004-.827c.292-.24.437-.613.43-.991a6.932 6.932 0 0 1 0-.255c.007-.38-.138-.751-.43-.992l-1.004-.827a1.125 1.125 0 0 1-.26-1.43l1.297-2.247a1.125 1.125 0 0 1 1.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.086.22-.128.332-.183.582-.495.644-.869l.214-1.28Z"/>
  <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"/>
</svg>
        """
            )
        )
        q_svg_renderer.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)
        q_v_box_layout.addWidget(
            q_svg_widget, alignment=Qt.AlignmentFlag.AlignCenter
        )

    def mousePressEvent(self, event: QMouseEvent, /) -> None:
        self.pressed.emit()
        return super().mousePressEvent(event)


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

        q_h_box_layout = QHBoxLayout()
        q_line_edit = QLineEdit()
        q_line_edit.setFixedHeight(40)
        q_line_edit.setTextMargins(14, 0, 14, 0)
        self.focusQLineEdit.connect(q_line_edit.setFocus)
        q_h_box_layout.addWidget(q_line_edit, stretch=1)
        q_push_button = SettingsButton()
        q_push_button.pressed.connect(partial(self.toRoute.emit, "settings"))
        q_h_box_layout.addWidget(q_push_button, stretch=0)
        q_v_box_layout.addLayout(q_h_box_layout, stretch=0)

        menu = Menu()
        q_line_edit.textChanged.connect(menu.find_)
        self.redirectedTo.connect(menu.setSelected)
        menu.itemSelected.connect(
            lambda user_role: self.toRoute.emit(user_role)
        )
        menu.add("initial", "dashboard")
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
        q_splitter_handle = QSplitterHandle(
            q_splitter.orientation(), q_splitter
        )
        q_splitter_handle.setEnabled(False)
        q_splitter.createHandle = lambda: q_splitter_handle

        self.navigation = Navigation()
        q_splitter.addWidget(self.navigation)

        self.stack = Stack(initialRouteName="initial")
        self.stack.currentChanged.connect(
            lambda _: self.navigation.redirectedTo.emit(
                self.stack.currentName()
            )
        )
        self.navigation.toRoute.connect(
            lambda q_string: self.stack.navigate(q_string)
        )

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
            self.stack.addWidget(
                "sensors_temperatures", sensors_temperatures.Widget()
            )

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

        self.stack.addWidget("settings", settings.Widget())

        q_splitter.addWidget(self.stack)

        q_v_box_layout.addWidget(q_splitter)

        # =====================================================================
        # --- shortcuts
        # =====================================================================

        ctrl_b = QShortcut(
            QKeySequence(
                QKeyCombination(
                    Qt.KeyboardModifier.ControlModifier, Qt.Key.Key_B
                )
            ),
            self,
        )
        ctrl_b.activated.connect(
            lambda: self.navigation.setVisible(not self.navigation.isVisible())
        )

        ctrl_shift_f = QShortcut(
            QKeySequence(
                QKeyCombination(
                    Qt.KeyboardModifier.ControlModifier
                    | Qt.KeyboardModifier.ShiftModifier,
                    Qt.Key.Key_F,
                )
            ),
            self,
        )
        ctrl_shift_f.activated.connect(
            partial(self.focus, Qt.FocusReason.ShortcutFocusReason)
        )

        ctrl_q = QShortcut(
            QKeySequence(
                QKeyCombination(
                    Qt.KeyboardModifier.ControlModifier, Qt.Key.Key_Q
                )
            ),
            self,
        )
        ctrl_q.activated.connect(QApplication.quit)

        ctrl_comma = QShortcut(
            QKeySequence(
                QKeyCombination(
                    Qt.KeyboardModifier.ControlModifier, Qt.Key.Key_Comma
                )
            ),
            self,
        )
        ctrl_comma.activated.connect(lambda: self.stack.navigate("settings"))

    def focus(self, focus_reason: Qt.FocusReason):
        if self.navigation.isHidden():
            self.navigation.setVisible(True)
        self.navigation.focusQLineEdit.emit(focus_reason)
