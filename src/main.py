import sys

from PySide6.QtCore import QSize
from PySide6.QtGui import QFont, QFontDatabase, QIcon
from PySide6.QtWidgets import QApplication, QMainWindow

from central_widget import CentralWidget
from environment import APPLICATION_NAME, contents_path


def main():
    q_application = QApplication(sys.argv)

    QFontDatabase.addApplicationFont(str(contents_path("res/font/inter-bold.ttf")))
    QFontDatabase.addApplicationFont(str(contents_path("res/font/inter-medium.ttf")))
    QFontDatabase.addApplicationFont(str(contents_path("res/font/inter-regular.ttf")))
    QFontDatabase.addApplicationFont(str(contents_path("res/font/gitlab_mono.ttf")))

    q_font = QFont("Inter")
    q_font.setPixelSize(13)
    q_font.setWeight(QFont.Weight.Normal)
    q_font.setStyleStrategy(QFont.StyleStrategy.PreferQuality)
    q_application.setFont(q_font)

    q_icon = QIcon(str(cp.joinpath("favicon.ico")))

    q_application.setWindowIcon(QIcon(str(contents_path("favicon.ico"))))

    q_main_window = QMainWindow()
    q_main_window.setMinimumSize(QSize(640, 360))

    central_widget = CentralWidget()
    q_main_window.setCentralWidget(central_widget)

    q_main_window.show()
    sys.exit(q_application.exec())


if __name__ == "__main__":
    main()
