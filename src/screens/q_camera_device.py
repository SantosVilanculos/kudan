from PySide6.QtCore import QSize, Qt, QTimer
from PySide6.QtGui import (QColor, QFont, QHideEvent, QPainter, QPaintEvent,
                           QShowEvent)
from PySide6.QtMultimedia import QCameraDevice, QCameraFormat, QMediaDevices
from PySide6.QtWidgets import (QFormLayout, QHBoxLayout, QLabel, QScrollArea,
                               QSizePolicy, QStyle, QStyleOption, QVBoxLayout,
                               QWidget)


class PhotoResolutions(QWidget):
    def __init__(self, photo_resolutions: list[QSize]) -> None:
        super().__init__()

        q_v_box_layout = QVBoxLayout(self)
        q_v_box_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        q_v_box_layout.setContentsMargins(0, 0, 0, 0)

        for q_size in photo_resolutions:
            q_label = QLabel(f"{q_size.width()} x {q_size.height()}")
            q_v_box_layout.addWidget(q_label)


class VideoFormats(QWidget):
    def __init__(self, video_formats: list[QCameraFormat]) -> None:
        super().__init__()

        q_v_box_layout = QVBoxLayout(self)
        q_v_box_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        q_v_box_layout.setContentsMargins(0, 0, 0, 0)

        for q_camemera_format in video_formats:
            q_widget = QWidget()
            q_color = QColor(Qt.GlobalColor.lightGray)
            q_widget.setObjectName("name")
            q_widget.setStyleSheet(f"#name{{background-color:{q_color.name()}}}")
            q_form_layout = QFormLayout(q_widget)
            q_form_layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
            q_form_layout.addRow(
                self.q_label("maxFrameRate"),
                QLabel(str(q_camemera_format.maxFrameRate())),
            )
            q_form_layout.addRow(
                self.q_label("minFrameRate"),
                QLabel(str(q_camemera_format.minFrameRate())),
            )
            q_form_layout.addRow(
                self.q_label("pixelFormat"),
                QLabel(str(q_camemera_format.pixelFormat().name)),
            )
            q_form_layout.addRow(
                self.q_label("resolution"),
                QLabel(
                    f"{q_camemera_format.resolution().width()} x {
                        q_camemera_format.resolution().height()}"
                ),
            )
            q_v_box_layout.addWidget(q_widget)

    def q_label(self, text: str) -> QLabel:
        q_label = QLabel(text)
        q_font = q_label.font()
        q_font.setWeight(QFont.Weight.Medium)
        q_label.setFont(q_font)
        return q_label


class ListItem(QWidget):
    def __init__(self, q_camera_device: QCameraDevice) -> None:
        super().__init__()

        self.q_camera_device = q_camera_device

        self.setObjectName("undefined")

        if q_camera_device.isDefault():
            q_color = QColor(Qt.GlobalColor.darkGreen)
            self.setStyleSheet(
                f"#undefined{{border: 1px solid {
                    q_color.name()};background-color:white}}"
            )
        else:
            q_color = QColor(Qt.GlobalColor.lightGray)
            self.setStyleSheet(
                f"#undefined{{border: 1px solid {
                    q_color.name()};background-color:white}}"
            )

        q_form_layout = QFormLayout(self)
        q_form_layout.setVerticalSpacing(24)
        id = QLabel(q_camera_device.id().toStdString())
        q_form_layout.addRow("id", id)
        description = QLabel(q_camera_device.description())
        q_form_layout.addRow("description", description)
        self.is_default = QLabel(str(q_camera_device.isDefault()))
        q_form_layout.addRow("isDefault", self.is_default)
        self.correction_angle = QLabel(q_camera_device.correctionAngle().name)
        q_form_layout.addRow("correctionAngle", self.correction_angle)
        self.position = QLabel(q_camera_device.position().name)
        q_form_layout.addRow("position", self.position)
        q_form_layout.addRow(
            "photoResolutions",
            PhotoResolutions(q_camera_device.photoResolutions()),
        )
        q_form_layout.addRow(
            "videoFormats", VideoFormats(q_camera_device.videoFormats())
        )

    def paintEvent(self, event: QPaintEvent) -> None:
        q_style_option = QStyleOption()
        q_style_option.initFrom(self)
        q_painter = QPainter(self)
        self.style().drawPrimitive(
            QStyle.PrimitiveElement.PE_Widget, q_style_option, q_painter, self
        )

    def update(self, q_camera_device: QCameraDevice) -> None:
        if q_camera_device.isDefault():
            q_color = QColor(Qt.GlobalColor.darkGreen)
            self.setStyleSheet(
                f"#undefined{{border: 1px solid {
                    q_color.name()};background-color:white}}"
            )
        else:
            q_color = QColor(Qt.GlobalColor.lightGray)
            self.setStyleSheet(
                f"#undefined{{border: 1px solid {
                    q_color.name()};background-color:white}}"
            )

        self.is_default.setText(str(q_camera_device.isDefault()))
        self.correction_angle.setText((str(q_camera_device.correctionAngle().name)))
        self.position.setText(str(q_camera_device.position().name))


class List(QWidget):
    def __init__(self):
        super().__init__()

        self.q_v_box_layout = QVBoxLayout(self)
        self.q_v_box_layout.setContentsMargins(0, 0, 0, 0)
        self.q_v_box_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for q_camera_device in QMediaDevices.videoInputs():
            self.q_v_box_layout.addWidget(ListItem(q_camera_device))

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
        _A = QMediaDevices.videoInputs()
        _B: list[str] = [q_camera_device.id().toStdString() for q_camera_device in _A]
        _C: list[str] = list()

        for index in range(self.q_v_box_layout.count()):
            q_layout_item = self.q_v_box_layout.itemAt(index)

            if not q_layout_item:
                continue

            q_widget = q_layout_item.widget()

            if not isinstance(q_widget, ListItem):
                continue

            if q_widget.q_camera_device.id().toStdString() not in _B:
                self.q_v_box_layout.removeWidget(q_widget)
                q_widget.deleteLater()
            else:
                _C.append(q_widget.q_camera_device.id().toStdString())
                q_camera_device = next(
                    (
                        q_camera_device
                        for q_camera_device in _A
                        if q_camera_device.id().toStdString()
                        == q_widget.q_camera_device.id().toStdString()
                    ),
                    None,
                )
                if q_camera_device:
                    q_widget.update(q_camera_device)

        for q_camera_device in _A:
            if q_camera_device.id().toStdString() not in _C:
                self.q_v_box_layout.addWidget(ListItem(q_camera_device))


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
