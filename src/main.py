import sys

from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import QApplication

from env import contents_directory_path
from window import Window


def main() -> None:
    PATH = contents_directory_path()

    application = QApplication(sys.argv)
    QFontDatabase.addApplicationFont(str(PATH.joinpath("Inter-Regular.ttf")))
    QFontDatabase.addApplicationFont(str(PATH.joinpath("Inter-Medium.ttf")))
    QFontDatabase.addApplicationFont(str(PATH.joinpath("Inter-Bold.ttf")))
    QFontDatabase.addApplicationFont(str(PATH.joinpath("JetBrainsMono-Regular.ttf")))
    application.setFont(QFont("Inter", int(14 / (96 / 72)), 400))

    window = Window()
    window.show()

    sys.exit(application.exec())


if __name__ == "__main__":
    main()
