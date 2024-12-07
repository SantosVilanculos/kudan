import psutil
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QHideEvent, QShowEvent
from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QSizePolicy,
    QSplitter,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)

from components.Page import Page


def secs2hours(secs):
    mm, ss = divmod(secs, 60)
    hh, mm = divmod(mm, 60)
    return "%02d:%02d:%02d" % (hh, mm, ss)


class CpuTimes(QWidget):
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
        q_label = QLabel("cpu_times")
        q_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        q_font = q_label.font()
        q_font.setWeight(QFont.Weight.Medium)
        q_label.setFont(q_font)
        q_font = q_label.font()
        q_font.setWeight(QFont.Weight.Medium)
        q_label.setFont(q_font)
        q_v_box_layout.addWidget(q_label)
        q_form_layout = QFormLayout()
        q_form_layout.setVerticalSpacing(12)
        # q_form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        # q_form_layout.setFormAlignment(Qt.AlignmentFlag.AlignRight)
        self.user = QLabel()
        self.user.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("user", self.user)

        self.system = QLabel()
        self.system.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("system", self.system)

        self.idle = QLabel()
        self.idle.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("idle", self.idle)

        if psutil.LINUX or psutil.MACOS:
            self.nice = QLabel()
            self.nice.setAlignment(Qt.AlignmentFlag.AlignRight)
            q_form_layout.addRow("nice", self.nice)

        if psutil.LINUX:
            self.iowait = QLabel()
            self.iowait.setAlignment(Qt.AlignmentFlag.AlignRight)
            q_form_layout.addRow("iowait", self.iowait)

            self.irq = QLabel()
            self.irq.setAlignment(Qt.AlignmentFlag.AlignRight)
            q_form_layout.addRow("irq", self.irq)

            self.softirq = QLabel()
            self.softirq.setAlignment(Qt.AlignmentFlag.AlignRight)
            q_form_layout.addRow("softirq", self.softirq)

            self.steal = QLabel()
            self.steal.setAlignment(Qt.AlignmentFlag.AlignRight)
            q_form_layout.addRow("steal", self.steal)

            self.guest = QLabel()
            self.guest.setAlignment(Qt.AlignmentFlag.AlignRight)
            q_form_layout.addRow("guest", self.guest)

            self.guest_nice = QLabel()
            self.guest_nice.setAlignment(Qt.AlignmentFlag.AlignRight)
            q_form_layout.addRow("guest_nice", self.guest_nice)

        if psutil.WINDOWS:
            self.interrupt = QLabel()
            self.interrupt.setAlignment(Qt.AlignmentFlag.AlignRight)
            q_form_layout.addRow("interrupt", self.interrupt)

            self.dpc = QLabel()
            self.dpc.setAlignment(Qt.AlignmentFlag.AlignRight)
            q_form_layout.addRow("dpc", self.dpc)
        q_v_box_layout.addLayout(q_form_layout)
        q_stacked_layout.addWidget(q_widget)
        # TODO: psutil.cpu_times(percpu=True)

    def update(self) -> None:
        # TODO: format dates
        scputimes = psutil.cpu_times(percpu=False)

        self.user.setText(str(secs2hours(scputimes.user)))
        self.system.setText(str(secs2hours(scputimes.system)))
        self.idle.setText(str(secs2hours(scputimes.idle)))

        if psutil.LINUX or psutil.MACOS:
            self.nice.setText(str(secs2hours(scputimes.nice)))

        if psutil.LINUX:
            self.iowait.setText(str(secs2hours(scputimes.iowait)))
            self.irq.setText(str(secs2hours(scputimes.irq)))
            self.softirq.setText(str(secs2hours(scputimes.softirq)))
            self.steal.setText(str(secs2hours(scputimes.steal)))
            self.guest.setText(str(secs2hours(scputimes.guest)))
            self.guest_nice.setText(str(secs2hours(scputimes.guest_nice)))

        if psutil.WINDOWS:
            self.interrupt.setText(str(secs2hours(scputimes.interrupt)))
            self.dpc.setText(str(secs2hours(scputimes.dpc)))


class CpuPercent(QWidget):
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
        q_label = QLabel("cpu_percent")
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
        # self.q_progress_bar.setTextVisible(False)
        self.q_progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        q_v_box_layout.addWidget(self.q_progress_bar)
        # TODO: psutil.cpu_percent(interval=None, percpu=True)
        q_stacked_layout.addWidget(q_widget)

    def update(self) -> None:
        p = psutil.cpu_percent(interval=None, percpu=False)
        self.q_progress_bar.setValue(int(p))


class CpuCount(QWidget):
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
        q_label = QLabel("cpu_count")
        q_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        q_font = q_label.font()
        q_font.setWeight(QFont.Weight.Medium)
        q_label.setFont(q_font)
        q_v_box_layout.addWidget(q_label)
        q_form_layout = QFormLayout()
        q_form_layout.setVerticalSpacing(12)
        # q_form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        # q_form_layout.setFormAlignment(Qt.AlignmentFlag.AlignRight)
        self.cpu_count_cores = QLabel()
        self.cpu_count_cores.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("cpu_count_cores", self.cpu_count_cores)
        self.cpu_count_logical = QLabel()
        self.cpu_count_logical.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("cpu_count_logical", self.cpu_count_logical)
        q_v_box_layout.addLayout(q_form_layout)
        q_stacked_layout.addWidget(q_widget)

    def showEvent(self, event: QShowEvent) -> None:
        self.cpu_count_cores.setText(str(psutil.cpu_count(logical=False)))
        self.cpu_count_logical.setText(str(psutil.cpu_count(logical=True)))
        return super().showEvent(event)


class CpuStats(QWidget):
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
        q_label = QLabel("cpu_stats")
        q_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        q_font = q_label.font()
        q_font.setWeight(QFont.Weight.Medium)
        q_label.setFont(q_font)
        q_font = q_label.font()
        q_font.setWeight(QFont.Weight.Medium)
        q_label.setFont(q_font)
        q_v_box_layout.addWidget(q_label)
        q_form_layout = QFormLayout()
        q_form_layout.setVerticalSpacing(12)
        # q_form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        # q_form_layout.setFormAlignment(Qt.AlignmentFlag.AlignRight)
        self.ctx_switches = QLabel()
        self.ctx_switches.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("ctx_switches", self.ctx_switches)
        self.interrupts = QLabel()
        self.interrupts.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("interrupts", self.interrupts)
        self.soft_interrupts = QLabel()
        self.soft_interrupts.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("soft_interrupts", self.soft_interrupts)
        self.syscalls = QLabel()
        self.syscalls.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("syscalls", self.syscalls)
        q_v_box_layout.addLayout(q_form_layout)
        q_stacked_layout.addWidget(q_widget)

    def update(self) -> None:
        scpustats = psutil.cpu_stats()
        self.ctx_switches.setText(str(scpustats.ctx_switches))
        self.interrupts.setText(str(scpustats.interrupts))
        self.soft_interrupts.setText(str(scpustats.soft_interrupts))
        self.syscalls.setText(str(scpustats.syscalls))


class CpuFreq(QWidget):
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
        q_label = QLabel("cpu_freq")
        q_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        q_font = q_label.font()
        q_font.setWeight(QFont.Weight.Medium)
        q_label.setFont(q_font)
        q_v_box_layout.addWidget(q_label)
        q_form_layout = QFormLayout()
        q_form_layout.setVerticalSpacing(12)
        # q_form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        # q_form_layout.setFormAlignment(Qt.AlignmentFlag.AlignRight)
        self.current = QLabel()
        self.current.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("current", self.current)
        self.min = QLabel()
        self.min.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("min", self.min)
        self.max = QLabel()
        self.max.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("max", self.max)
        q_v_box_layout.addLayout(q_form_layout)
        q_stacked_layout.addWidget(q_widget)

    def update(self) -> None:
        scpufreq = psutil.cpu_freq(percpu=False)
        self.current.setText(f"{scpufreq.current}MHz")
        self.min.setText(f"{scpufreq.min}MHz")
        self.max.setText(f"{scpufreq.max}MHz")

        # TODO: psutil.cpu_freq(percpu=True)/Availability: Linux and FreeBSD


class Getloadavg(QWidget):
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
        q_label = QLabel("getloadavg")
        q_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        q_font = q_label.font()
        q_font.setWeight(QFont.Weight.Medium)
        q_label.setFont(q_font)
        q_v_box_layout.addWidget(q_label)

        q_h_box_layout = QHBoxLayout()
        self.q_label1 = QLabel()
        self.q_label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        q_h_box_layout.addWidget(self.q_label1)
        self.q_label2 = QLabel()
        self.q_label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        q_h_box_layout.addWidget(self.q_label2)
        self.q_label3 = QLabel()
        self.q_label3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        q_h_box_layout.addWidget(self.q_label3)
        q_v_box_layout.addLayout(q_h_box_layout)
        q_stacked_layout.addWidget(q_widget)

    def update(self) -> None:
        p1, p2, p3 = psutil.getloadavg()
        scpucount = psutil.cpu_count()
        self.q_label1.setText(f"{p1 / scpucount * 100}%")
        self.q_label2.setText(f"{p2 / scpucount * 100}%")
        self.q_label3.setText(f"{p3 / scpucount * 100}%")


class C1(QSplitter):
    def __init__(self):
        super().__init__()
        self.setChildrenCollapsible(False)
        self.setStyleSheet(
            "QSplitter{border:1px solid #e0e0e0;background-color:#ffffff}QSplitter::handle{background-color:#e0e0e0}"
        )
        self.setOrientation(Qt.Orientation.Vertical)
        self.setHandleWidth(1)

        self.cpu_times = CpuTimes()
        self.addWidget(self.cpu_times)

        self.cpu_percent = CpuPercent()
        self.addWidget(self.cpu_percent)

        self.addWidget(CpuCount())

        self.cpu_stats = CpuStats()
        self.addWidget(self.cpu_stats)

        self.cpu_freq = CpuFreq()
        self.addWidget(self.cpu_freq)

        self.getloadavg = Getloadavg()
        self.addWidget(self.getloadavg)
        for index in range(self.count()):
            self.handle(index).setEnabled(False)

        self.q_timer = QTimer(self)
        self.q_timer.setInterval(1_000)
        self.q_timer.timeout.connect(self.update)

    def update(self) -> None:
        self.cpu_times.update()
        self.cpu_percent.update()
        self.cpu_stats.update()
        self.cpu_freq.update()
        self.getloadavg.update()

    def showEvent(self, event: QShowEvent) -> None:
        self.update()
        self.q_timer.start()
        return super().showEvent(event)

    def hideEvent(self, event: QHideEvent) -> None:
        self.q_timer.stop()
        return super().hideEvent(event)


class CPU(Page):
    def __init__(self):
        super().__init__("CPU")
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

        self.cpu_times = CpuTimes()
        q_v_box_layout.addWidget(self.cpu_times, alignment=Qt.AlignmentFlag.AlignTop)

        self.cpu_percent = CpuPercent()
        q_v_box_layout.addWidget(self.cpu_percent, alignment=Qt.AlignmentFlag.AlignTop)

        q_v_box_layout.addWidget(CpuCount(), alignment=Qt.AlignmentFlag.AlignTop)

        self.cpu_stats = CpuStats()
        q_v_box_layout.addWidget(self.cpu_stats, alignment=Qt.AlignmentFlag.AlignTop)

        self.cpu_freq = CpuFreq()
        q_v_box_layout.addWidget(self.cpu_freq, alignment=Qt.AlignmentFlag.AlignTop)

        self.getloadavg = Getloadavg()
        q_v_box_layout.addWidget(self.getloadavg, alignment=Qt.AlignmentFlag.AlignTop)

        q_h_box_layout.addWidget(c)
        self.setWidget(q_widget)
        self.q_timer = QTimer(self)
        self.q_timer.setInterval(1_000)
        self.q_timer.timeout.connect(self.update)

    def update(self) -> None:
        self.cpu_times.update()
        self.cpu_percent.update()
        self.cpu_stats.update()
        self.cpu_freq.update()
        self.getloadavg.update()

    def showEvent(self, event: QShowEvent) -> None:
        self.update()
        self.q_timer.start()
        return super().showEvent(event)

    def hideEvent(self, event: QHideEvent) -> None:
        self.q_timer.stop()
        return super().hideEvent(event)
