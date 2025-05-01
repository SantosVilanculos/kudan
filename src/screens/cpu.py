from datetime import timedelta

import psutil
import psutil._common
from custom.os import OS
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import (QColor, QFont, QHideEvent, QPainter, QPaintEvent,
                           QShowEvent)
from PySide6.QtWidgets import (QFormLayout, QHBoxLayout, QLabel, QProgressBar,
                               QScrollArea, QSizePolicy, QStyle, QStyleOption,
                               QVBoxLayout, QWidget)
from ui.divider import Divider


# TODO: per cpu
class CpuTimes(QWidget):
    def __init__(self) -> None:
        super().__init__()

        q_v_box_layout = QVBoxLayout(self)
        q_v_box_layout.setSpacing(24)

        q_label = QLabel("cpu_times")
        q_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        q_font = q_label.font()
        q_font.setWeight(QFont.Weight.Medium)
        q_label.setFont(q_font)
        q_v_box_layout.addWidget(q_label)

        q_form_layout = QFormLayout()
        q_form_layout.setSpacing(24)

        self.user = QLabel("―")
        self.user.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("user", self.user)

        self.system = QLabel("―")
        self.system.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("system", self.system)

        self.idle = QLabel("―")
        self.idle.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("idle", self.idle)

        if psutil.LINUX or psutil.MACOS:
            self.nice = QLabel("―")
            self.nice.setAlignment(Qt.AlignmentFlag.AlignRight)
            q_form_layout.addRow("nice", self.nice)

        if psutil.LINUX:
            self.iowait = QLabel("―")
            self.iowait.setAlignment(Qt.AlignmentFlag.AlignRight)
            q_form_layout.addRow("iowait", self.iowait)

            self.irq = QLabel("―")
            self.irq.setAlignment(Qt.AlignmentFlag.AlignRight)
            q_form_layout.addRow("irq", self.irq)

            self.softirq = QLabel("―")
            self.softirq.setAlignment(Qt.AlignmentFlag.AlignRight)
            q_form_layout.addRow("softirq", self.softirq)

            self.steal = QLabel("―")
            self.steal.setAlignment(Qt.AlignmentFlag.AlignRight)
            q_form_layout.addRow("steal", self.steal)

            self.guest = QLabel("―")
            self.guest.setAlignment(Qt.AlignmentFlag.AlignRight)
            q_form_layout.addRow("guest", self.guest)

            self.guest_nice = QLabel("―")
            self.guest_nice.setAlignment(Qt.AlignmentFlag.AlignRight)
            q_form_layout.addRow("guest_nice", self.guest_nice)

        if psutil.WINDOWS:
            self.interrupt = QLabel("―")
            self.interrupt.setAlignment(Qt.AlignmentFlag.AlignRight)
            q_form_layout.addRow("interrupt", self.interrupt)

            self.dpc = QLabel("―")
            self.dpc.setAlignment(Qt.AlignmentFlag.AlignRight)
            q_form_layout.addRow("dpc", self.dpc)

        q_v_box_layout.addLayout(q_form_layout)

    def update(self) -> None:
        p = psutil.cpu_times_percent(interval=None, percpu=False)
        scputimes = psutil.cpu_times(percpu=False)

        self.user.setText(f"{timedelta(seconds=scputimes.user)} ({p.user}%)")
        self.system.setText(f"{timedelta(seconds=scputimes.system)} ({p.system}%)")
        self.idle.setText(f"{timedelta(seconds=scputimes.idle)} ({p.idle}%)")

        if OS.LINUX or psutil.MACOS:
            self.nice.setText(str(timedelta(seconds=scputimes.nice)))

        if OS.LINUX:
            self.iowait.setText(str(timedelta(seconds=scputimes.iowait)))
            self.irq.setText(str(timedelta(seconds=scputimes.irq)))
            self.softirq.setText(str(timedelta(seconds=scputimes.softirq)))
            self.steal.setText(str(timedelta(seconds=scputimes.steal)))
            self.guest.setText(str(timedelta(seconds=scputimes.guest)))
            self.guest_nice.setText(str(timedelta(seconds=scputimes.guest_nice)))

        if OS.WINDOWS:
            self.interrupt.setText(
                f"{timedelta(seconds=scputimes.interrupt)} ({p.interrupt}%)"
            )
            self.dpc.setText(f"{timedelta(seconds=scputimes.dpc)} ({p.dpc}%)")


# TODO: per cpu
class CpuPercent(QWidget):
    def __init__(self) -> None:
        super().__init__()

        q_v_box_layout = QVBoxLayout(self)
        q_v_box_layout.setSpacing(24)

        q_label = QLabel("cpu_percent")
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

    def update(self) -> None:
        p = psutil.cpu_percent(interval=None, percpu=False)
        self.q_progress_bar.setValue(int(p))


class CpuCount(QWidget):
    def __init__(self) -> None:
        super().__init__()

        q_v_box_layout = QVBoxLayout(self)
        q_v_box_layout.setSpacing(24)

        q_label = QLabel("cpu_count")
        q_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        q_font = q_label.font()
        q_font.setWeight(QFont.Weight.Medium)
        q_label.setFont(q_font)
        q_v_box_layout.addWidget(q_label)

        q_form_layout = QFormLayout()
        q_form_layout.setSpacing(24)

        self.cpu_count_cores = QLabel("―")
        self.cpu_count_cores.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("cpu_count_cores", self.cpu_count_cores)

        self.cpu_count_logical = QLabel("―")
        self.cpu_count_logical.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("cpu_count_logical", self.cpu_count_logical)

        q_v_box_layout.addLayout(q_form_layout)

    def showEvent(self, event: QShowEvent) -> None:
        self.cpu_count_cores.setText(str(psutil.cpu_count(logical=False)))
        self.cpu_count_logical.setText(str(psutil.cpu_count(logical=True)))
        return super().showEvent(event)


class CpuStats(QWidget):
    def __init__(self) -> None:
        super().__init__()

        q_v_box_layout = QVBoxLayout(self)
        q_v_box_layout.setSpacing(24)

        q_label = QLabel("cpu_stats")
        q_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        q_font = q_label.font()
        q_font.setWeight(QFont.Weight.Medium)
        q_label.setFont(q_font)
        q_v_box_layout.addWidget(q_label)

        q_form_layout = QFormLayout()
        q_form_layout.setSpacing(24)

        self.ctx_switches = QLabel("―")
        self.ctx_switches.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("ctx_switches", self.ctx_switches)
        self.interrupts = QLabel("―")
        self.interrupts.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("interrupts", self.interrupts)
        self.soft_interrupts = QLabel("―")
        self.soft_interrupts.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("soft_interrupts", self.soft_interrupts)
        self.syscalls = QLabel("―")
        self.syscalls.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("syscalls", self.syscalls)

        q_v_box_layout.addLayout(q_form_layout)

    def update(self) -> None:
        scpustats = psutil.cpu_stats()
        self.ctx_switches.setText(str(scpustats.ctx_switches))
        self.interrupts.setText(str(scpustats.interrupts))
        self.soft_interrupts.setText(str(scpustats.soft_interrupts))
        self.syscalls.setText(str(scpustats.syscalls))


# TODO: per cpu
class CpuFreq(QWidget):
    def __init__(self) -> None:
        super().__init__()

        q_v_box_layout = QVBoxLayout(self)
        q_v_box_layout.setSpacing(24)

        q_label = QLabel("cpu_stats")
        q_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        q_font = q_label.font()
        q_font.setWeight(QFont.Weight.Medium)
        q_label.setFont(q_font)
        q_v_box_layout.addWidget(q_label)

        q_form_layout = QFormLayout()
        q_form_layout.setSpacing(24)

        self.current = QLabel("―")
        self.current.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("current", self.current)
        self.min = QLabel("―")
        self.min.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("min", self.min)
        self.max = QLabel("―")
        self.max.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("max", self.max)

        q_v_box_layout.addLayout(q_form_layout)

    def update(self) -> None:
        scpufreq = psutil.cpu_freq(percpu=False)
        self.current.setText(f"{scpufreq.current} MHz")
        self.min.setText(f"{scpufreq.min} MHz")
        self.max.setText(f"{scpufreq.max} MHz")


class GetLoadAvg(QWidget):
    def __init__(self) -> None:
        super().__init__()

        q_v_box_layout = QVBoxLayout(self)
        q_v_box_layout.setSpacing(24)

        q_label = QLabel("getloadavg")
        q_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        q_font = q_label.font()
        q_font.setWeight(QFont.Weight.Medium)
        q_label.setFont(q_font)
        q_v_box_layout.addWidget(q_label)

        q_h_box_layout = QHBoxLayout()
        self.q_label_0 = QLabel("―")
        self.q_label_0.setAlignment(Qt.AlignmentFlag.AlignCenter)
        q_h_box_layout.addWidget(self.q_label_0)
        self.q_label_1 = QLabel("―")
        self.q_label_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        q_h_box_layout.addWidget(self.q_label_1)
        self.q_label_2 = QLabel("―")
        self.q_label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        q_h_box_layout.addWidget(self.q_label_2)
        q_v_box_layout.addLayout(q_h_box_layout)

    def update(self) -> None:
        if OS.UNIX or OS.WINDOWS:
            p_0, p_1, p_2 = psutil.getloadavg()
            scpucount = psutil.cpu_count()
            self.q_label_0.setText(f"{(p_0 / scpucount * 100):.2f}%")
            self.q_label_1.setText(f"{(p_1 / scpucount * 100):.2f}%")
            self.q_label_2.setText(f"{(p_2 / scpucount * 100):.2f}%")


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

        self.ct = CpuTimes()
        q_v_box_layout.addWidget(self.ct)

        q_v_box_layout.addWidget(Divider())

        self.cp = CpuPercent()
        q_v_box_layout.addWidget(self.cp)

        q_v_box_layout.addWidget(Divider())

        q_v_box_layout.addWidget(CpuCount())

        q_v_box_layout.addWidget(Divider())

        self.cs = CpuStats()
        q_v_box_layout.addWidget(self.cs)

        q_v_box_layout.addWidget(Divider())

        self.cf = CpuFreq()
        q_v_box_layout.addWidget(self.cf)

        if OS.UNIX or OS.WINDOWS:
            q_v_box_layout.addWidget(Divider())

            self.gla = GetLoadAvg()
            q_v_box_layout.addWidget(self.gla)

    def update(self) -> None:
        self.ct.update()
        self.cp.update()
        self.cs.update()
        self.cf.update()
        if OS.UNIX or OS.WINDOWS:
            self.gla.update()

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
