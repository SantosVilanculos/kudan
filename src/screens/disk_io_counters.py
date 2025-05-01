import psutil
import psutil._common
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QFont, QHideEvent, QShowEvent, Qt
from PySide6.QtWidgets import (QAbstractItemView, QFormLayout, QHeaderView,
                               QLabel, QSplitter, QSplitterHandle,
                               QTableWidget, QTableWidgetItem, QVBoxLayout,
                               QWidget)


class Widget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        q_v_box_layout = QVBoxLayout(self)
        q_v_box_layout.setContentsMargins(0, 0, 0, 0)
        q_v_box_layout.setSpacing(0)

        q_splitter = QSplitter()
        q_color = QColor(Qt.GlobalColor.lightGray)
        q_splitter.setStyleSheet(
            f"QSplitter:handle{{background-color:{q_color.name()}}}"
        )
        q_splitter.setChildrenCollapsible(False)
        q_splitter.setHandleWidth(1)
        q_splitter_handle = QSplitterHandle(
            Qt.Orientation.Vertical, q_splitter)
        q_splitter_handle.setEnabled(False)
        q_splitter.createHandle = lambda: q_splitter_handle

        self.q_table_widget = QTableWidget()
        self.q_table_widget.setStyleSheet("QTableWidget{border:0}")
        self.q_table_widget.setColumnCount(10)
        self.q_table_widget.setHorizontalHeaderLabels(
            [
                "device",
                "read_count",
                "write_count",
                "read_bytes",
                "write_bytes",
                "read_time",
                "write_time",
                "busy_time",
                "read_merged_count",
                "write_merged_count",
            ]
        )
        q_table_widget_horizontal_header = self.q_table_widget.horizontalHeader()
        q_table_widget_horizontal_header.setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
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
        q_splitter.addWidget(self.q_table_widget)

        h = QWidget()
        h.setFixedWidth(240)
        q_form_layout = QFormLayout(h)
        q_form_layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
        q_form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        q_form_layout.setFormAlignment(Qt.AlignmentFlag.AlignRight)
        self.read_count = QLabel("—")
        q_form_layout.addRow("read_count", self.read_count)
        self.write_count = QLabel("—")
        q_form_layout.addRow("write_count", self.write_count)
        self.read_bytes = QLabel("—")
        q_form_layout.addRow("read_bytes", self.read_bytes)
        self.write_bytes = QLabel("—")
        q_form_layout.addRow("write_bytes", self.write_bytes)
        self.read_time = QLabel("—")
        q_form_layout.addRow("read_time", self.read_time)
        self.write_time = QLabel("—")
        q_form_layout.addRow("write_time", self.write_time)
        self.read_merged_count = QLabel("—")
        q_form_layout.addRow("read_merged_count", self.read_merged_count)
        self.write_merged_count = QLabel("—")
        q_form_layout.addRow("write_merged_count", self.write_merged_count)
        self.busy_time = QLabel("—")
        q_form_layout.addRow("busy_time", self.busy_time)
        q_splitter.addWidget(h)
        q_v_box_layout.addWidget(q_splitter)

        self.q_timer = QTimer(self)
        self.q_timer.setInterval(1_000)
        self.q_timer.timeout.connect(self.q_timer_timeout)

    def q_timer_timeout(self) -> None:
        sdiskio = psutil.disk_io_counters(perdisk=False, nowrap=True)

        self.read_count.setText(str(sdiskio.read_count))
        self.write_count.setText(str(sdiskio.write_count))
        self.read_bytes.setText(str(sdiskio.read_bytes))
        self.write_bytes.setText(str(sdiskio.write_bytes))
        self.read_time.setText(str(sdiskio.read_time))
        self.write_time.setText(str(sdiskio.write_time))
        if psutil.LINUX or psutil.FREEBSD:
            self.busy_time.setText(f"{sdiskio.busy_time} ms")
        if psutil.LINUX:
            self.read_merged_count.setText(str(sdiskio.read_merged_count))
            self.write_merged_count.setText(str(sdiskio.write_merged_count))

        p = psutil.disk_io_counters(perdisk=True, nowrap=True)

        # Create a set of PIDs from the q_table_widget
        q_table_widget_devices = set(
            str(self.q_table_widget.item(index, 0).text())
            for index in range(self.q_table_widget.rowCount())
        )

        # Remove the devices from the device list that ain't present in the q_table_widget
        device_old_list = [
            device for device in p.keys() if str(device) in q_table_widget_devices
        ]
        # Remove the devices from the device list that are already present in the q_table_widget
        device_new_list = [
            device for device in p.keys() if str(device) not in q_table_widget_devices
        ]

        # Remove the rows from the q_table_widget that are no longer in the users_list
        for index in reversed(range(self.q_table_widget.rowCount())):
            device = str(self.q_table_widget.item(index, 0).text())
            if device not in device_old_list:
                self.q_table_widget.removeRow(index)

        for index in range(self.q_table_widget.rowCount()):
            device = str(self.q_table_widget.item(index, 0).text())
            if device in device_old_list:
                self.q_table_widget_update_row(
                    row=index, device=device, sdiskio=p.get(device)
                )

        # Add the remaining users to the q_table_widget
        row_count = self.q_table_widget.rowCount()
        for index, device in enumerate(device_new_list):
            self.q_table_widget_insert_row(
                row=(row_count + index), device=device, sdiskio=p.get(device)
            )

    def showEvent(self, event: QShowEvent) -> None:
        self.q_timer_timeout()
        self.q_timer.start()
        return super().showEvent(event)

    def hideEvent(self, event: QHideEvent) -> None:
        self.q_timer.stop()
        return super().hideEvent(event)

    def q_table_widget_insert_row(self, row: int, device: str, sdiskio) -> None:
        self.q_table_widget.setSortingEnabled(False)
        self.q_table_widget.insertRow(row)
        self.q_table_widget.setRowHeight(row, 36)

        column = 0
        device = QTableWidgetItem(device)
        self.q_table_widget.setItem(row, column, device)

        column = 1
        read_count = QTableWidgetItem(str(sdiskio.read_count))
        self.q_table_widget.setItem(row, column, read_count)

        column = 2
        write_count = QTableWidgetItem(str(sdiskio.write_count))
        self.q_table_widget.setItem(row, column, write_count)

        column = 3
        read_bytes = QTableWidgetItem(str(sdiskio.read_bytes))
        self.q_table_widget.setItem(row, column, read_bytes)

        column = 4
        write_bytes = QTableWidgetItem(str(sdiskio.write_bytes))
        self.q_table_widget.setItem(row, column, write_bytes)

        column = 5
        read_time = QTableWidgetItem(str(sdiskio.read_time))
        self.q_table_widget.setItem(row, column, read_time)

        column = 6
        write_time = QTableWidgetItem(str(sdiskio.write_time))
        self.q_table_widget.setItem(row, column, write_time)

        column = 7
        if psutil.LINUX or psutil.FREEBSD:
            busy_time = QTableWidgetItem(f"{sdiskio.busy_time} ms")
        else:
            busy_time = QTableWidgetItem("—")
        self.q_table_widget.setItem(row, column, busy_time)

        column = 8
        if psutil.LINUX:
            read_merged_count = QTableWidgetItem(
                str(sdiskio.read_merged_count))
        else:
            read_merged_count = QTableWidgetItem("—")
        self.q_table_widget.setItem(row, column, read_merged_count)

        column = 9
        if psutil.LINUX:
            write_merged_count = QTableWidgetItem(
                str(sdiskio.write_merged_count))
        else:
            write_merged_count = QTableWidgetItem("—")
        self.q_table_widget.setItem(row, column, write_merged_count)

        self.q_table_widget.setSortingEnabled(True)

    def q_table_widget_update_row(self, row: int, device: str, sdiskio) -> None:
        self.q_table_widget.setSortingEnabled(False)

        column = 0
        device_item = self.q_table_widget.item(row, column)
        device_item.setText(f"{device}")

        column = 1
        read_count = self.q_table_widget.item(row, column)
        read_count.setText(str(sdiskio.read_count))

        column = 2
        write_count = self.q_table_widget.item(row, column)
        write_count.setText(str(sdiskio.write_count))

        column = 3
        read_bytes = self.q_table_widget.item(row, column)
        read_bytes.setText(str(sdiskio.read_bytes))

        column = 4
        write_bytes = self.q_table_widget.item(row, column)
        write_bytes.setText(str(sdiskio.write_bytes))

        column = 5
        read_time = self.q_table_widget.item(row, column)
        read_time.setText(str(sdiskio.read_time))

        column = 6
        write_time = self.q_table_widget.item(row, column)
        write_time.setText(str(sdiskio.write_time))

        column = 7
        busy_time = self.q_table_widget.item(row, column)
        if psutil.LINUX or psutil.FREEBSD:
            busy_time.setText(f"{sdiskio.busy_time} ms")
        else:
            busy_time.setText("—")

        column = 8
        read_merged_count = self.q_table_widget.item(row, column)
        if psutil.LINUX:
            read_merged_count.setText(str(sdiskio.read_merged_count))
        else:
            read_merged_count.setText("—")

        column = 9
        write_merged_count = self.q_table_widget.item(row, column)
        if psutil.LINUX:
            write_merged_count.setText(str(sdiskio.write_merged_count))
        else:
            write_merged_count.setText("—")

        self.q_table_widget.setSortingEnabled(True)
