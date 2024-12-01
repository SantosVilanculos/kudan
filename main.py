import sys
from functools import partial

from PySide6.QtCore import QSize
from PySide6.QtGui import QAction, QColor, QFont, QFontDatabase, QIcon, QPalette
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

    _ = QApplication(sys.argv)

    _.setStyle("Fusion")

    q_palette = QPalette()
    q_palette.setColor(QPalette.ColorRole.WindowText, QColor("#ffffff"))
    q_palette.setColor(QPalette.ColorRole.Button, QColor("#353535"))
    # q_palette.setColor(QPalette.ColorRole.Light, QColor("#ff0000"))
    # q_palette.setColor(QPalette.ColorRole.Midlight, QColor("#ff0000"))
    # q_palette.setColor(QPalette.ColorRole.Dark, QColor("#ff0000"))
    # q_palette.setColor(QPalette.ColorRole.Mid, QColor("#ff0000"))
    q_palette.setColor(QPalette.ColorRole.Text, QColor("#ffffff"))
    # q_palette.setColor(QPalette.ColorRole.BrightText, QColor("#ff0000"))
    # q_palette.setColor(QPalette.ColorRole.ButtonText, QColor("#ffffff"))
    q_palette.setColor(QPalette.ColorRole.Base, QColor("#3b3b3b"))
    q_palette.setColor(QPalette.ColorRole.Window, QColor("#2b2b2b"))
    # q_palette.setColor(QPalette.ColorRole.Shadow, QColor("#ff0000"))
    q_palette.setColor(QPalette.ColorRole.Highlight, QColor("#2979ff"))
    q_palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
    # q_palette.setColor(QPalette.ColorRole.Link, QColor("#ff0000"))
    # q_palette.setColor(QPalette.ColorRole.LinkVisited, QColor("#ff0000"))
    q_palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#2b2b2b"))
    # q_palette.setColor(QPalette.ColorRole.NoRole, QColor("#ff0000"))
    # q_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#ff0000"))
    # q_palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#ff0000"))
    # q_palette.setColor(QPalette.ColorRole.PlaceholderText, QColor("#ff0000"))
    # q_palette.setColor(QPalette.ColorRole.Accent, QColor("#ff0000"))
    # q_palette.setColor(QPalette.ColorRole.NColorRoles, QColor("#ff0000"))

    _.setPalette(q_palette)

    QFontDatabase.addApplicationFont(str(cp.joinpath("inter/4.0/inter-bold.ttf")))
    QFontDatabase.addApplicationFont(str(cp.joinpath("inter/4.0/inter-medium.ttf")))
    QFontDatabase.addApplicationFont(str(cp.joinpath("inter/4.0/inter-regular.ttf")))

    q_font = QFont("Inter")
    q_font.setPixelSize(13)
    q_font.setWeight(QFont.Weight.Normal)
    q_font.setStyleStrategy(QFont.StyleStrategy.PreferQuality)

    _.setFont(q_font)

    q_icon = QIcon(str(cp.joinpath("favicon.ico")))

    q_main_window = QMainWindow()
    q_main_window.setWindowIcon(q_icon)
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
        q_action_2.triggered.connect(_.quit)
        q_menu.addAction(q_action_2)

        q_system_tray_icon.setContextMenu(q_menu)
        q_system_tray_icon.show()
        _.setQuitOnLastWindowClosed(not q_system_tray_icon.isVisible())

    q_main_window.show()
    sys.exit(_.exec())


if __name__ == "__main__":
    main()
