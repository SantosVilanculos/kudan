from PySide6.QtGui import QColor, QPalette


def q_palette() -> QPalette:
    _ = QPalette()
    _.setColor(QPalette.ColorRole.WindowText, QColor("#ffffff"))
    _.setColor(QPalette.ColorRole.Button, QColor("#353535"))
    # _.setColor(QPalette.ColorRole.Light, QColor("#ff0000"))
    # _.setColor(QPalette.ColorRole.Midlight, QColor("#ff0000"))
    # _.setColor(QPalette.ColorRole.Dark, QColor("#ff0000"))
    # _.setColor(QPalette.ColorRole.Mid, QColor("#ff0000"))
    _.setColor(QPalette.ColorRole.Text, QColor("#ffffff"))
    # _.setColor(QPalette.ColorRole.BrightText, QColor("#ff0000"))
    # _.setColor(QPalette.ColorRole.ButtonText, QColor("#ffffff"))
    _.setColor(QPalette.ColorRole.Base, QColor("#3b3b3b"))
    _.setColor(QPalette.ColorRole.Window, QColor("#2b2b2b"))
    # _.setColor(QPalette.ColorRole.Shadow, QColor("#ff0000"))
    _.setColor(QPalette.ColorRole.Highlight, QColor("#2979ff"))
    _.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
    # _.setColor(QPalette.ColorRole.Link, QColor("#ff0000"))
    # _.setColor(QPalette.ColorRole.LinkVisited, QColor("#ff0000"))
    _.setColor(QPalette.ColorRole.AlternateBase, QColor("#2b2b2b"))
    # _.setColor(QPalette.ColorRole.NoRole, QColor("#ff0000"))
    # _.setColor(QPalette.ColorRole.ToolTipBase, QColor("#ff0000"))
    # _.setColor(QPalette.ColorRole.ToolTipText, QColor("#ff0000"))
    # _.setColor(QPalette.ColorRole.PlaceholderText, QColor("#ff0000"))
    # _.setColor(QPalette.ColorRole.Accent, QColor("#ff0000"))
    # _.setColor(QPalette.ColorRole.NColorRoles, QColor("#ff0000"))
    return _
