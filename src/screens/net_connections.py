from datetime import datetime
from logging import ERROR, WARNING
from sys import exec_prefix

import psutil
import psutil._common
from logger import logger
from PySide6.QtCore import QTimer, QUrl
from PySide6.QtGui import QHideEvent, QShowEvent, Qt
from PySide6.QtWidgets import (QAbstractItemView, QComboBox, QHBoxLayout,
                               QHeaderView, QSizePolicy, QTableWidget,
                               QTableWidgetItem, QVBoxLayout, QWidget)


class Widget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.kind = "all"

        q_v_box_layout = QVBoxLayout(self)
        q_v_box_layout.setContentsMargins(0, 0, 0, 0)
        q_v_box_layout.setSpacing(0)

        q_widget = QWidget()
        q_widget.setFixedHeight(44)
        q_h_box_layout = QHBoxLayout(q_widget)
        # q_h_box_layout.setContentsMargins(0, 0, 0, 0)
        self.q_combo_box = QComboBox()
        self.q_combo_box.setSizePolicy(
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Preferred,
        )
        self.q_combo_box.addItem(
            "the sum of all the possible families and protocols", "all"
        )
        self.q_combo_box.addItem("IPv4 and IPv6", "inet")
        self.q_combo_box.addItem("IPv4", "inet4")
        self.q_combo_box.addItem("IPv6", "inet6")
        self.q_combo_box.addItem("TCP", "tcp")
        self.q_combo_box.addItem("TCP over IPv4", "tcp4")
        self.q_combo_box.addItem("TCP over IPv6", "tcp6")
        self.q_combo_box.addItem("UDP", "udp")
        self.q_combo_box.addItem("UDP over IPv4", "udp4")
        self.q_combo_box.addItem("UDP over IPv6", "udp6")
        self.q_combo_box.addItem(
            "UNIX socket (both UDP and TCP protocols)", "unix")

        self.q_combo_box.currentIndexChanged.connect(
            lambda index: self.k(index))
        q_h_box_layout.addWidget(
            self.q_combo_box, 0, Qt.AlignmentFlag.AlignLeft)
        q_v_box_layout.addWidget(q_widget)

        self.q_table_widget = QTableWidget()
        self.q_table_widget.setColumnCount(9)
        self.q_table_widget.setHorizontalHeaderLabels(
            [
                "pid",
                "name",
                "fd",
                "family",
                "type",
                "laddr",
                "raddr",
                "status",
                "create_time",
            ]
        )
        self.q_table_widget.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
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
        self.q_table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.q_table_widget.setAlternatingRowColors(True)
        self.q_table_widget.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.q_table_widget.setContextMenuPolicy(
            Qt.ContextMenuPolicy.ActionsContextMenu
        )
        self.q_table_widget.addAction("SIGKILL", self.process_kill)
        self.q_table_widget.addAction("SIGTERM", self.process_terminate)

        for index, sconn in enumerate(psutil.net_connections()):
            self.q_table_widget_insert_row(index, sconn)

        self.q_table_widget.setSortingEnabled(True)
        self.q_table_widget.sortByColumn(0, Qt.SortOrder.AscendingOrder)

        q_v_box_layout.addWidget(self.q_table_widget)

        self.q_timer = QTimer(self)
        self.q_timer.setInterval(1_000)
        self.q_timer.timeout.connect(self.q_timer_timeout)

    def k(self, index: int) -> None:
        # TODO: update table
        self.kind = self.q_combo_box.currentData(Qt.ItemDataRole.UserRole)
        self.q_table_widget.clearContents()
        self.q_table_widget.setRowCount(0)
        for index, sconn in enumerate(psutil.net_connections(self.kind)):
            self.q_table_widget_insert_row(index, sconn)

    def q_table_widget_insert_row(self, row: int, sconn) -> None:
        self.q_table_widget.setSortingEnabled(False)

        self.q_table_widget.insertRow(row)
        self.q_table_widget.setRowHeight(row, 36)

        column = 0
        pid = QTableWidgetItem(str(sconn.pid))
        pid.setData(Qt.ItemDataRole.UserRole, sconn.pid)
        self.q_table_widget.setItem(row, column, pid)

        column = 1
        name = QTableWidgetItem()
        try:
            process = psutil.Process(sconn.pid)
            name.setText(process.name())
        except Exception as exception:
            pass
        self.q_table_widget.setItem(row, column, name)

        column = 2
        fd = QTableWidgetItem(str(sconn.fd))
        self.q_table_widget.setItem(row, column, fd)

        column = 3
        family = QTableWidgetItem(str(sconn.family.name))
        self.q_table_widget.setItem(row, column, family)

        column = 4
        type = QTableWidgetItem(str(sconn.type.name))
        self.q_table_widget.setItem(row, column, type)

        column = 5
        q_url = QUrl()
        if isinstance(sconn.laddr, psutil._common.addr):
            q_url.setHost(sconn.laddr.ip)
            q_url.setPort(sconn.laddr.port)
            laddr = QTableWidgetItem(
                str(q_url.url(QUrl.ComponentFormattingOption.EncodeUnicode))
            )
        elif sconn.laddr:
            laddr = QTableWidgetItem(str(sconn.laddr))
        else:
            laddr = QTableWidgetItem()

        self.q_table_widget.setItem(row, column, laddr)

        column = 6
        q_url.clear()
        if isinstance(sconn.raddr, psutil._common.addr):
            q_url.setHost(sconn.raddr.ip)
            q_url.setPort(sconn.raddr.port)
            raddr = QTableWidgetItem(
                q_url.url(QUrl.ComponentFormattingOption.EncodeUnicode)
            )
        elif sconn.raddr:
            raddr = QTableWidgetItem(str(sconn.raddr))
        else:
            raddr = QTableWidgetItem()
        self.q_table_widget.setItem(row, column, raddr)

        column = 7
        status = QTableWidgetItem(str(sconn.status))
        self.q_table_widget.setItem(row, column, status)

        column = 8
        create_time = QTableWidgetItem()
        try:
            process = psutil.Process(sconn.pid)
            create_time.setText(
                datetime.fromtimestamp(process.create_time()).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )
        except Exception as exception:
            pass
        self.q_table_widget.setItem(row, column, create_time)

        self.q_table_widget.setSortingEnabled(True)

    def q_timer_timeout(self) -> None:
        n = psutil.net_connections(kind=self.kind)
        process_list: list[psutil.Process] = list(psutil.process_iter())
        if not process_list:
            return

        process_pids = {int(process.pid) for process in process_list}

        # Create a dictionary to store the unique network connections
        unique_connections: dict[int,
                                 dict[tuple[str, str], psutil._common.sconn]] = {}

        # Iterate through the network connections and store the unique ones
        for sconn in n:
            if sconn.pid in process_pids:
                conn_key = (sconn.laddr, sconn.raddr)
                if sconn.pid not in unique_connections:
                    unique_connections[sconn.pid] = {}
                if conn_key not in unique_connections[sconn.pid]:
                    unique_connections[sconn.pid][conn_key] = sconn

        # Create a set of PIDs from the q_table_widget
        q_table_widget_pids = set()
        for index in range(self.q_table_widget.rowCount()):
            text = self.q_table_widget.item(index, 0).text()
            if (text is not None) and (text != "None"):
                q_table_widget_pids.add(int(text))

        # Remove the rows from the q_table_widget that are no longer in the process_list
        for index in reversed(range(self.q_table_widget.rowCount())):
            text = self.q_table_widget.item(index, 0).text()
            if (text is not None) and (text != "None"):
                pid = int(text)
                if pid not in process_pids:
                    self.q_table_widget.removeRow(index)

        # Add the unique network connections to the q_table_widget
        row_count = self.q_table_widget.rowCount()
        for pid, conn_dict in unique_connections.items():
            for sconn in conn_dict.values():
                if pid not in q_table_widget_pids:
                    self.q_table_widget_insert_row(row_count, sconn)
                    row_count += 1

    def showEvent(self, event: QShowEvent) -> None:
        self.q_timer.start()
        return super().showEvent(event)

    def hideEvent(self, event: QHideEvent) -> None:
        self.q_timer.stop()
        return super().hideEvent(event)

    def process_kill(self) -> None:
        q_table_widget_selected_items = self.q_table_widget.selectedItems()
        if len(q_table_widget_selected_items) > 0:
            row_list = list(
                set(
                    self.q_table_widget.row(x)
                    for x in self.q_table_widget.selectedItems()
                )
            )
            for row in row_list:
                pid = int(self.q_table_widget.item(row, 0).text())
                try:
                    process = psutil.Process(pid)
                    process.kill()
                except Exception as exception:
                    logger.log(
                        ERROR, f"Unable to kill process (pid={pid}):{exception}")

    def process_terminate(self) -> None:
        q_table_widget_selected_items = self.q_table_widget.selectedItems()
        if len(q_table_widget_selected_items) > 0:
            row_list = list(
                set(
                    self.q_table_widget.row(x)
                    for x in self.q_table_widget.selectedItems()
                )
            )
            for row in row_list:
                pid = int(self.q_table_widget.item(row, 0).text())
                try:
                    process = psutil.Process(pid)
                    process.terminate()
                except Exception as exception:
                    logger.log(
                        ERROR,
                        f"Unable to terminate process (pid={pid}):{
                            exception}",
                    )
