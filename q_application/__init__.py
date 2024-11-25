import sys
from functools import partial

from PySide6.QtCore import QSize
from PySide6.QtGui import QAction, QFontDatabase, QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QMenu, QSystemTrayIcon

from environment import APPLICATION_NAME, contents_path
from q_application.central_widget import CentralWidget
from q_application.q_font import q_font
from q_application.q_palette import q_palette


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


def q_application():
    cp = contents_path()

    _ = QApplication(sys.argv)

    _.setStyle("Fusion")

    _.setPalette(q_palette)

    QFontDatabase.addApplicationFont(str(cp.joinpath("inter/4.0/inter-bold.ttf")))
    QFontDatabase.addApplicationFont(str(cp.joinpath("inter/4.0/inter-medium.ttf")))
    QFontDatabase.addApplicationFont(str(cp.joinpath("inter/4.0/inter-regular.ttf")))
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
