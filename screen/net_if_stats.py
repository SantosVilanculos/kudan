from psutil import net_if_addrs, net_if_stats, net_io_counters
from PySide6.QtCore import QTimer
from PySide6.QtGui import QFont, QHideEvent, QShowEvent, QTextDocument
from PySide6.QtWidgets import QTabWidget, QTextBrowser, QVBoxLayout, QWidget

from environment import logger


class Tab(QWidget):
    def __init__(self, nic: str) -> None:
        super().__init__()
        self.nic = nic

        q_v_box_layout = QVBoxLayout(self)
        q_v_box_layout.setContentsMargins(0, 0, 0, 0)
        q_v_box_layout.setSpacing(0)
        self.q_text_browser = QTextBrowser()
        self.q_text_browser.setFont(QFont("Inter", int(14 / (96 / 72)), 400))
        q_v_box_layout.addWidget(self.q_text_browser)

        self.q_timer = QTimer(self)
        self.q_timer.setInterval(1_000)
        self.q_timer.timeout.connect(self.q_timer_timeout)

    def q_timer_timeout(self) -> None:
        q_text_document = QTextDocument()
        q_text_document.setPlainText(
            f"{str(net_if_stats().get(self.nic))}\n\n{str(net_io_counters(pernic=True).get(self.nic))}\n\n{str(net_if_addrs().get(self.nic))}"
        )
        self.q_text_browser.setDocument(q_text_document)

    def showEvent(self, event: QShowEvent) -> None:
        self.q_timer_timeout()
        self.q_timer.start()
        return super().showEvent(event)

    def hideEvent(self, event: QHideEvent) -> None:
        self.q_timer.stop()
        return super().hideEvent(event)


class Widget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.logger = logger()

        q_v_box_layout = QVBoxLayout(self)
        q_v_box_layout.setContentsMargins(0, 0, 0, 0)
        q_v_box_layout.setSpacing(0)

        self.q_tab_widget = QTabWidget()
        self.q_tab_widget.removeTab
        for nic in net_if_stats().keys():
            widget = Tab(nic)
            self.q_tab_widget.addTab(widget, nic)
        q_v_box_layout.addWidget(self.q_tab_widget)

        self.q_timer = QTimer(self)
        self.q_timer.setInterval(1_000)
        self.q_timer.timeout.connect(self.q_timer_timeout)

    def q_timer_timeout(self) -> None:
        nic_list = list(net_if_stats().keys())
        index = 0
        while index < self.q_tab_widget.count():
            nic = self.q_tab_widget.tabText(index)
            if nic_list.count(nic) == 0:
                self.q_tab_widget.removeTab(index)
            else:
                nic_list.remove(nic)
            index += 1

        for nic in nic_list:
            widget = Tab(nic)
            self.q_tab_widget.addTab(widget, nic)

    def showEvent(self, event: QShowEvent) -> None:
        self.q_timer.start()
        return super().showEvent(event)

    def hideEvent(self, event: QHideEvent) -> None:
        self.q_timer.stop()
        return super().hideEvent(event)
