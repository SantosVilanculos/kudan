from math import floor, log2

import psutil
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QHideEvent, QShowEvent
from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QSizePolicy,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)

from components.Page import Page


def format_bytes(bytes_value) -> str:
    """
    Convert bytes to human readable format with appropriate units.
    Automatically selects the best unit for readability.
    """
    if bytes_value == 0:
        return "0 B"

    # Define unit prefixes
    units = ["B", "KB", "MB", "GB", "TB", "PB"]

    # Calculate appropriate unit index based on log2
    unit_index = min(floor(log2(abs(bytes_value)) / 10), len(units) - 1)

    # Convert to the target unit
    value = bytes_value / (1024**unit_index)

    # Format with appropriate decimal places based on size
    if value >= 100:
        # For large numbers, no decimal places
        return f"{value:.0f} {units[unit_index]}"
    elif value >= 10:
        # For medium numbers, one decimal place
        return f"{value:.1f} {units[unit_index]}"
    else:
        # For small numbers, two decimal places
        return f"{value:.2f} {units[unit_index]}"


class VirtualMemory(QWidget):
    def __init__(self):
        super().__init__()

        q_stacked_layout = QStackedLayout(self)

        q_widget = QWidget()
        q_widget.setObjectName("form")
        q_widget.setStyleSheet(
            "#form{border:1px solid #e0e0e0;background-color:#ffffff}"
        )
        q_v_box_layout = QVBoxLayout(q_widget)

        q_v_box_layout.setContentsMargins(24, 24, 24, 24)
        q_v_box_layout.setSpacing(24)
        q_label = QLabel("virtual_memory")
        q_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        q_font = q_label.font()
        q_font.setWeight(QFont.Weight.Medium)
        q_label.setFont(q_font)
        q_font = q_label.font()
        q_font.setWeight(QFont.Weight.Medium)
        q_label.setFont(q_font)
        q_v_box_layout.addWidget(q_label)

        self.q_progress_bar = QProgressBar()
        self.q_progress_bar.setStyleSheet(
            "QProgressBar{border:1px solid #e0e0e0;background-color:#f6f6f6}"
        )
        self.q_progress_bar.setFixedHeight(24)
        self.q_progress_bar.setMaximum(100)
        self.q_progress_bar.setTextVisible(False)
        self.q_progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        q_v_box_layout.addWidget(self.q_progress_bar)

        q_form_layout = QFormLayout()
        q_form_layout.setVerticalSpacing(12)

        self.total = QLabel()
        self.total.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("total", self.total)

        self.available = QLabel()
        self.available.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("available", self.available)

        self.percent = QLabel()
        self.percent.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("percent", self.percent)

        self.used = QLabel()
        self.used.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("used", self.used)

        self.free = QLabel()
        self.free.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("free", self.free)

        if psutil.LINUX or psutil.MACOS:
            self.active = QLabel()
            self.active.setAlignment(Qt.AlignmentFlag.AlignRight)
            q_form_layout.addRow("active", self.active)

            self.inactive = QLabel()
            self.inactive.setAlignment(Qt.AlignmentFlag.AlignRight)
            q_form_layout.addRow("inactive", self.inactive)

        if psutil.LINUX or psutil.BSD:
            self.buffers = QLabel()
            self.buffers.setAlignment(Qt.AlignmentFlag.AlignRight)
            q_form_layout.addRow("buffers", self.buffers)

            self.cached = QLabel()
            self.cached.setAlignment(Qt.AlignmentFlag.AlignRight)
            q_form_layout.addRow("cached", self.cached)

            self.shared = QLabel()
            self.shared.setAlignment(Qt.AlignmentFlag.AlignRight)
            q_form_layout.addRow("shared", self.shared)
        if psutil.LINUX:
            self.slab = QLabel()
            self.slab.setAlignment(Qt.AlignmentFlag.AlignRight)
            q_form_layout.addRow("slab", self.slab)
        if psutil.BSD or psutil.MACOS:
            self.wired = QLabel()
            self.wired.setAlignment(Qt.AlignmentFlag.AlignRight)
            q_form_layout.addRow("wired", self.wired)

        q_v_box_layout.addLayout(q_form_layout)
        q_stacked_layout.addWidget(q_widget)

    def update(self) -> None:
        # TODO: format correctly the filesizes
        svirtualmemory = psutil.virtual_memory()

        self.q_progress_bar.setValue(int(svirtualmemory.percent))

        self.total.setText(format_bytes(svirtualmemory.total))
        self.available.setText(format_bytes(svirtualmemory.available))
        self.percent.setText(f"{svirtualmemory.percent}%")
        self.used.setText(format_bytes(svirtualmemory.used))
        self.free.setText(format_bytes(svirtualmemory.free))

        if psutil.LINUX or psutil.MACOS:
            self.active.setText(format_bytes(svirtualmemory.active))
            self.inactive.setText(format_bytes(svirtualmemory.inactive))

        if psutil.LINUX or psutil.BSD:
            self.buffers.setText(format_bytes(svirtualmemory.buffers))
            self.cached.setText(format_bytes(svirtualmemory.cached))
            self.shared.setText(format_bytes(svirtualmemory.shared))

        if psutil.LINUX:
            self.slab.setText(str(svirtualmemory.slab))

        if psutil.BSD or psutil.MACOS:
            self.wired.setText(str(svirtualmemory.wired))


class SwapMemory(QWidget):
    def __init__(self):
        super().__init__()

        q_stacked_layout = QStackedLayout(self)
        q_widget = QWidget()
        q_widget.setObjectName("form")
        q_widget.setStyleSheet(
            "#form{border:1px solid #e0e0e0;background-color:#ffffff}"
        )
        q_v_box_layout = QVBoxLayout(q_widget)
        q_v_box_layout.setContentsMargins(24, 24, 24, 24)
        q_v_box_layout.setSpacing(24)

        q_label = QLabel("swap_memory")
        q_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        q_font = q_label.font()
        q_font.setWeight(QFont.Weight.Medium)
        q_label.setFont(q_font)
        q_v_box_layout.addWidget(q_label)

        self.q_progress_bar = QProgressBar()
        self.q_progress_bar.setStyleSheet(
            "QProgressBar{border:1px solid #e0e0e0;background-color:#f6f6f6}"
        )
        self.q_progress_bar.setFixedHeight(24)
        self.q_progress_bar.setMaximum(100)
        self.q_progress_bar.setTextVisible(False)
        self.q_progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        q_v_box_layout.addWidget(self.q_progress_bar)

        q_form_layout = QFormLayout()
        q_form_layout.setVerticalSpacing(12)

        self.total = QLabel()
        self.total.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("total", self.total)

        self.used = QLabel()
        self.used.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("used", self.used)

        self.free = QLabel()
        self.free.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("free", self.free)

        self.percent = QLabel()
        self.percent.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("percent", self.percent)

        if not psutil.WINDOWS:
            self.sin = QLabel()
            self.sin.setAlignment(Qt.AlignmentFlag.AlignRight)
            q_form_layout.addRow("sin", self.sin)

            self.sout = QLabel()
            self.sout.setAlignment(Qt.AlignmentFlag.AlignRight)
            q_form_layout.addRow("sout", self.sout)

        q_v_box_layout.addLayout(q_form_layout)
        q_stacked_layout.addWidget(q_widget)

    def update(self) -> None:
        # TODO: format correctly the filesizes
        sswap = psutil.swap_memory()

        self.q_progress_bar.setValue(int(sswap.percent))

        self.total.setText(format_bytes(sswap.total))
        self.used.setText(format_bytes(sswap.used))
        self.free.setText(format_bytes(sswap.free))
        self.percent.setText(f"{sswap.percent}%")
        if not psutil.WINDOWS:
            self.sin.setText(format_bytes(sswap.sin))
            self.sout.setText(format_bytes(sswap.sout))


class Memory(Page):
    def __init__(self):
        super().__init__("Memory")

        q_widget = QWidget()
        q_h_box_layout = QHBoxLayout(q_widget)
        q_h_box_layout.setContentsMargins(0, 0, 0, 0)
        q_h_box_layout.setSpacing(0)
        c = QWidget()
        c.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )
        c.setMaximumWidth(640)
        q_v_box_layout = QVBoxLayout(c)
        q_v_box_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        q_v_box_layout.setContentsMargins(24, 24, 24, 24)
        q_v_box_layout.setSpacing(24)
        self.virtual_memory = VirtualMemory()
        q_v_box_layout.addWidget(
            self.virtual_memory, alignment=Qt.AlignmentFlag.AlignTop
        )
        self.swap_memory = SwapMemory()
        q_v_box_layout.addWidget(self.swap_memory, alignment=Qt.AlignmentFlag.AlignTop)
        q_h_box_layout.addWidget(c)
        self.setWidget(q_widget)
        self.q_timer = QTimer(self)
        self.q_timer.setInterval(1_000)
        self.q_timer.timeout.connect(self.update)

    def update(self) -> None:
        self.virtual_memory.update()
        self.swap_memory.update()

    def showEvent(self, event: QShowEvent) -> None:
        self.update()
        self.q_timer.start()
        return super().showEvent(event)

    def hideEvent(self, event: QHideEvent) -> None:
        self.q_timer.stop()
        return super().hideEvent(event)
