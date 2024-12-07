from datetime import datetime

from psutil import _common, users
from PySide6.QtCore import QMargins, QTimer
from PySide6.QtGui import QHideEvent, QShowEvent, Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class Widget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.q_v_box_layout = QVBoxLayout(self)
        self.q_v_box_layout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.q_v_box_layout.setSpacing(0)

        self.q_table_widget = QTableWidget()
        self.q_table_widget.setColumnCount(5)
        self.q_table_widget.setHorizontalHeaderLabels(
            ["pid", "name", "terminal", "host", "started"]
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
        self.q_v_box_layout.addWidget(self.q_table_widget)

        self.q_timer = QTimer(self)
        self.q_timer.setInterval(1_000)
        self.q_timer.timeout.connect(self.q_timer_timeout)

    def q_timer_timeout(self) -> None:
        users_list: list[_common.suser] = users()
        users_list_pid: list[str] = [str(user.pid) for user in users_list]

        # Create a set of PIDs from the q_table_widget
        q_table_widget_pids = set(
            str(self.q_table_widget.item(index, 0).text())
            for index in range(self.q_table_widget.rowCount())
        )

        # Remove the users from the users_list that are already present in the q_table_widget
        users_list = [
            user for user in users_list if str(user.pid) not in q_table_widget_pids
        ]

        # Remove the rows from the q_table_widget that are no longer in the users_list
        for index in reversed(range(self.q_table_widget.rowCount())):
            pid = str(self.q_table_widget.item(index, 0).text())
            if pid not in users_list_pid:
                self.q_table_widget.removeRow(index)

        # Add the remaining users to the q_table_widget
        row_count = self.q_table_widget.rowCount()
        for index, user in enumerate(users_list):
            self.q_table_widget_insert_row(row=(row_count + index), user=user)

    def showEvent(self, event: QShowEvent) -> None:
        self.q_timer_timeout()
        self.q_timer.start()
        return super().showEvent(event)

    def hideEvent(self, event: QHideEvent) -> None:
        self.q_timer.stop()
        return super().hideEvent(event)

    def q_table_widget_insert_row(self, row: int, user: _common.suser) -> None:
        self.q_table_widget.setSortingEnabled(False)
        self.q_table_widget.insertRow(row)
        self.q_table_widget.setRowHeight(row, 36)

        column = 0
        pid = QTableWidgetItem(str(user.pid))
        self.q_table_widget.setItem(row, column, pid)

        column = 1
        name = QTableWidgetItem(user.name)
        self.q_table_widget.setItem(row, column, name)

        column = 2
        username = QTableWidgetItem(user.terminal)
        self.q_table_widget.setItem(row, column, username)

        column = 3
        username = QTableWidgetItem(str(user.host))
        self.q_table_widget.setItem(row, column, username)

        column = 4
        username = QTableWidgetItem(
            str(datetime.fromtimestamp(user.started).strftime("%Y-%m-%d %H:%M:%S"))
        )
        self.q_table_widget.setItem(row, column, username)

        self.q_table_widget.setSortingEnabled(True)
