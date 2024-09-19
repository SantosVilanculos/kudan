import sys
from functools import partial

from PySide6.QtGui import QAction, QDesktopServices, QFont, QFontDatabase, QIcon
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

from environment import GITHUB_REPOSITORY_URL, contents_path
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
    q_font.setPixelSize(13)
    q_font.setWeight(QFont.Weight.Normal)
    q_font.setStyleStrategy(QFont.StyleStrategy.PreferQuality)
    q_application.setFont(q_font)

    window = Window()

    if QSystemTrayIcon.isSystemTrayAvailable():
        q_application.setQuitOnLastWindowClosed(False)

        q_system_tray_icon = QSystemTrayIcon(window)
        q_system_tray_icon.setIcon(QIcon(str(cp.joinpath("icon.ico"))))

        def q_system_tray_icon_activated(ar: QSystemTrayIcon.ActivationReason) -> None:
            if ar == QSystemTrayIcon.ActivationReason.Trigger:
                print(q_system_tray_icon.geometry())
            elif ar == QSystemTrayIcon.ActivationReason.DoubleClick:
                window.setVisible(not window.isVisible())

        q_system_tray_icon.activated.connect(q_system_tray_icon_activated)

        q_menu = QMenu()
        q_font.setPixelSize(12)
        q_menu.setFont(q_font)

        documentation = QAction("Documentation")
        documentation.triggered.connect(
            partial(QDesktopServices.openUrl, GITHUB_REPOSITORY_URL)
        )
        q_menu.addAction(documentation)

        report_bug = QAction("Report bug")
        report_bug.triggered.connect(
            partial(QDesktopServices.openUrl, f"{GITHUB_REPOSITORY_URL}/issues/new")
        )
        q_menu.addAction(report_bug)

        q_menu.addSeparator()

        quit = QAction("Exit")
        quit.triggered.connect(q_application.quit)
        q_menu.addAction(quit)

        q_system_tray_icon.setContextMenu(q_menu)

        q_system_tray_icon.show()

    window.show()

    sys.exit(q_application.exec())


if __name__ == "__main__":
    main()
