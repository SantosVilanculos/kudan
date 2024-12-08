from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QHideEvent, QInputDevice, QShowEvent
from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)

from components.Page import Page


class Card(QWidget):
    def __init__(self, device: QInputDevice):
        super().__init__()
        self.device = device

        q_stacked_layout = QStackedLayout(self)
        q_widget = QWidget()
        q_widget.setObjectName("form")
        q_widget.setStyleSheet(
            "#form{border:1px solid #e0e0e0;background-color:#ffffff}"
        )
        q_v_box_layout = QVBoxLayout(q_widget)
        q_v_box_layout.setContentsMargins(24, 24, 24, 24)
        q_v_box_layout.setSpacing(24)

        q_form_layout = QFormLayout()
        q_form_layout.setVerticalSpacing(12)

        self.system_id = QLabel(str(device.systemId()))
        self.system_id.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("system_id", self.system_id)

        self.name = QLabel(device.name())
        self.name.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("name", self.name)

        self.type = QLabel(str(device.type().name))
        self.type.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("type", self.type)

        self.capabilities = QLabel(str(device.capabilities().name))
        self.capabilities.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("capabilities", self.capabilities)

        q_v_box_layout.addLayout(q_form_layout)
        q_stacked_layout.addWidget(q_widget)

    def systemId(self):
        return self.device.systemId()


class List(QWidget):
    def __init__(self):
        super().__init__()
        self.cards: list[Card] = list([])
        self.q_v_box_layout = QVBoxLayout(self)
        self.q_v_box_layout.setContentsMargins(0, 0, 0, 0)
        # self.q_v_box_layout.setSpacing(0)
        for device in QInputDevice.devices():
            card = Card(device)
            self.cards.append(card)
            self.q_v_box_layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignTop)

        self.q_timer = QTimer(self)
        self.q_timer.setInterval(1_000)
        self.q_timer.timeout.connect(self.update)

    def update(self) -> None:
        devices = QInputDevice.devices()

        # Remove cards for devices that no longer exist
        for card in list(
            self.cards
        ):  # Create a copy of the list to avoid modification during iteration
            if card.systemId() not in [device.systemId() for device in devices]:
                self.q_v_box_layout.removeWidget(card)
                self.cards.remove(card)
                card.deleteLater()  # Properly clean up the widget

        # Add cards for new devices
        for device in devices:
            if device.systemId() not in [card.systemId() for card in self.cards]:
                new_card = Card(device)
                self.q_v_box_layout.addWidget(
                    new_card, alignment=Qt.AlignmentFlag.AlignTop
                )
                self.cards.append(new_card)

    def showEvent(self, event: QShowEvent) -> None:
        self.update()
        self.q_timer.start()

        return super().showEvent(event)

    def hideEvent(self, event: QHideEvent) -> None:
        self.q_timer.stop()
        return super().hideEvent(event)


class Widget(Page):
    def __init__(self):
        super().__init__("q_input_device")

        q_widget = QWidget()
        q_h_box_layout = QHBoxLayout(q_widget)
        q_h_box_layout.setContentsMargins(0, 0, 0, 0)
        q_h_box_layout.setSpacing(0)
        c = QWidget()
        c.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )
        c.setMaximumWidth(640)
        q_v_box_layout = QVBoxLayout(c)
        q_v_box_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        q_v_box_layout.setContentsMargins(24, 24, 24, 24)
        q_v_box_layout.setSpacing(24)
        q_v_box_layout.addWidget(List())
        q_h_box_layout.addWidget(c)
        self.setWidget(q_widget)
