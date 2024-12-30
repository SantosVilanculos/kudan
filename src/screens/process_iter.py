from logging import WARNING

import psutil
from PySide6.QtCore import QMargins, QTimer
from PySide6.QtGui import QHideEvent, QShowEvent, Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from environment import logger


class Widget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.logger = logger()
        self.q_v_box_layout = QVBoxLayout(self)
        self.q_v_box_layout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.q_v_box_layout.setSpacing(0)

        self.q_table_widget = QTableWidget()
        self.q_table_widget.setColumnCount(3)
        self.q_table_widget.setHorizontalHeaderLabels(["pid", "name", "username"])
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
        self.q_table_widget.addAction("SIGKILL", self.process_kill)
        self.q_table_widget.addAction("SIGTERM", self.process_terminate)

        self.q_table_widget.setSortingEnabled(True)
        self.q_table_widget.sortByColumn(0, Qt.SortOrder.AscendingOrder)
        self.q_v_box_layout.addWidget(self.q_table_widget)

        self.q_timer = QTimer(self)
        self.q_timer.setInterval(1_000)
        self.q_timer.timeout.connect(self.q_timer_timeout)

    def q_timer_timeout(self) -> None:
        process_list: list[psutil.Process] = list(psutil.process_iter())
        if not process_list:
            return

        # Create a set of PIDs from the q_table_widget
        q_table_widget_pids = set(
            int(self.q_table_widget.item(index, 0).text())
            for index in range(self.q_table_widget.rowCount())
        )

        # Remove the processes from the process_list that are already present in the q_table_widget
        process_list = [
            process
            for process in process_list
            if int(process.pid) not in q_table_widget_pids
        ]

        # Remove the rows from the q_table_widget that are no longer in the process_list
        for index in reversed(range(self.q_table_widget.rowCount())):
            pid = int(self.q_table_widget.item(index, 0).text())
            if not psutil.pid_exists(pid):
                self.q_table_widget.removeRow(index)

        # Add the remaining processes to the q_table_widget
        row_count = self.q_table_widget.rowCount()
        for index, process in enumerate(process_list):
            try:
                if psutil.Process(process.pid).is_running():
                    self.q_table_widget_insert_row(
                        row=(row_count + index), process=process
                    )
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                # TODO:log it
                # Skip the process if it no longer exists or we don't have permission to access it
                pass

    def showEvent(self, event: QShowEvent) -> None:
        self.q_timer_timeout()
        self.q_timer.start()
        return super().showEvent(event)

    def hideEvent(self, event: QHideEvent) -> None:
        self.q_timer.stop()
        return super().hideEvent(event)

    def q_table_widget_insert_row(self, row: int, process: psutil.Process) -> None:
        self.q_table_widget.setSortingEnabled(False)
        self.q_table_widget.insertRow(row)
        self.q_table_widget.setRowHeight(row, 36)

        column = 0
        pid = QTableWidgetItem(str(process.pid))
        self.q_table_widget.setItem(row, column, pid)

        column = 1
        name = QTableWidgetItem(str(process.name()))
        self.q_table_widget.setItem(row, column, name)

        column = 2
        username = QTableWidgetItem(str(process.username()))
        self.q_table_widget.setItem(row, column, username)

        self.q_table_widget.setSortingEnabled(True)

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
                    msg_box = QMessageBox(self)
                    msg_box.setIcon(QMessageBox.Warning)
                    msg_box.setText("Warning!")
                    msg_box.setInformativeText(f"Unable to kill process (pid={pid})")
                    msg_box.setStandardButtons(QMessageBox.Ok)
                    msg_box.show()
                    self.logger.log(WARNING, f"Unable to kill process (pid={pid})")

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
                    self.logger.log(WARNING, f"Unable to terminate process (pid={pid})")
