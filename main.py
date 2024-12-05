import sys
from functools import partial

from PySide6.QtCore import QSize
from PySide6.QtGui import QAction, QFont, QFontDatabase, QIcon, QPalette
from PySide6.QtWidgets import QApplication, QMainWindow, QMenu, QSystemTrayIcon

from central_widget import CentralWidget
from environment import APPLICATION_NAME, contents_path


def q_system_tray_icon_activated(
    activation_reason: QSystemTrayIcon.ActivationReason, q_main_window: QMainWindow
) -> None:
    if activation_reason != QSystemTrayIcon.ActivationReason.Context:
        q_main_window.setVisible(not q_main_window.isVisible())


def q_action_1_triggered(q_action: QAction, q_main_window: QMainWindow) -> None:
    q_main_window.setVisible(not q_main_window.isVisible())

    if q_main_window.isVisible():
        q_action.setText("Hide")
    else:
        q_action.setText("Show")


def main():
    cp = contents_path()

    q_application = QApplication(sys.argv)

    # q_application.setStyle("Fusion")

    q_palette = QPalette()
    # q_palette.setColor(QPalette.ColorRole.WindowText, QColor("#e0e0e0"))
    # q_palette.setColor(QPalette.ColorRole.Button, QColor("#353535"))
    # q_palette.setColor(QPalette.ColorRole.Light, QColor("#4a4a4a"))
    # q_palette.setColor(QPalette.ColorRole.Midlight, QColor("#3d3d3d"))
    # q_palette.setColor(QPalette.ColorRole.Dark, QColor("#202020"))
    # q_palette.setColor(QPalette.ColorRole.Mid, QColor("#2c2c2c"))
    # q_palette.setColor(QPalette.ColorRole.Text, QColor("#f0f0f0"))
    # q_palette.setColor(QPalette.ColorRole.BrightText, QColor("#ffffff"))
    # q_palette.setColor(QPalette.ColorRole.ButtonText, QColor("#e6e6e6"))
    # q_palette.setColor(QPalette.ColorRole.Base, QColor("#2c2c2c"))
    # q_palette.setColor(QPalette.ColorRole.Window, QColor("#1e1e1e"))
    # q_palette.setColor(QPalette.ColorRole.Shadow, QColor("#121212"))
    # q_palette.setColor(QPalette.ColorRole.Highlight, QColor("#4a4a4a"))
    # q_palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
    # q_palette.setColor(QPalette.ColorRole.Link, QColor("#5a9eff"))
    # q_palette.setColor(QPalette.ColorRole.LinkVisited, QColor("#7b64ff"))
    # q_palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#2a2a2a"))
    # q_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#3a3a3a"))
    # q_palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#e0e0e0"))
    # q_palette.setColor(QPalette.ColorRole.PlaceholderText, QColor("#707070"))
    # q_palette.setColor(QPalette.ColorRole.Accent, QColor("#ff0000"))
    # q_palette.setColor(QPalette.ColorRole.NColorRoles, QColor("#ff0000"))
    q_application.setPalette(q_palette)

    QFontDatabase.addApplicationFont(str(cp.joinpath("inter/4.0/inter-bold.ttf")))
    QFontDatabase.addApplicationFont(str(cp.joinpath("inter/4.0/inter-medium.ttf")))
    QFontDatabase.addApplicationFont(str(cp.joinpath("inter/4.0/inter-regular.ttf")))

    q_font = QFont("Inter")
    q_font.setPixelSize(13)
    q_font.setWeight(QFont.Weight.Normal)
    q_font.setStyleStrategy(QFont.StyleStrategy.PreferQuality)

    q_application.setFont(q_font)
    q_icon = QIcon(str(cp.joinpath("favicon.ico")))
    q_application.setWindowIcon(q_icon)

    q_main_window = QMainWindow()
    q_main_window.setWindowTitle(APPLICATION_NAME)
    q_main_window.setMinimumSize(QSize(640, 360))

    central_widget = CentralWidget()
    q_main_window.setCentralWidget(central_widget)

    if QSystemTrayIcon.isSystemTrayAvailable():
        q_system_tray_icon = QSystemTrayIcon(q_main_window)

        q_system_tray_icon.setIcon(q_icon)

        q_system_tray_icon.activated.connect(
            lambda activation_reason: q_system_tray_icon_activated(
                activation_reason, q_main_window
            )
        )

        q_menu = QMenu()
        q_font.setPixelSize(12)
        q_menu.setFont(q_font)

        q_action_1 = QAction("Hide")
        q_action_1.triggered.connect(
            partial(q_action_1_triggered, q_action_1, q_main_window)
        )
        q_main_window.showEvent = lambda q_show_event: q_action_1.setText("Hide")
        q_main_window.hideEvent = lambda q_hide_event: q_action_1.setText("Show")
        q_menu.addAction(q_action_1)

        # q_menu.addSeparator()

        q_action_2 = QAction("Exit")
        q_action_2.triggered.connect(q_application.quit)
        q_menu.addAction(q_action_2)

        q_system_tray_icon.setContextMenu(q_menu)
        q_system_tray_icon.show()
        q_application.setQuitOnLastWindowClosed(not q_system_tray_icon.isVisible())

    q_main_window.show()
    sys.exit(q_application.exec())


if __name__ == "__main__":
    main()
