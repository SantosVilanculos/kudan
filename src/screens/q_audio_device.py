from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QFont, QHideEvent, QPainter, QPaintEvent, QShowEvent
from PySide6.QtMultimedia import QAudioDevice, QAudioFormat, QMediaDevices
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


class PreferredFormat(QWidget):
    def __init__(self, q_audio_format: QAudioFormat) -> None:
        super().__init__()

        q_v_box_layout = QVBoxLayout(self)
        q_v_box_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        q_v_box_layout.setContentsMargins(0, 0, 0, 0)

        q_widget = QWidget()
        q_color = QColor(Qt.GlobalColor.lightGray)
        q_widget.setObjectName("name")
        q_widget.setStyleSheet(f"#name{{background-color:{q_color.name()}}}")
        q_form_layout = QFormLayout(q_widget)
        q_form_layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
        self.bytes_per_frame = QLabel(str(q_audio_format.bytesPerFrame()))
        q_form_layout.addRow(self.q_label("bytesPerFrame"), self.bytes_per_frame)
        self.bytes_per_sample = QLabel(str(q_audio_format.bytesPerSample()))
        q_form_layout.addRow(self.q_label("bytesPerSample"), self.bytes_per_sample)
        self.channel_count = QLabel(str(q_audio_format.channelCount()))
        q_form_layout.addRow(self.q_label("channelCount"), self.channel_count)
        self.channel_config = QLabel(q_audio_format.channelConfig().name)
        q_form_layout.addRow(self.q_label("channelConfig"), self.channel_config)
        self.sample_rate = QLabel(f"{q_audio_format.sampleRate()} Hz")
        q_form_layout.addRow(self.q_label("sampleRate"), self.sample_rate)
        self.sample_format = QLabel(q_audio_format.sampleFormat().name)
        q_form_layout.addRow(self.q_label("sampleFormat"), self.sample_format)

        q_v_box_layout.addWidget(q_widget)

    def q_label(self, text: str) -> QLabel:
        q_label = QLabel(text)
        q_font = q_label.font()
        q_font.setWeight(QFont.Weight.Medium)
        q_label.setFont(q_font)
        return q_label

    def update(self, q_audio_format: QAudioFormat) -> None:
        self.bytes_per_frame.setText(str(q_audio_format.bytesPerFrame()))
        self.bytes_per_sample.setText(str(q_audio_format.bytesPerSample()))
        self.channel_count.setText(str(q_audio_format.channelCount()))
        self.channel_config.setText(q_audio_format.channelConfig().name)
        self.sample_rate.setText(f"{q_audio_format.sampleRate()} Hz")
        self.sample_format.setText(q_audio_format.sampleFormat().name)


class SupportedSampleFormats(QWidget):
    def __init__(
        self, supported_sample_formats: list[QAudioFormat.SampleFormat]
    ) -> None:
        super().__init__()

        q_v_box_layout = QVBoxLayout(self)
        q_v_box_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        q_v_box_layout.setContentsMargins(0, 0, 0, 0)

        for sample_format in supported_sample_formats:
            q_label = QLabel(sample_format.name)
            q_v_box_layout.addWidget(q_label)


class ListItem(QWidget):
    def __init__(self, q_audio_device: QAudioDevice) -> None:
        super().__init__()

        self.q_audio_device = q_audio_device

        self.setObjectName("undefined")

        if q_audio_device.isDefault():
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
        id = QLabel(q_audio_device.id().toStdString())
        q_form_layout.addRow("id", id)
        description = QLabel(q_audio_device.description())
        q_form_layout.addRow("description", description)
        mode = QLabel(str(q_audio_device.mode().name))
        q_form_layout.addRow("mode", mode)
        channel_configuration = QLabel(str(q_audio_device.channelConfiguration().name))
        q_form_layout.addRow("channelConfiguration", channel_configuration)
        self.is_default = QLabel(str(q_audio_device.isDefault()))
        q_form_layout.addRow("isDefault", self.is_default)
        minimum_channel_count = QLabel(str((q_audio_device.minimumChannelCount())))
        q_form_layout.addRow("minimumChannelCount", minimum_channel_count)
        maximum_channel_count = QLabel(str(q_audio_device.maximumChannelCount()))
        q_form_layout.addRow("maximumChannelCount", maximum_channel_count)
        minimum_sample_rate = QLabel(f"{q_audio_device.minimumSampleRate()} Hz")
        q_form_layout.addRow("minimumSampleRate", minimum_sample_rate)
        maximum_sample_rate = QLabel(f"{q_audio_device.maximumSampleRate()} Hz")
        q_form_layout.addRow("maximumSampleRate", maximum_sample_rate)
        q_form_layout.addRow(
            "supportedSampleFormats",
            SupportedSampleFormats(q_audio_device.supportedSampleFormats()),
        )
        self.preferred_format = PreferredFormat(q_audio_device.preferredFormat())
        q_form_layout.addRow("preferredFormat", self.preferred_format)

    def paintEvent(self, event: QPaintEvent) -> None:
        q_style_option = QStyleOption()
        q_style_option.initFrom(self)
        q_painter = QPainter(self)

        self.style().drawPrimitive(
            QStyle.PrimitiveElement.PE_Widget, q_style_option, q_painter, self
        )

    def update(self, q_audio_device: QAudioDevice) -> None:
        if q_audio_device.isDefault():
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

        self.is_default.setText(str(q_audio_device.isDefault()))
        self.preferred_format.update(q_audio_device.preferredFormat())


class AudioInputsList(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.q_v_box_layout = QVBoxLayout(self)
        self.q_v_box_layout.setContentsMargins(0, 0, 0, 0)
        self.q_v_box_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for q_audio_device in QMediaDevices.audioInputs():
            self.q_v_box_layout.addWidget(ListItem(q_audio_device))

    def update(self) -> None:
        _A = QMediaDevices.audioInputs()
        _B: list[str] = [q_audio_device.id().toStdString() for q_audio_device in _A]
        _C: list[str] = list()

        for index in range(self.q_v_box_layout.count()):
            q_widget = self.q_v_box_layout.itemAt(index).widget()

            if not isinstance(q_widget, ListItem):
                continue

            if q_widget.q_audio_device.id().toStdString() not in _B:
                self.q_v_box_layout.removeWidget(q_widget)
                q_widget.deleteLater()
            else:
                _C.append(q_widget.q_audio_device.id().toStdString())
                q_input_device = next(
                    (
                        q_input_device
                        for q_input_device in _A
                        if q_input_device.id().toStdString()
                        == q_widget.q_audio_device.id().toStdString()
                    ),
                    None,
                )
                if q_input_device:
                    q_widget.update(q_input_device)

            for q_input_device in _A:
                if q_input_device.id().toStdString() not in _C:
                    self.q_v_box_layout.addWidget(ListItem(q_input_device))


class AudioOutputsList(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.q_v_box_layout = QVBoxLayout(self)
        self.q_v_box_layout.setContentsMargins(0, 0, 0, 0)
        self.q_v_box_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for q_audio_device in QMediaDevices.audioOutputs():
            self.q_v_box_layout.addWidget(ListItem(q_audio_device))

    def update(self) -> None:
        _A = QMediaDevices.audioOutputs()
        _B: list[str] = [q_audio_device.id().toStdString() for q_audio_device in _A]
        _C: list[str] = list()

        for index in range(self.q_v_box_layout.count()):
            q_widget = self.q_v_box_layout.itemAt(index).widget()

            if not isinstance(q_widget, ListItem):
                continue

            if q_widget.q_audio_device.id().toStdString() not in _B:
                self.q_v_box_layout.removeWidget(q_widget)
                q_widget.deleteLater()
            else:
                _C.append(q_widget.q_audio_device.id().toStdString())
                q_input_device = next(
                    (
                        q_input_device
                        for q_input_device in _A
                        if q_input_device.id().toStdString()
                        == q_widget.q_audio_device.id().toStdString()
                    ),
                    None,
                )
                if q_input_device:
                    q_widget.update(q_input_device)

        for q_input_device in _A:
            if q_input_device.id().toStdString() not in _C:
                self.q_v_box_layout.addWidget(ListItem(q_input_device))


class Widget(QScrollArea):
    def __init__(self) -> None:
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
        q_v_box_layout.addWidget(QLabel("audioInputs"))
        self.audio_inputs = AudioInputsList()
        q_v_box_layout.addWidget(self.audio_inputs)
        q_v_box_layout.addWidget(QLabel("audioOutputs"))
        self.audio_outputs = AudioOutputsList()
        q_v_box_layout.addWidget(self.audio_outputs)
        q_h_box_layout.addWidget(main)
        self.setWidget(q_widget)

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
        self.audio_inputs.update()
        self.audio_outputs.update()
