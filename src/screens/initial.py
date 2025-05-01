import locale
import platform
from datetime import datetime

import psutil
from custom.function import file_size
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (QFormLayout, QHBoxLayout, QLabel, QScrollArea,
                               QSizePolicy, QWidget)


class Field(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignmentFlag.AlignRight)


class Widget(QScrollArea):
    def __init__(self):
        super().__init__()

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        q_widget = QWidget()
        q_h_box_layout = QHBoxLayout(q_widget)
        q_h_box_layout.setContentsMargins(24, 24, 24, 24)
        q_h_box_layout.setSpacing(0)
        q_widget_0 = QWidget()
        q_widget_0.setObjectName("name")
        q_color = QColor(Qt.GlobalColor.lightGray)
        q_widget_0.setStyleSheet(
            f"#name{{border:1px solid {q_color.name()};background-color:white}}"
        )
        q_widget_0.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )
        q_widget_0.setMaximumWidth(568)

        q_form_layout = QFormLayout(q_widget_0)
        q_form_layout.setSpacing(24)
        self.system = Field()
        q_form_layout.addRow("system", self.system)
        self.node = Field()
        q_form_layout.addRow("node", self.node)
        self.release = Field()
        q_form_layout.addRow("release", self.release)
        self.version = Field()
        self.version.setWordWrap(True)
        q_form_layout.addRow("version", self.version)
        self.machine = Field()
        q_form_layout.addRow("machine", self.machine)
        self.processor = Field()
        q_form_layout.addRow("processor", self.processor)
        self.cpu_count = Field()
        q_form_layout.addRow("cpu_count", self.cpu_count)
        self.cpu_freq = Field()
        q_form_layout.addRow("cpu_freq", self.cpu_freq)
        self.memory_total = Field()
        q_form_layout.addRow("memory_total", self.memory_total)
        self.memory_used = Field()
        q_form_layout.addRow("memory_used", self.memory_used)
        self.memory_available = Field()
        q_form_layout.addRow("memory_available", self.memory_available)
        self.disk_total = Field()
        q_form_layout.addRow("disk_total", self.disk_total)
        self.disk_used = Field()
        q_form_layout.addRow("disk_used", self.disk_used)
        self.disk_free = Field()
        q_form_layout.addRow("disk_free", self.disk_free)
        self.boot_time = Field()
        q_form_layout.addRow("boot_time", self.boot_time)
        self.locale1 = Field()
        q_form_layout.addRow("locale", self.locale1)
        q_h_box_layout.addWidget(q_widget_0)
        self.setWidget(q_widget)

        self.q_timer = QTimer(self)
        self.q_timer.setInterval(1_000)
        self.q_timer.timeout.connect(self.update)

    def showEvent(self, event):
        self.q_timer.start()

        uname = platform.uname()
        self.system.setText(uname.system)
        self.node.setText(uname.node)
        self.release.setText(uname.release)
        self.version.setText(uname.version)
        self.machine.setText(uname.machine)
        self.processor.setText(uname.processor)
        self.cpu_count.setText(str(psutil.cpu_count(logical=True)))
        self.cpu_freq.setText(f"{(psutil.cpu_freq(percpu=False).current/1000):.2f} MHz")
        self.memory_total.setText(f"{file_size(psutil.virtual_memory().total)}")
        self.disk_total.setText(f"{file_size(psutil.disk_usage("/").total)}")
        self.locale1.setText(
            f"{locale.getlocale()[0]}.{
                locale.getlocale()[1]}"
        )
        return super().showEvent(event)

    def hideEvent(self, event):
        self.q_timer.stop()
        return super().hideEvent(event)

    def update(self):
        self.memory_used.setText(
            f"{file_size(psutil.virtual_memory().used)} ({
                psutil.virtual_memory().percent:.2f}%)"
        )
        self.memory_available.setText(f"{file_size(psutil.virtual_memory().available)}")

        disk_usage = psutil.disk_usage("/")
        self.disk_used.setText(
            f"{file_size(disk_usage.used)} ({disk_usage.percent:.2f}%)"
        )
        self.disk_free.setText(f"{file_size(disk_usage.free)}")

        a = datetime.fromtimestamp(psutil.boot_time())
        b = datetime.now() - a
        self.boot_time.setText(f"{a.strftime("%Y-%m-%d %H:%M:%S")}/{b}")
