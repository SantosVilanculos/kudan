from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QHideEvent, QShowEvent
from PySide6.QtMultimedia import QCameraDevice, QMediaDevices
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
    def __init__(self, device: QCameraDevice):
        super().__init__()
        self.device = device

        q_stacked_layout = QStackedLayout(self)
        self.q_widget = QWidget()
        self.q_widget.setObjectName("form")
        if device.isDefault():
            self.q_widget.setStyleSheet(
                "#form{border:1px solid #34a853;background-color:#ffffff}"
            )
        else:
            self.q_widget.setStyleSheet(
                "#form{border:1px solid #e0e0e0;background-color:#ffffff}"
            )
        q_v_box_layout = QVBoxLayout(self.q_widget)
        q_v_box_layout.setContentsMargins(24, 24, 24, 24)
        q_v_box_layout.setSpacing(24)

        q_form_layout = QFormLayout()
        q_form_layout.setVerticalSpacing(12)

        self.id = QLabel(str(device.id()))
        self.id.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("id", self.id)

        self.description = QLabel(device.description())
        self.description.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("description", self.description)

        self.is_default = QLabel(str(device.isDefault()))
        self.is_default.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("is_default", self.is_default)

        self.correction_angle = QLabel(device.correctionAngle().name)
        self.correction_angle.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("correction_angle", self.correction_angle)

        self.position = QLabel(device.position().name)
        self.position.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("position", self.position)

        # TODO: photo_resolutions and video_formats

        q_v_box_layout.addLayout(q_form_layout)
        q_stacked_layout.addWidget(self.q_widget)

    def systemId(self) -> int:
        return self.device.id()

    def update(self, device: QCameraDevice):
        if device.isDefault():
            self.q_widget.setStyleSheet(
                "#form{border:1px solid #34a853;background-color:#ffffff}"
            )
        else:
            self.q_widget.setStyleSheet(
                "#form{border:1px solid #e0e0e0;background-color:#ffffff}"
            )
        self.id.setText(str(device.id()))

        self.description.setText(device.description())

        self.is_default.setText(str(device.isDefault()))

        self.correction_angle.setText(device.correctionAngle().name)

        self.position.setText(device.position().name)


class List(QWidget):
    def __init__(self):
        super().__init__()
        self.cards: list[Card] = list([])
        self.q_v_box_layout = QVBoxLayout(self)
        self.q_v_box_layout.setContentsMargins(0, 0, 0, 0)
        for device in QMediaDevices.videoInputs():
            card = Card(device)
            self.cards.append(card)
            self.q_v_box_layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignTop)

        self.q_timer = QTimer(self)
        self.q_timer.setInterval(1_000)
        self.q_timer.timeout.connect(self.update)

    def update(self) -> None:
        devices = QMediaDevices.videoInputs()

        for card in list(self.cards):
            if card.systemId() not in [device.id() for device in devices]:
                self.q_v_box_layout.removeWidget(card)
                self.cards.remove(card)
                card.deleteLater()  # Properly clean up the widget

        for device in devices:
            existing_card = next(
                (card for card in self.cards if card.systemId() == device.id()), None
            )

            if existing_card is None:
                # Create a new card if no card exists for this device
                new_card = Card(device)
                self.q_v_box_layout.addWidget(
                    new_card, alignment=Qt.AlignmentFlag.AlignTop
                )
                self.cards.append(new_card)
            else:
                existing_card.update(device)

    def showEvent(self, event: QShowEvent) -> None:
        self.update()
        self.q_timer.start()

        return super().showEvent(event)

    def hideEvent(self, event: QHideEvent) -> None:
        self.q_timer.stop()
        return super().hideEvent(event)


class Widget(Page):
    def __init__(self):
        super().__init__("q_camera_device")

        self.q_widget = QWidget()
        q_h_box_layout = QHBoxLayout(self.q_widget)
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
        q_v_box_layout.setSpacing(0)
        q_v_box_layout.addWidget(List())
        q_h_box_layout.addWidget(c)
        self.setWidget(self.q_widget)
