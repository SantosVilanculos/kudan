import psutil
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QHideEvent, QShowEvent, Qt
from PySide6.QtWidgets import (QAbstractItemView, QCheckBox, QHBoxLayout,
                               QHeaderView, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget)


class Widget(QWidget):
    all = False

    def __init__(self) -> None:
        super().__init__()

        q_v_box_layout = QVBoxLayout(self)
        q_v_box_layout.setContentsMargins(0, 0, 0, 0)
        q_v_box_layout.setSpacing(0)

        h = QWidget()
        h.setFixedHeight(44)
        q_h_box_layout = QHBoxLayout(h)
        q_h_box_layout.setContentsMargins(0, 0, 0, 0)
        q_h_box_layout.setSpacing(0)
        q_check_box = QCheckBox()
        q_check_box.setChecked(self.all)
        q_check_box.setText("all")
        q_check_box.checkStateChanged.connect(
            lambda check_state: self.check_state_changed(check_state)
        )
        q_h_box_layout.addWidget(q_check_box)
        q_v_box_layout.addWidget(h)

        self.q_table_widget = QTableWidget()
        self.q_table_widget.setColumnCount(4)
        self.q_table_widget.setHorizontalHeaderLabels(
            ["device", "mountpoint", "fstype", "opts"]
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
        q_v_box_layout.addWidget(self.q_table_widget)

        self.q_timer = QTimer(self)
        self.q_timer.setInterval(1_000)
        self.q_timer.timeout.connect(self.q_timer_timeout)

    def check_state_changed(self, check_state: Qt.CheckState):
        if (check_state == Qt.CheckState.PartiallyChecked) or (
            check_state == Qt.CheckState.Checked
        ):
            self.all = True
        elif check_state == Qt.CheckState.Unchecked:
            self.all = False

    def q_timer_timeout(self) -> None:

        sdiskpart_list = psutil.disk_partitions(all=self.all)
        sdiskpart_list_pid: list[str] = [
            str(sdiskpart.device) for sdiskpart in sdiskpart_list
        ]

        # Create a set of PIDs from the q_table_widget
        q_table_widget_pids = set(
            str(self.q_table_widget.item(index, 0).text())
            for index in range(self.q_table_widget.rowCount())
        )

        # Remove the users from the sdiskpart_list that are already present in the q_table_widget
        sdiskpart_list = [
            sdiskpart
            for sdiskpart in sdiskpart_list
            if str(sdiskpart.device) not in q_table_widget_pids
        ]

        # Remove the rows from the q_table_widget that are no longer in the sdiskpart_list
        for index in reversed(range(self.q_table_widget.rowCount())):
            device = str(self.q_table_widget.item(index, 0).text())
            if device not in sdiskpart_list_pid:
                self.q_table_widget.removeRow(index)

        # Add the remaining users to the q_table_widget
        row_count = self.q_table_widget.rowCount()
        for index, sdiskpart in enumerate(sdiskpart_list):
            self.q_table_widget_insert_row(row=(row_count + index), sdiskpart=sdiskpart)

    def showEvent(self, event: QShowEvent) -> None:
        self.q_timer_timeout()
        self.q_timer.start()
        return super().showEvent(event)

    def hideEvent(self, event: QHideEvent) -> None:
        self.q_timer.stop()
        return super().hideEvent(event)

    def q_table_widget_insert_row(self, row: int, sdiskpart) -> None:
        self.q_table_widget.setSortingEnabled(False)
        self.q_table_widget.insertRow(row)
        self.q_table_widget.setRowHeight(row, 36)

        column = 0
        pid = QTableWidgetItem(str(sdiskpart.device))
        self.q_table_widget.setItem(row, column, pid)

        column = 1
        name = QTableWidgetItem(str(sdiskpart.mountpoint))
        self.q_table_widget.setItem(row, column, name)

        column = 2
        username = QTableWidgetItem(str(sdiskpart.fstype))
        self.q_table_widget.setItem(row, column, username)

        column = 3
        username = QTableWidgetItem(str(sdiskpart.opts))
        self.q_table_widget.setItem(row, column, username)

        self.q_table_widget.setSortingEnabled(True)
