import psutil
import psutil._common
from PySide6.QtCore import QMargins, QTimer
from PySide6.QtGui import QHideEvent, QShowEvent, Qt
from PySide6.QtWidgets import (QAbstractItemView, QHeaderView, QTableWidget,
                               QTableWidgetItem, QVBoxLayout, QWidget)


class Widget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.q_v_box_layout = QVBoxLayout(self)
        self.q_v_box_layout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.q_v_box_layout.setSpacing(0)

        self.q_table_widget = QTableWidget()
        self.q_table_widget.setColumnCount(5)
        self.q_table_widget.setHorizontalHeaderLabels(
            ["pid", "display_name", "name", "username", "start_type"]
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
        if psutil.WINDOWS:
            for index, service in enumerate(psutil.win_service_iter()):
                self.q_table_widget_insert_row(index, service)
        self.q_table_widget.setSortingEnabled(True)
        self.q_table_widget.sortByColumn(0, Qt.SortOrder.AscendingOrder)
        self.q_v_box_layout.addWidget(self.q_table_widget)

        self.q_timer = QTimer(self)
        self.q_timer.setInterval(1_000)
        self.q_timer.timeout.connect(self.update)

    def update(self) -> None:
        win_service_list = psutil.win_service_iter()
        win_service_list_name: list[str] = [
            str(win_service.name()) for win_service in win_service_list
        ]

        q_table_widget_names = set(
            str(self.q_table_widget.item(index, 2).text())
            for index in range(self.q_table_widget.rowCount())
        )

        win_service_list = [
            win_service
            for win_service in win_service_list
            if str(win_service.name()) not in q_table_widget_names
        ]

        for index in reversed(range(self.q_table_widget.rowCount())):
            name = str(self.q_table_widget.item(index, 2).text())
            if name not in win_service_list_name:
                self.q_table_widget.removeRow(index)

        row_count = self.q_table_widget.rowCount()
        for index, win_service in enumerate(win_service_list):
            self.q_table_widget_insert_row(
                row=(row_count + index), win_service=win_service
            )

    def showEvent(self, event: QShowEvent) -> None:
        self.update()
        self.q_timer.start()
        return super().showEvent(event)

    def hideEvent(self, event: QHideEvent) -> None:
        self.q_timer.stop()
        return super().hideEvent(event)

    def q_table_widget_insert_row(self, row: int, win_service) -> None:
        self.q_table_widget.setSortingEnabled(False)
        self.q_table_widget.insertRow(row)
        self.q_table_widget.setRowHeight(row, 36)

        column = 0
        pid = QTableWidgetItem(str(win_service.pid()))
        self.q_table_widget.setItem(row, column, pid)

        column = 1
        display_name = QTableWidgetItem(str(win_service.display_name()))
        self.q_table_widget.setItem(row, column, display_name)

        column = 2
        name = QTableWidgetItem(str(win_service.name()))
        self.q_table_widget.setItem(row, column, name)

        column = 3
        try:
            username = QTableWidgetItem(str(win_service.username()))
        except Exception as exception:
            username = QTableWidgetItem()
        self.q_table_widget.setItem(row, column, username)

        column = 4
        try:
            start_type = QTableWidgetItem(str(win_service.start_type()))
        except Exception as exception:
            start_type = QTableWidgetItem()
        self.q_table_widget.setItem(row, column, start_type)

        # binpath
        # description

        self.q_table_widget.setSortingEnabled(True)
