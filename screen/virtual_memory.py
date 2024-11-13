from math import floor, log2

from psutil import virtual_memory
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QHideEvent, QShowEvent
from PySide6.QtWidgets import QFormLayout, QLabel, QProgressBar, QVBoxLayout, QWidget


class Widget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        q_v_box_layout = QVBoxLayout(self)
        q_v_box_layout.setContentsMargins(4, 4, 4, 4)
        q_v_box_layout.setSpacing(0)
        q_v_box_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        h = QWidget()

        q_form_layout = QFormLayout(h)
        q_form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.setFormAlignment(Qt.AlignmentFlag.AlignLeft)
        self.total = QLabel("—")
        self.total.setStyleSheet("color:#bbb")
        q_form_layout.addRow("total", self.total)
        self.avail = QLabel("—")
        self.avail.setStyleSheet("color:#bbb")
        q_form_layout.addRow("avail", self.avail)
        self.percent = QLabel("—")
        self.percent.setStyleSheet("color:#bbb")
        q_form_layout.addRow("percent", self.percent)
        self.used = QLabel("—")
        self.used.setStyleSheet("color:#bbb")
        q_form_layout.addRow("used", self.used)
        self.free = QLabel("—")
        self.free.setStyleSheet("color:#bbb")
        q_form_layout.addRow("free", self.free)
        self.active = QLabel("—")
        self.active.setStyleSheet("color:#bbb")
        q_form_layout.addRow("active", self.active)
        self.inactive = QLabel("—")
        self.inactive.setStyleSheet("color:#bbb")
        q_form_layout.addRow("inactive", self.inactive)
        self.buffers = QLabel("—")
        self.buffers.setStyleSheet("color:#bbb")
        q_form_layout.addRow("buffers", self.buffers)
        self.cached = QLabel("—")
        self.cached.setStyleSheet("color:#bbb")
        q_form_layout.addRow("cached", self.cached)
        self.shared = QLabel("—")
        self.shared.setStyleSheet("color:#bbb")
        q_form_layout.addRow("shared", self.shared)
        self.slab = QLabel("—")
        self.slab.setStyleSheet("color:#bbb")
        q_form_layout.addRow("slab", self.slab)

        q_v_box_layout.addWidget(h)

        self.q_progress_bar = QProgressBar()
        self.q_progress_bar.setFixedHeight(44)
        q_v_box_layout.addWidget(self.q_progress_bar)

        self.q_timer = QTimer(self)
        self.q_timer.setInterval(1_000)
        self.q_timer.timeout.connect(self.q_timer_timeout)

    def format_bytes(self, bytes_value):
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

    def q_timer_timeout(self) -> None:
        vm = virtual_memory()
        self.total.setText(str(self.format_bytes(vm.total)))
        self.avail.setText(str(self.format_bytes(vm.available)))
        self.percent.setText(f"{vm.percent}%")
        self.used.setText(str(self.format_bytes(vm.used)))
        self.free.setText(str(self.format_bytes(vm.free)))
        self.active.setText(str(self.format_bytes(vm.active)))
        self.inactive.setText(str(self.format_bytes(vm.inactive)))
        self.buffers.setText(str(self.format_bytes(vm.buffers)))
        self.cached.setText(str(self.format_bytes(vm.cached)))
        self.shared.setText(str(self.format_bytes(vm.shared)))
        self.slab.setText(str(self.format_bytes(vm.slab)))

        self.q_progress_bar.setMaximum(100)
        self.q_progress_bar.setValue(int(vm.percent))

    def showEvent(self, event: QShowEvent) -> None:
        self.q_timer_timeout()
        self.q_timer.start()
        return super().showEvent(event)

    def hideEvent(self, event: QHideEvent) -> None:
        self.q_timer.stop()
        return super().hideEvent(event)
