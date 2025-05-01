import psutil
import psutil._common
from custom.function import file_size
from custom.os import OS
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import (QColor, QFont, QHideEvent, QPainter, QPaintEvent,
                           QShowEvent)
from PySide6.QtWidgets import (QFormLayout, QHBoxLayout, QLabel, QProgressBar,
                               QScrollArea, QSizePolicy, QStyle, QStyleOption,
                               QVBoxLayout, QWidget)
from ui.divider import Divider


class VirtualMemory(QWidget):
    def __init__(self) -> None:
        super().__init__()

        q_color = QColor(Qt.GlobalColor.lightGray)
        self.setObjectName("name")
        self.setStyleSheet(
            f"#name{{border:1px solid {q_color.name()};background-color:white}}"
        )

        q_v_box_layout = QVBoxLayout(self)
        q_v_box_layout.setSpacing(24)

        q_label = QLabel("virtual_memory")
        q_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        q_font = q_label.font()
        q_font.setWeight(QFont.Weight.Medium)
        q_label.setFont(q_font)
        q_v_box_layout.addWidget(q_label)

        self.q_progress_bar = QProgressBar()
        self.q_progress_bar.setFixedHeight(24)
        self.q_progress_bar.setMaximum(100)
        self.q_progress_bar.setTextVisible(False)
        self.q_progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        q_v_box_layout.addWidget(self.q_progress_bar)

        q_form_layout = QFormLayout()
        q_form_layout.setSpacing(24)

        self.total = QLabel("―")
        self.total.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("total", self.total)

        self.available = QLabel("―")
        self.available.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("available", self.available)

        self.percent = QLabel("―")
        self.percent.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("percent", self.percent)

        self.used = QLabel("―")
        self.used.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("used", self.used)
        self.free = QLabel("―")
        self.free.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("free", self.free)

        if OS.LINUX or OS.MACOS:
            self.active = QLabel("―")
            self.active.setAlignment(Qt.AlignmentFlag.AlignRight)
            q_form_layout.addRow("active", self.active)

            self.inactive = QLabel("―")
            self.inactive.setAlignment(Qt.AlignmentFlag.AlignRight)
            q_form_layout.addRow("inactive", self.inactive)

        if OS.LINUX or OS.BSD:
            self.buffers = QLabel("―")
            self.buffers.setAlignment(Qt.AlignmentFlag.AlignRight)
            q_form_layout.addRow("buffers", self.buffers)

            self.cached = QLabel("―")
            self.cached.setAlignment(Qt.AlignmentFlag.AlignRight)
            q_form_layout.addRow("cached", self.cached)

            self.shared = QLabel("―")
            self.shared.setAlignment(Qt.AlignmentFlag.AlignRight)
            q_form_layout.addRow("shared", self.shared)

        if OS.LINUX:
            self.slab = QLabel("―")
            self.slab.setAlignment(Qt.AlignmentFlag.AlignRight)
            q_form_layout.addRow("slab", self.slab)

        if OS.BSD or OS.MACOS:
            self.wired = QLabel("―")
            self.wired.setAlignment(Qt.AlignmentFlag.AlignRight)
            q_form_layout.addRow("wired", self.wired)

        q_v_box_layout.addLayout(q_form_layout)

    def update(self) -> None:
        svirtualmemory = psutil.virtual_memory()

        self.q_progress_bar.setValue(int(svirtualmemory.percent))

        self.total.setText(file_size(svirtualmemory.total))
        self.available.setText(file_size(svirtualmemory.available))
        self.percent.setText(f"{svirtualmemory.percent}%")
        self.used.setText(file_size(svirtualmemory.used))
        self.free.setText(file_size(svirtualmemory.free))

        if OS.LINUX or OS.MACOS:
            self.active.setText(file_size(svirtualmemory.active))
            self.inactive.setText(file_size(svirtualmemory.inactive))

        if OS.LINUX or OS.BSD:
            self.buffers.setText(file_size(svirtualmemory.buffers))
            self.cached.setText(file_size(svirtualmemory.cached))
            self.shared.setText(file_size(svirtualmemory.shared))

        if OS.LINUX:
            self.slab.setText(file_size(svirtualmemory.slab))

        if OS.BSD or OS.MACOS:
            self.wired.setText(file_size(svirtualmemory.wired))


class SwapMemory(QWidget):
    def __init__(self) -> None:
        super().__init__()

        q_color = QColor(Qt.GlobalColor.lightGray)
        self.setObjectName("name")
        self.setStyleSheet(
            f"#name{{border:1px solid {q_color.name()};background-color:white}}"
        )

        q_v_box_layout = QVBoxLayout(self)
        q_v_box_layout.setSpacing(24)

        q_label = QLabel("swap_memory")
        q_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        q_font = q_label.font()
        q_font.setWeight(QFont.Weight.Medium)
        q_label.setFont(q_font)
        q_v_box_layout.addWidget(q_label)

        self.q_progress_bar = QProgressBar()
        self.q_progress_bar.setFixedHeight(24)
        self.q_progress_bar.setMaximum(100)
        self.q_progress_bar.setTextVisible(False)
        self.q_progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        q_v_box_layout.addWidget(self.q_progress_bar)

        q_form_layout = QFormLayout()
        q_form_layout.setSpacing(24)

        self.total = QLabel("―")
        self.total.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("total", self.total)

        self.used = QLabel("―")
        self.used.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("used", self.used)

        self.free = QLabel("―")
        self.free.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("free", self.free)

        self.percent = QLabel("―")
        self.percent.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("percent", self.percent)

        if not OS.WINDOWS:
            self.sin = QLabel("―")
            self.sin.setAlignment(Qt.AlignmentFlag.AlignRight)
            q_form_layout.addRow("sin", self.sin)

            self.sout = QLabel("―")
            self.sout.setAlignment(Qt.AlignmentFlag.AlignRight)
            q_form_layout.addRow("sout", self.sout)

        q_v_box_layout.addLayout(q_form_layout)

    def update(self) -> None:
        sswap = psutil.swap_memory()

        self.q_progress_bar.setValue(int(sswap.percent))

        self.total.setText(file_size(sswap.total))
        self.used.setText(file_size(sswap.used))
        self.free.setText(file_size(sswap.free))
        self.percent.setText(f"{sswap.percent}%")
        if not OS.WINDOWS:
            self.sin.setText(file_size(sswap.sin))
            self.sout.setText(file_size(sswap.sout))


class List(QWidget):
    def __init__(self) -> None:
        super().__init__()

        q_color = QColor(Qt.GlobalColor.lightGray)
        self.setObjectName("name")
        self.setStyleSheet(
            f"#name{{border:1px solid {q_color.name()};background-color:white}}"
        )

        q_v_box_layout = QVBoxLayout(self)
        q_v_box_layout.setContentsMargins(0, 0, 0, 0)
        q_v_box_layout.setSpacing(0)

        self.vm = VirtualMemory()
        q_v_box_layout.addWidget(self.vm)

        q_v_box_layout.addWidget(Divider())

        self.sm = SwapMemory()
        q_v_box_layout.addWidget(self.sm)

    def update(self) -> None:
        self.vm.update()
        self.sm.update()

    def paintEvent(self, event: QPaintEvent) -> None:
        q_style_option = QStyleOption()
        q_style_option.initFrom(self)
        q_painter = QPainter(self)

        self.style().drawPrimitive(
            QStyle.PrimitiveElement.PE_Widget, q_style_option, q_painter, self
        )


class Widget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        q_v_box_layout = QVBoxLayout(self)
        q_v_box_layout.setContentsMargins(0, 0, 0, 0)
        q_v_box_layout.setSpacing(0)
        q_scroll_area = QScrollArea()
        q_scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        q_scroll_area.setWidgetResizable(True)
        q_widget = QWidget()
        q_h_box_layout = QHBoxLayout(q_widget)
        q_h_box_layout.setContentsMargins(24, 24, 24, 24)
        q_h_box_layout.setSpacing(0)
        q_widget_0 = QWidget()
        q_widget_0.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )
        q_widget_0.setMaximumWidth(568)

        q_v_box_layout_0 = QVBoxLayout(q_widget_0)
        q_v_box_layout_0.setContentsMargins(0, 0, 0, 0)
        self.list_0 = List()
        q_v_box_layout_0.addWidget(self.list_0)
        q_h_box_layout.addWidget(q_widget_0, alignment=Qt.AlignmentFlag.AlignTop)
        q_scroll_area.setWidget(q_widget)
        q_v_box_layout.addWidget(q_scroll_area)

        self.q_timer = QTimer(self)
        self.q_timer.setInterval(1_000)
        self.q_timer.timeout.connect(self.update)

    def showEvent(self, event: QShowEvent) -> None:
        self.q_timer.start()
        return super().showEvent(event)

    def hideEvent(self, event: QHideEvent) -> None:
        self.q_timer.stop()
        return super().hideEvent(event)

    def update(self) -> None:
        self.list_0.update()
