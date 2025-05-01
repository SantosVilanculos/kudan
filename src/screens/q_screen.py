from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import (QColor, QGuiApplication, QHideEvent, QPainter,
                           QPaintEvent, QScreen, QShowEvent)
from PySide6.QtWidgets import (QFormLayout, QHBoxLayout, QLabel, QScrollArea,
                               QSizePolicy, QStyle, QStyleOption, QVBoxLayout,
                               QWidget)


class ListItem(QWidget):
    def __init__(self, q_screen: QScreen) -> None:
        super().__init__()

        self.q_screen = q_screen

        self.setObjectName("undefined")
        q_color = QColor(Qt.GlobalColor.lightGray)
        self.setStyleSheet(
            f"#undefined{{border: 1px solid {
                q_color.name()};background-color:white}}"
        )
        q_form_layout = QFormLayout(self)
        q_form_layout.setVerticalSpacing(24)
        self.name = QLabel(q_screen.name())
        self.name.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("name", self.name)
        self.size = QLabel(str(q_screen.size()))
        self.size.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("size", self.size)
        self.depth = QLabel(str(q_screen.depth()))
        self.depth.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("depth", self.depth)
        self.device_pixel_ratio = QLabel(str(q_screen.devicePixelRatio()))
        self.device_pixel_ratio.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("devicePixelRatio", self.device_pixel_ratio)
        self.refresh_rate = QLabel(str(q_screen.refreshRate()))
        self.refresh_rate.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("refreshRate", self.refresh_rate)
        self.model = QLabel(q_screen.model())
        self.model.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("model", self.model)
        self.serial_number = QLabel(q_screen.serialNumber())
        self.serial_number.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("serialNumber", self.serial_number)
        self.manufacturer = QLabel(q_screen.manufacturer())
        self.manufacturer.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("manufacturer", self.manufacturer)
        self.native_interface = QLabel(str(q_screen.nativeInterface()))
        self.native_interface.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("nativeInterface", self.native_interface)
        self.orientation = QLabel(str(q_screen.orientation().name))
        self.orientation.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("orientation", self.orientation)
        self.native_orientation = QLabel(str(q_screen.nativeOrientation().name))
        self.native_orientation.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("nativeOrientation", self.native_orientation)

    def paintEvent(self, event: QPaintEvent) -> None:
        q_style_option = QStyleOption()
        q_style_option.initFrom(self)
        q_painter = QPainter(self)
        self.style().drawPrimitive(
            QStyle.PrimitiveElement.PE_Widget, q_style_option, q_painter, self
        )

    def update(self, q_screen: QScreen) -> None:
        self.device_pixel_ratio.setText(str(q_screen.devicePixelRatio()))
        self.refresh_rate.setText(str(q_screen.refreshRate()))
        self.model.setText(q_screen.model())
        self.serial_number.setText(q_screen.serialNumber())
        self.manufacturer.setText(q_screen.manufacturer())
        self.native_interface.setText(str(q_screen.nativeInterface()))
        self.orientation.setText(str(q_screen.orientation().name))
        self.native_orientation.setText(str(q_screen.nativeOrientation().name))


class List(QWidget):
    def __init__(self):
        super().__init__()

        self.q_v_box_layout = QVBoxLayout(self)
        self.q_v_box_layout.setContentsMargins(0, 0, 0, 0)
        self.q_v_box_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for q_screen in QGuiApplication.screens():
            self.q_v_box_layout.addWidget(ListItem(q_screen))

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
        _A = QGuiApplication.screens()
        _B: list[str] = [q_screen.name() for q_screen in _A]
        _C: list[str] = list()

        for index in range(self.q_v_box_layout.count()):
            q_layout_item = self.q_v_box_layout.itemAt(index)

            if not q_layout_item:
                continue

            q_widget = q_layout_item.widget()

            if not isinstance(q_widget, ListItem):
                continue

            if q_widget.q_screen.name() not in _B:
                self.q_v_box_layout.removeWidget(q_widget)
                q_widget.deleteLater()
            else:
                _C.append(q_widget.q_screen.name())
                q_screen = next(
                    (
                        q_screen
                        for q_screen in _A
                        if q_screen.name() == q_widget.q_screen.name()
                    ),
                    None,
                )
                if q_screen:
                    q_widget.update(q_screen)

        for q_screen in _A:
            if q_screen.name() not in _C:
                self.q_v_box_layout.addWidget(ListItem(q_screen))


class Widget(QScrollArea):
    def __init__(self):
        super().__init__()

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        q_widget = QWidget()
        q_h_box_layout = QHBoxLayout(q_widget)
        q_h_box_layout.setContentsMargins(24, 24, 24, 24)
        q_h_box_layout.setSpacing(0)
        main = QWidget()
        main.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )
        main.setMaximumWidth(568)
        q_v_box_layout = QVBoxLayout(main)
        q_v_box_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        q_v_box_layout.setContentsMargins(0, 0, 0, 0)
        q_v_box_layout.addWidget(List())
        q_h_box_layout.addWidget(main)

        self.setWidget(q_widget)
