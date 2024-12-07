from psutil import (
    LINUX,
    MACOS,
    WINDOWS,
    cpu_count,
    cpu_freq,
    cpu_percent,
    cpu_stats,
    cpu_times,
    getloadavg,
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QHideEvent, QShowEvent
from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QScrollArea,
    QSizePolicy,
    QSplitter,
    QVBoxLayout,
    QWidget,
)


class Page(QWidget):
    def __init__(self, label: str):
        super().__init__()
        q_v_box_layout = QVBoxLayout(self)
        q_v_box_layout.setContentsMargins(0, 0, 0, 0)
        q_v_box_layout.setSpacing(0)

        q_widget = QWidget()
        q_widget.setFixedHeight(44)
        q_h_box_layout = QHBoxLayout(q_widget)
        q_h_box_layout.setContentsMargins(24, 0, 24, 0)
        q_label = QLabel(label)
        q_font = q_label.font()
        q_font.setWeight(QFont.Weight.Medium)
        q_label.setFont(q_font)
        q_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        q_h_box_layout.addWidget(q_label)

        q_v_box_layout.addWidget(q_widget)

        self.q_scroll_area = QScrollArea()
        self.q_scroll_area.setStyleSheet("QScrollArea{border:0}")
        self.q_scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.q_scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.q_scroll_area.setWidgetResizable(True)
        q_v_box_layout.addWidget(self.q_scroll_area)

    def setWidget(self, q_widget: QWidget) -> None:
        self.q_scroll_area.setWidget(q_widget)


class F0(QWidget):
    def __init__(self):
        super().__init__()

        q_v_box_layout = QVBoxLayout(self)
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

        if LINUX or MACOS:
            self.nice = QLabel()
            self.nice.setAlignment(Qt.AlignmentFlag.AlignRight)
            q_form_layout.addRow("nice", self.nice)

        if LINUX:
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

        if WINDOWS:
            self.interrupt = QLabel()
            self.interrupt.setAlignment(Qt.AlignmentFlag.AlignRight)
            q_form_layout.addRow("interrupt", self.interrupt)

            self.dpc = QLabel()
            self.dpc.setAlignment(Qt.AlignmentFlag.AlignRight)
            q_form_layout.addRow("dpc", self.dpc)
        q_v_box_layout.addLayout(q_form_layout)
        # TODO: cpu_times(percpu=True)

    def update(self) -> None:
        # TODO: format dates
        scputimes = cpu_times(percpu=False)

        self.user.setText(str(scputimes.user))
        self.system.setText(str(scputimes.system))
        self.idle.setText(str(scputimes.idle))

        if LINUX or MACOS:
            self.nice.setText(str(scputimes.nice))

        if LINUX:
            self.iowait.setText(str(scputimes.iowait))
            self.irq.setText(str(scputimes.irq))
            self.softirq.setText(str(scputimes.softirq))
            self.steal.setText(str(scputimes.steal))
            self.guest.setText(str(scputimes.guest))
            self.guest_nice.setText(str(scputimes.guest_nice))

        if WINDOWS:
            self.interrupt.setText(str(scputimes.interrupt))
            self.dpc.setText(str(scputimes.dpc))


class F1(QWidget):
    def __init__(self):
        super().__init__()
        q_v_box_layout = QVBoxLayout(self)
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

    def showEvent(self, event: QShowEvent) -> None:
        self.cpu_count_cores.setText(str(cpu_count(logical=False)))
        self.cpu_count_logical.setText(str(cpu_count(logical=True)))
        return super().showEvent(event)


class F2(QWidget):
    def __init__(self):
        super().__init__()

        q_v_box_layout = QVBoxLayout(self)
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

    def update(self) -> None:
        scpustats = cpu_stats()
        self.ctx_switches.setText(str(scpustats.ctx_switches))
        self.interrupts.setText(str(scpustats.interrupts))
        self.soft_interrupts.setText(str(scpustats.soft_interrupts))
        self.syscalls.setText(str(scpustats.syscalls))


class F3(QWidget):
    def __init__(self):
        super().__init__()

        q_v_box_layout = QVBoxLayout(self)
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

    def update(self) -> None:
        scpufreq = cpu_freq(percpu=False)
        self.current.setText(f"{scpufreq.current}MHz")
        self.min.setText(f"{scpufreq.min}MHz")
        self.max.setText(f"{scpufreq.max}MHz")

        # TODO: cpu_freq(percpu=True)/Availability: Linux and FreeBSD


class F4(QWidget):
    def __init__(self):
        super().__init__()

        q_v_box_layout = QVBoxLayout(self)
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
        # TODO: cpu_percent(interval=None, percpu=True)

    def update(self) -> None:
        p = cpu_percent(interval=None, percpu=False)
        self.q_progress_bar.setValue(int(p))


class F5(QWidget):
    def __init__(self):
        super().__init__()

        q_v_box_layout = QVBoxLayout(self)
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

    def update(self) -> None:
        p1, p2, p3 = getloadavg()
        scpucount = cpu_count()
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
        self.f0 = F0()
        self.addWidget(self.f0)
        self.addWidget(F1())
        self.f2 = F2()
        self.addWidget(self.f2)
        self.f3 = F3()
        self.addWidget(self.f3)
        self.f4 = F4()
        self.addWidget(self.f4)
        self.f5 = F5()
        self.addWidget(self.f5)
        for index in range(self.count()):
            self.handle(index).setEnabled(False)

        self.q_timer = QTimer(self)
        self.q_timer.setInterval(1_000)
        self.q_timer.timeout.connect(self.update)

    def update(self) -> None:
        self.f0.update()
        self.f2.update()
        self.f3.update()
        self.f4.update()
        self.f5.update()

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
        q_v_box_layout.addWidget(C1())
        q_h_box_layout.addWidget(c)
        self.setWidget(q_widget)
