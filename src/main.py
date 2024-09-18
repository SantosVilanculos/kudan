import sys
from functools import partial

from PySide6.QtGui import QAction, QFont, QFontDatabase, QIcon
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

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

    if QSystemTrayIcon.isSystemTrayAvailable():

        def q_system_tray_icon_activated(
            activation_reason: QSystemTrayIcon.ActivationReason,
        ):
            if activation_reason == QSystemTrayIcon.ActivationReason.Trigger:
                window.setVisible(not window.isVisible())

        q_application.setQuitOnLastWindowClosed(False)

        q_system_tray_icon = QSystemTrayIcon()
        q_system_tray_icon.setIcon(QIcon(str(cp.joinpath("icon.ico"))))

        q_menu = QMenu()
        action3 = QAction("Gritting")
        action3.triggered.connect(partial(print, "Olar, Pessoas!"))
        q_menu.addAction(action3)
        quit = QAction("Exit")
        quit.triggered.connect(q_application.quit)
        q_menu.addAction(quit)
        q_system_tray_icon.setContextMenu(q_menu)

        q_system_tray_icon.setVisible(True)
        q_system_tray_icon.activated.connect(q_system_tray_icon_activated)

    window.show()

    sys.exit(q_application.exec())


if __name__ == "__main__":
    main()
