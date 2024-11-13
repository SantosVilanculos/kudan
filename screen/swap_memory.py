from math import floor, log2

from psutil import swap_memory
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
        self.used = QLabel("—")
        self.used.setStyleSheet("color:#bbb")
        q_form_layout.addRow("used", self.used)
        self.free = QLabel("—")
        self.free.setStyleSheet("color:#bbb")
        q_form_layout.addRow("free", self.free)
        self.percent = QLabel("—")
        self.percent.setStyleSheet("color:#bbb")
        q_form_layout.addRow("percent", self.percent)
        self.sin = QLabel("—")
        self.sin.setStyleSheet("color:#bbb")
        q_form_layout.addRow("sin", self.sin)
        self.sout = QLabel("—")
        self.sout.setStyleSheet("color:#bbb")
        q_form_layout.addRow("sout", self.sout)

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
        sm = swap_memory()
        self.total.setText(str(self.format_bytes(sm.total)))
        self.used.setText(str(self.format_bytes(sm.used)))
        self.free.setText(str(self.format_bytes(sm.free)))
        self.percent.setText(f"{sm.percent}%")
        self.sin.setText(str(self.format_bytes(sm.sin)))
        self.sout.setText(str(self.format_bytes(sm.sout)))

        self.q_progress_bar.setMaximum(100)
        self.q_progress_bar.setValue(int(sm.percent))

    def showEvent(self, event: QShowEvent) -> None:
        self.q_timer_timeout()
        self.q_timer.start()
        return super().showEvent(event)

    def hideEvent(self, event: QHideEvent) -> None:
        self.q_timer.stop()
        return super().hideEvent(event)
