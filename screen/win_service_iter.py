from psutil import WINDOWS, _pswindows, win_service_iter
from PySide6.QtCore import QMargins
from PySide6.QtGui import Qt
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
        if WINDOWS:
            for index, service in enumerate(win_service_iter()):
                self.q_table_widget_insert_row(index, service)
        self.q_table_widget.setSortingEnabled(True)
        self.q_table_widget.sortByColumn(0, Qt.SortOrder.AscendingOrder)
        self.q_v_box_layout.addWidget(self.q_table_widget)

    def q_table_widget_insert_row(
        self, row: int, service: _pswindows.WindowsService
    ) -> None:
        self.q_table_widget.setSortingEnabled(False)
        self.q_table_widget.insertRow(row)
        self.q_table_widget.setRowHeight(row, 36)

        column = 0
        pid = QTableWidgetItem(str(service.pid()))
        self.q_table_widget.setItem(row, column, pid)

        column = 1
        display_name = QTableWidgetItem(str(service.display_name()))
        self.q_table_widget.setItem(row, column, display_name)

        column = 2
        name = QTableWidgetItem(str(service.name()))
        self.q_table_widget.setItem(row, column, name)

        column = 3
        try:
            username = QTableWidgetItem(str(service.username()))
        except Exception as exception:
            username = QTableWidgetItem()
        self.q_table_widget.setItem(row, column, username)

        column = 4
        try:
            start_type = QTableWidgetItem(str(service.start_type()))
        except Exception as exception:
            start_type = QTableWidgetItem()
        self.q_table_widget.setItem(row, column, start_type)

        # binpath
        # description

        self.q_table_widget.setSortingEnabled(True)
