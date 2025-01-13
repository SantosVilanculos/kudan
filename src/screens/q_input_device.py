from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import (
    QColor,
    QHideEvent,
    QInputDevice,
    QPainter,
    QPaintEvent,
    QShowEvent,
)
from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QSizePolicy,
    QStyle,
    QStyleOption,
    QVBoxLayout,
    QWidget,
)


class ListItem(QWidget):
    def __init__(self, q_input_device: QInputDevice):
        super().__init__()

        self.q_input_device = q_input_device

        q_color = QColor(Qt.GlobalColor.lightGray)
        self.setObjectName("undefined")
        self.setStyleSheet(
            f"#undefined{{border: 1px solid {
                q_color.name()};background-color:white}}"
        )
        q_form_layout = QFormLayout(self)
        q_form_layout.setVerticalSpacing(24)
        self.system_id = QLabel(str(q_input_device.systemId()))
        self.system_id.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("systemId", self.system_id)
        self.name = QLabel(q_input_device.name())
        self.name.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("name", self.name)
        self.type = QLabel(str(q_input_device.type().name))
        self.type.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("type", self.type)
        self.capabilities = QLabel(str(q_input_device.capabilities().name))
        self.capabilities.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("capabilities", self.capabilities)

    def paintEvent(self, event: QPaintEvent) -> None:
        q_style_option = QStyleOption()
        q_style_option.initFrom(self)
        q_painter = QPainter(self)

        self.style().drawPrimitive(
            QStyle.PrimitiveElement.PE_Widget, q_style_option, q_painter, self
        )

    def update(self, q_input_device: QInputDevice) -> None:
        pass


class List(QWidget):
    def __init__(self):
        super().__init__()

        self.q_v_box_layout = QVBoxLayout(self)
        self.q_v_box_layout.setContentsMargins(0, 0, 0, 0)
        self.q_v_box_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for q_input_device in QInputDevice.devices():
            self.q_v_box_layout.addWidget(ListItem(q_input_device))

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
        _A = QInputDevice.devices()
        _B: list[int] = [q_input_device.systemId() for q_input_device in _A]
        _C: list[int] = list()

        for index in range(self.q_v_box_layout.count()):
            q_layout_item = self.q_v_box_layout.itemAt(index)

            if not q_layout_item:
                continue

            q_widget = q_layout_item.widget()

            if not isinstance(q_widget, ListItem):
                continue

            if q_widget.q_input_device.systemId() not in _B:
                self.q_v_box_layout.removeWidget(q_widget)
                q_widget.deleteLater()
            else:
                _C.append(q_widget.q_input_device.systemId())
                q_input_device = next(
                    (
                        q_input_device
                        for q_input_device in _A
                        if q_input_device.systemId()
                        == q_widget.q_input_device.systemId()
                    ),
                    None,
                )
                if q_input_device:
                    q_widget.update(q_input_device)

        for q_input_device in _A:
            if q_input_device.systemId() not in _C:
                self.q_v_box_layout.addWidget(ListItem(q_input_device))


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
