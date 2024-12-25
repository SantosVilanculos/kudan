import psutil
import psutil._common
from PySide6.QtCore import QTimer
from PySide6.QtGui import QFont, QHideEvent, QShowEvent, Qt, QTextDocument
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from environment import logger


class Tab(QWidget):
    def __init__(self, nic: str) -> None:
        super().__init__()
        self.nic = nic

        self.q_v_box_layout = QVBoxLayout(self)
        self.q_v_box_layout.setContentsMargins(0, 0, 0, 0)
        self.q_v_box_layout.setSpacing(0)
        self.q_v_box_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.q_text_browser = QTextBrowser()
        self.q_text_browser.setFont(QFont("Inter", int(14 / (96 / 72)), 400))
        self.q_v_box_layout.addWidget(self.q_text_browser, 0)

        self.q_table_widget = QTableWidget()
        self.q_table_widget.setColumnCount(5)
        self.q_table_widget.setHorizontalHeaderLabels(
            ["family", "address", "netmask", "broadcast", "ptp"]
        )
        q_table_widget_horizontal_header = self.q_table_widget.horizontalHeader()
        q_table_widget_horizontal_header.setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        # q_table_widget_horizontal_header.setFixedHeight(44)
        self.q_table_widget.verticalHeader().setHidden(True)
        self.q_table_widget.setAutoScroll(True)
        self.q_table_widget.setVerticalScrollMode(
            QAbstractItemView.ScrollMode.ScrollPerPixel
        )
        self.q_table_widget.setAlternatingRowColors(True)
        self.q_table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.q_table_widget.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.q_table_widget.setContextMenuPolicy(
            Qt.ContextMenuPolicy.ActionsContextMenu
        )

        self.q_table_widget.setSortingEnabled(True)
        self.q_table_widget.sortByColumn(0, Qt.SortOrder.AscendingOrder)
        self.q_v_box_layout.addWidget(self.q_table_widget, 1)

        self.q_timer = QTimer(self)
        self.q_timer.setInterval(1_000)
        self.q_timer.timeout.connect(self.q_timer_timeout)

    def q_timer_timeout(self) -> None:
        q_text_document = QTextDocument()
        q_text_document.setPlainText(
            f"{str(psutil.net_if_stats().get(self.nic))}\n\n{str(psutil.net_io_counters(pernic=True).get(self.nic))}"
        )
        self.q_text_browser.setDocument(q_text_document)

        self.q_table_widget.clearContents()
        self.q_table_widget.setRowCount(0)
        row_count = self.q_table_widget.rowCount()
        for index, snicaddr in enumerate(psutil.net_if_addrs().get(self.nic)):
            self.q_table_widget_insert_row(row=(row_count + index), snicaddr=snicaddr)

    def showEvent(self, event: QShowEvent) -> None:
        self.q_timer_timeout()
        self.q_timer.start()
        return super().showEvent(event)

    def hideEvent(self, event: QHideEvent) -> None:
        self.q_timer.stop()
        return super().hideEvent(event)

    def q_table_widget_insert_row(
        self, row: int, snicaddr: psutil._common.snicaddr
    ) -> None:
        self.q_table_widget.setSortingEnabled(False)
        self.q_table_widget.insertRow(row)
        self.q_table_widget.setRowHeight(row, 36)

        column = 0
        family = QTableWidgetItem(str(snicaddr.family.name))
        self.q_table_widget.setItem(row, column, family)

        column = 1
        address = QTableWidgetItem(str(snicaddr.address))
        self.q_table_widget.setItem(row, column, address)

        column = 2
        netmask = QTableWidgetItem(str(snicaddr.netmask))
        self.q_table_widget.setItem(row, column, netmask)

        column = 3
        broadcast = QTableWidgetItem(str(snicaddr.broadcast))
        self.q_table_widget.setItem(row, column, broadcast)

        column = 4
        ptp = QTableWidgetItem(str(snicaddr.ptp))
        self.q_table_widget.setItem(row, column, ptp)

        self.q_table_widget.setSortingEnabled(True)


class Widget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.logger = logger()

        q_v_box_layout = QVBoxLayout(self)
        q_v_box_layout.setContentsMargins(0, 0, 0, 0)
        q_v_box_layout.setSpacing(0)

        self.q_tab_widget = QTabWidget()
        self.q_tab_widget.removeTab
        for nic in psutil.net_if_stats().keys():
            widget = Tab(nic)
            self.q_tab_widget.addTab(widget, nic)
        q_v_box_layout.addWidget(self.q_tab_widget)

        self.q_timer = QTimer(self)
        self.q_timer.setInterval(1_000)
        self.q_timer.timeout.connect(self.q_timer_timeout)

    def q_timer_timeout(self) -> None:
        nic_list = list(psutil.net_if_stats().keys())
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
