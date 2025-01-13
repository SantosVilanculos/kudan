from socket import AddressFamily

import psutil
import psutil._common
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QHideEvent, QPainter, QPaintEvent, QShowEvent
from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QSizePolicy,
    QStyle,
    QStyleOption,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from custom.function import file_size


class SNicStats(QWidget):
    def __init__(self, name: str) -> None:
        super().__init__()

        self.name = name

        q_color = QColor(Qt.GlobalColor.lightGray)
        self.setObjectName("name")
        self.setStyleSheet(
            f"#name{{border:1px solid {q_color.name()};background-color:white}}"
        )
        q_form_layout = QFormLayout(self)
        q_form_layout.setSpacing(24)
        self.isup = QLabel("―")
        self.isup.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("isup", self.isup)
        self.duplex = QLabel("―")
        self.duplex.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("duplex", self.duplex)
        self.speed = QLabel("―")
        self.speed.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("speed", self.speed)
        self.mtu = QLabel("―")
        self.mtu.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("mtu", self.mtu)
        self.flags = QLabel("―")
        self.flags.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("flags", self.flags)

    def update(self) -> None:
        snicstats = psutil.net_if_stats().get(self.name, None)

        if not snicstats:
            return

        self.isup.setText(str(snicstats.isup))
        if snicstats.duplex == psutil.NIC_DUPLEX_FULL:
            self.duplex.setText("NIC_DUPLEX_FULL")
        elif snicstats.duplex == psutil.NIC_DUPLEX_HALF:
            self.duplex.setText("NIC_DUPLEX_HALF")
        else:
            self.duplex.setText("NIC_DUPLEX_UNKNOWN")

        self.speed.setText(file_size((snicstats.speed * 1024)))
        self.mtu.setText(file_size(snicstats.mtu))
        self.flags.setText(str(snicstats.flags))

    def paintEvent(self, event: QPaintEvent) -> None:
        q_style_option = QStyleOption()
        q_style_option.initFrom(self)
        q_painter = QPainter(self)

        self.style().drawPrimitive(
            QStyle.PrimitiveElement.PE_Widget, q_style_option, q_painter, self
        )


class SNetIO(QWidget):
    def __init__(self, name: str) -> None:
        super().__init__()

        self.name = name

        q_color = QColor(Qt.GlobalColor.lightGray)
        self.setObjectName("name")
        self.setStyleSheet(
            f"#name{{border:1px solid {q_color.name()};background-color:white}}"
        )
        q_form_layout = QFormLayout(self)
        q_form_layout.setSpacing(24)
        self.bytes_sent = QLabel("―")
        self.bytes_sent.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("bytes_sent", self.bytes_sent)
        self.bytes_recv = QLabel("―")
        self.bytes_recv.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("bytes_recv", self.bytes_recv)
        self.packets_sent = QLabel("―")
        self.packets_sent.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("packets_sent", self.packets_sent)
        self.packets_recv = QLabel("―")
        self.packets_recv.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("packets_recv", self.packets_recv)
        self.errin = QLabel("―")
        self.errin.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("errin", self.errin)
        self.errout = QLabel("―")
        self.errout.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("errout", self.errout)
        self.dropin = QLabel("―")
        self.dropin.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("dropin", self.dropin)
        self.dropout = QLabel("―")
        self.dropout.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("dropout", self.dropout)

    def update(self) -> None:
        snetio = psutil.net_io_counters(pernic=True).get(self.name, None)

        if not snetio:
            return

        self.bytes_sent.setText(file_size(snetio.bytes_sent))
        self.bytes_recv.setText(file_size(snetio.bytes_recv))
        self.packets_sent.setText(str(snetio.packets_sent))
        self.packets_recv.setText(str(snetio.packets_recv))
        self.errin.setText(str(snetio.errin))
        self.errout.setText(str(snetio.errout))
        self.dropin.setText(str(snetio.dropin))
        self.dropout.setText(str(snetio.dropout))

    def paintEvent(self, event: QPaintEvent) -> None:
        q_style_option = QStyleOption()
        q_style_option.initFrom(self)
        q_painter = QPainter(self)

        self.style().drawPrimitive(
            QStyle.PrimitiveElement.PE_Widget, q_style_option, q_painter, self
        )


class SNicAddrItem(QWidget):
    def __init__(self, snicaddr: psutil._common.snicaddr) -> None:
        super().__init__()

        self.snicaddr = snicaddr

        q_color = QColor(Qt.GlobalColor.lightGray)
        self.setObjectName("name")
        self.setStyleSheet(
            f"#name{{border:1px solid {q_color.name()};background-color:white}}"
        )
        q_form_layout = QFormLayout(self)
        q_form_layout.setSpacing(24)
        self.family = QLabel(snicaddr.family.name)
        self.family.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("family", self.family)
        self.address = QLabel(snicaddr.address)
        self.address.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("address", self.address)
        self.netmask = QLabel(snicaddr.netmask or "―")
        self.netmask.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("netmask", self.netmask)
        self.broadcast = QLabel(snicaddr.broadcast or "―")
        self.broadcast.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("broadcast", self.broadcast)
        self.ptp = QLabel(snicaddr.ptp or "―")
        self.ptp.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("ptp", self.ptp)

    def paintEvent(self, event: QPaintEvent) -> None:
        q_style_option = QStyleOption()
        q_style_option.initFrom(self)
        q_painter = QPainter(self)

        self.style().drawPrimitive(
            QStyle.PrimitiveElement.PE_Widget, q_style_option, q_painter, self
        )

    def update(self, snicaddr: psutil._common.snicaddr) -> None:
        self.family.setText(snicaddr.family.name)
        self.address.setText(snicaddr.address)
        self.netmask.setText(snicaddr.netmask or "―")
        self.broadcast.setText(snicaddr.broadcast or "―")
        self.ptp.setText(snicaddr.ptp or "―")


class SNicAddr(QWidget):
    def __init__(self, name: str) -> None:
        super().__init__()

        self.name = name

        self.q_v_box_layout = QVBoxLayout(self)
        self.q_v_box_layout.setContentsMargins(0, 0, 0, 0)

        for snicaddr in psutil.net_if_addrs().get(name, list()):
            self.q_v_box_layout.addWidget(SNicAddrItem(snicaddr))

    def update(self) -> None:
        _A = psutil.net_if_addrs().get(self.name, list())
        _B: list[AddressFamily] = [snicaddr.family for snicaddr in _A]
        _C: list[AddressFamily] = list()

        for index in range(self.q_v_box_layout.count()):
            q_layout_item = self.q_v_box_layout.itemAt(index)

            if not q_layout_item:
                continue

            q_widget = q_layout_item.widget()

            if not isinstance(q_widget, SNicAddrItem):
                continue

            if q_widget.snicaddr.family not in _B:
                self.q_v_box_layout.removeWidget(q_widget)
                q_widget.deleteLater()
            else:
                _C.append(q_widget.snicaddr.family)
                snicaddr = next(
                    (
                        snicaddr
                        for snicaddr in _A
                        if snicaddr.family == q_widget.snicaddr.family
                    ),
                    None,
                )
                if snicaddr:
                    q_widget.update(snicaddr)

        for snicaddr in _A:
            if snicaddr.family not in _C:
                self.q_v_box_layout.addWidget(SNicAddrItem(snicaddr))


class Tab(QWidget):
    def __init__(self, name: str) -> None:
        super().__init__()

        q_v_box_layout = QVBoxLayout(self)
        q_v_box_layout.setContentsMargins(0, 0, 0, 0)
        q_v_box_layout.setSpacing(0)
        q_scroll_area = QScrollArea()
        q_scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        q_scroll_area.setWidgetResizable(True)
        q_widget = QWidget()
        q_h_box_layout = QHBoxLayout(q_widget)
        q_h_box_layout.setContentsMargins(24, 24, 24, 24)
        q_h_box_layout.setSpacing(0)
        q_widget_0 = QWidget()
        q_widget_0.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )
        q_widget_0.setMaximumWidth(568)

        q_v_box_layout_0 = QVBoxLayout(q_widget_0)
        q_v_box_layout_0.setContentsMargins(0, 0, 0, 0)
        q_v_box_layout_0.addWidget(QLabel("snicstats"))
        self.s_nic_stats = SNicStats(name)
        q_v_box_layout_0.addWidget(self.s_nic_stats)
        q_v_box_layout_0.addWidget(QLabel("snetio"))
        self.s_net_io = SNetIO(name)
        q_v_box_layout_0.addWidget(self.s_net_io)

        q_v_box_layout_0.addWidget(QLabel("snicaddr"))
        self.s_nic_addr = SNicAddr(name)
        q_v_box_layout_0.addWidget(self.s_nic_addr)
        q_h_box_layout.addWidget(q_widget_0, alignment=Qt.AlignmentFlag.AlignTop)
        q_scroll_area.setWidget(q_widget)
        q_v_box_layout.addWidget(q_scroll_area)

    def update(self) -> None:
        if self.isHidden():
            return

        self.s_nic_stats.update()
        self.s_net_io.update()
        self.s_nic_addr.update()


class Widget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        q_v_box_layout = QVBoxLayout(self)
        q_v_box_layout.setContentsMargins(0, 0, 0, 0)
        q_v_box_layout.setSpacing(0)
        self.q_tab_widget = QTabWidget()
        # self.q_tab_widget.setCornerWidget(QPushButton("―"), Qt.Corner.TopRightCorner)
        self.q_tab_bar = self.q_tab_widget.tabBar()
        self.q_tab_bar.setDocumentMode(True)
        for name, snicstats in psutil.net_if_stats().items():
            index = self.q_tab_widget.addTab(
                Tab(name), f"{name} (isup={snicstats.isup})"
            )
            self.q_tab_bar.setTabData(index, name)
        q_v_box_layout.addWidget(self.q_tab_widget)

        self.q_timer = QTimer(self)
        self.q_timer.setInterval(1_000)
        self.q_timer.timeout.connect(self.update)

    def showEvent(self, event: QShowEvent) -> None:
        self.q_timer.start()
        return super().showEvent(event)

    def hideEvent(self, event: QHideEvent) -> None:
        self.q_timer.stop()
        return super().hideEvent(event)

    def update(self) -> None:
        collection = list(psutil.net_if_stats().keys())

        for index in reversed(range(self.q_tab_widget.count())):
            name = str(self.q_tab_bar.tabData(index))

            if name not in collection:
                q_widget = self.q_tab_widget.widget(index)
                self.q_tab_widget.removeTab(index)
                q_widget.deleteLater()
            else:
                collection.remove(name)

                snicstats = psutil.net_if_stats().get(name, None)
                if snicstats:
                    self.q_tab_widget.setTabText(
                        index, f"{name} (isup={snicstats.isup})"
                    )

                q_widget = self.q_tab_widget.widget(index)
                q_widget.update()

        for name in collection:
            self.q_tab_widget.addTab(Tab(name), name)
