from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QGuiApplication, QHideEvent, QScreen, QShowEvent
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
    def __init__(self, screen: QScreen):
        super().__init__()
        self.screen = screen

        q_stacked_layout = QStackedLayout(self)
        self.q_widget = QWidget()
        self.q_widget.setObjectName("form")

        self.q_widget.setStyleSheet(
            "#form{border:1px solid #e0e0e0;background-color:#ffffff}"
        )
        q_v_box_layout = QVBoxLayout(self.q_widget)
        q_v_box_layout.setContentsMargins(24, 24, 24, 24)
        q_v_box_layout.setSpacing(24)

        q_form_layout = QFormLayout()
        q_form_layout.setVerticalSpacing(12)

        self.name = QLabel(screen.name())
        self.name.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("name", self.name)

        self.size = QLabel(str(screen.size()))
        self.size.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("size", self.size)

        self.depth = QLabel(str(screen.depth()))
        self.depth.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("depth", self.depth)

        self.device_pixel_ratio = QLabel(str(screen.devicePixelRatio()))
        self.device_pixel_ratio.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("device_pixel_ratio", self.device_pixel_ratio)

        self.refresh_rate = QLabel(str(screen.refreshRate()))
        self.refresh_rate.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("refresh_rate", self.refresh_rate)

        self.model = QLabel(screen.model())
        self.model.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("model", self.model)

        self.serial_number = QLabel(screen.serialNumber())
        self.serial_number.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("serial_number", self.serial_number)

        self.manufacturer = QLabel(screen.manufacturer())
        self.manufacturer.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("manufacturer", self.manufacturer)

        self.native_interface = QLabel(str(screen.nativeInterface()))
        self.native_interface.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("native_interface", self.native_interface)

        self.orientation = QLabel(screen.orientation().name)
        self.orientation.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("orientation", self.orientation)

        self.native_orientation = QLabel(screen.nativeOrientation().name)
        self.native_orientation.setAlignment(Qt.AlignmentFlag.AlignRight)
        q_form_layout.addRow("native_orientation", self.native_orientation)

        q_v_box_layout.addLayout(q_form_layout)
        q_stacked_layout.addWidget(self.q_widget)

    def nameId(self) -> str:
        return self.screen.name()

    def update(self, screen: QScreen):
        self.device_pixel_ratio.setText(str(screen.devicePixelRatio()))

        self.refresh_rate.setText(str(screen.refreshRate()))

        self.model.setText(screen.model())

        self.serial_number.setText(screen.serialNumber())

        self.manufacturer.setText(screen.manufacturer())

        self.native_interface.setText(str(screen.nativeInterface()))

        self.orientation.setText(screen.orientation().name)

        self.native_orientation.setText(screen.nativeOrientation().name)


class List(QWidget):
    def __init__(self):
        super().__init__()
        self.cards: list[Card] = list([])
        self.q_v_box_layout = QVBoxLayout(self)
        self.q_v_box_layout.setContentsMargins(0, 0, 0, 0)
        for screen in QGuiApplication.screens():
            card = Card(screen)
            self.cards.append(card)
            self.q_v_box_layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignTop)

        self.q_timer = QTimer(self)
        self.q_timer.setInterval(1_000)
        self.q_timer.timeout.connect(self.update)

    def update(self) -> None:
        devices = QGuiApplication.screens()

        for card in list(self.cards):
            if card.nameId() not in [screen.name() for screen in devices]:
                self.q_v_box_layout.removeWidget(card)
                self.cards.remove(card)
                card.deleteLater()  # Properly clean up the widget

        for screen in devices:
            existing_card = next(
                (card for card in self.cards if card.nameId() == screen.name()), None
            )

            if existing_card is None:
                # Create a new card if no card exists for this screen
                new_card = Card(screen)
                self.q_v_box_layout.addWidget(
                    new_card, alignment=Qt.AlignmentFlag.AlignTop
                )
                self.cards.append(new_card)
            else:
                existing_card.update(screen)

    def showEvent(self, event: QShowEvent) -> None:
        self.update()
        self.q_timer.start()

        return super().showEvent(event)

    def hideEvent(self, event: QHideEvent) -> None:
        self.q_timer.stop()
        return super().hideEvent(event)


class Widget(Page):
    def __init__(self):
        super().__init__("screen")

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
