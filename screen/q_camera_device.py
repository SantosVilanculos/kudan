from PySide6.QtCore import QTimer
from PySide6.QtGui import QFont, QHideEvent, QShowEvent, QTextDocument
from PySide6.QtMultimedia import QMediaDevices
from PySide6.QtWidgets import QTextBrowser, QVBoxLayout, QWidget


class Widget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        q_v_box_layout = QVBoxLayout(self)
        q_v_box_layout.setContentsMargins(0, 0, 0, 0)
        q_v_box_layout.setSpacing(0)
        self.q_text_browser = QTextBrowser()
        self.q_text_browser.setFont(QFont("Inter", int(14 / (96 / 72)), 400))
        q_v_box_layout.addWidget(self.q_text_browser)

        self.q_timer = QTimer(self)
        self.q_timer.setInterval(1_000)
        self.q_timer.timeout.connect(self.q_timer_timeout)

    def q_timer_timeout(self) -> None:
        q_text_document = QTextDocument()
        q_text_document.setPlainText(
            str(
                [
                    f"correction_angle={q_camera_device.correctionAngle()}, description={q_camera_device.description()}, id={q_camera_device.id()}, is_default={q_camera_device.isDefault()}, photo_resolutions={q_camera_device.photoResolutions()}, position={q_camera_device.position()}, video_formats={q_camera_device.videoFormats()}"
                    for q_camera_device in QMediaDevices.videoInputs()
                ]
            )
        )
        self.q_text_browser.setDocument(q_text_document)

    def showEvent(self, event: QShowEvent) -> None:
        self.q_timer_timeout()
        self.q_timer.start()
        return super().showEvent(event)

    def hideEvent(self, event: QHideEvent) -> None:
        self.q_timer.stop()
        return super().hideEvent(event)
