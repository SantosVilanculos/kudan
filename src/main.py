import sys

from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import QApplication

from env import contents_path
from window import Window


def main() -> None:
    cp = contents_path()

    q_application = QApplication(sys.argv)

    QFontDatabase.addApplicationFont(str(cp.joinpath("res/font/Inter-Regular.ttf")))
    QFontDatabase.addApplicationFont(str(cp.joinpath("res/font/Inter-Medium.ttf")))
    QFontDatabase.addApplicationFont(str(cp.joinpath("res/font/Inter-Bold.ttf")))
    QFontDatabase.addApplicationFont(
        str(cp.joinpath("res/font/JetBrainsMono-Regular.ttf"))
    )

    q_font = QFont("Inter")
    q_font.setPixelSize(14)
    q_font.setWeight(QFont.Weight.Normal)
    q_font.setStyleStrategy(QFont.StyleStrategy.PreferQuality)
    q_application.setFont(q_font)

    window = Window()
    window.show()

    sys.exit(q_application.exec())


if __name__ == "__main__":
    main()
