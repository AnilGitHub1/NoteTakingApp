"""
Modern Professional Dark Theme stylesheet for PyQt6 / PySide6 Desktop Application.
Matches the Elegant Zinc-Dark design of the Web application.
"""

DARK_STYLESHEET = """
/* Global Application Styling */
QWidget {
    background-color: #09090b;
    color: #e4e4e7;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    font-size: 13px;
    selection-background-color: #4f46e5;
    selection-color: #ffffff;
}

/* Main Window & Panels */
QMainWindow {
    background-color: #09090b;
}

QSplitter::handle {
    background-color: #27272a;
    width: 2px;
}

QSplitter::handle:hover {
    background-color: #4f46e5;
}

/* Sidebar Container */
#sidebarWidget {
    background-color: #121212;
    border-right: 1px solid #27272a;
}

/* Navigation Buttons */
QPushButton.nav-btn {
    background-color: transparent;
    color: #a1a1aa;
    border: none;
    border-radius: 6px;
    padding: 10px 14px;
    text-align: left;
    font-size: 13px;
    font-weight: 500;
}

QPushButton.nav-btn:hover {
    background-color: #18181b;
    color: #ffffff;
}

QPushButton.nav-btn:checked, QPushButton.nav-btn.active {
    background-color: #27272a;
    color: #ffffff;
    font-weight: 600;
}

/* Action Buttons */
QPushButton.primary-btn {
    background-color: #4f46e5;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 8px 18px;
    font-weight: 600;
    font-size: 13px;
}

QPushButton.primary-btn:hover {
    background-color: #4338ca;
}

QPushButton.primary-btn:pressed {
    background-color: #3730a3;
}

QPushButton.secondary-btn {
    background-color: #18181b;
    color: #e4e4e7;
    border: 1px solid #27272a;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 500;
}

QPushButton.secondary-btn:hover {
    background-color: #27272a;
    border-color: #3f3f46;
    color: #ffffff;
}

QPushButton.danger-btn {
    background-color: #1c1917;
    color: #f87171;
    border: 1px solid #7f1d1d;
    border-radius: 6px;
    padding: 6px 14px;
    font-weight: 500;
}

QPushButton.danger-btn:hover {
    background-color: #2e191b;
    border-color: #ef4444;
    color: #fca5a5;
}

/* Quick Filter Buttons */
QPushButton.filter-pill {
    background-color: #18181b;
    border: 1px solid #27272a;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 12px;
    font-weight: 500;
    color: #a1a1aa;
    text-align: left;
}

QPushButton.filter-pill:hover {
    background-color: #27272a;
    color: #ffffff;
}

QPushButton.filter-pill:checked {
    background-color: #27272a;
    border-color: #4f46e5;
    color: #ffffff;
    font-weight: 600;
}

/* Inputs & Form Controls */
QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #18181b;
    color: #e4e4e7;
    border: 1px solid #27272a;
    border-radius: 6px;
    padding: 8px 10px;
    selection-background-color: #4f46e5;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border: 1px solid #4f46e5;
    background-color: #18181b;
}

/* Code Editor specifically */
QTextEdit#codeEditor, QPlainTextEdit#codeEditor, QTextEdit#readOnlyCodeViewer {
    background-color: #000000;
    color: #a5b4fc;
    border: 1px solid #27272a;
    border-radius: 6px;
    font-family: "Cascadia Code", "Fira Code", "Courier New", Courier, monospace;
    font-size: 13px;
    line-height: 1.5;
}

/* ComboBoxes */
QComboBox {
    background-color: #18181b;
    color: #e4e4e7;
    border: 1px solid #27272a;
    border-radius: 6px;
    padding: 6px 10px;
    min-height: 22px;
}

QComboBox:hover {
    border-color: #3f3f46;
}

QComboBox:focus {
    border-color: #4f46e5;
}

QComboBox::drop-down {
    border: none;
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 24px;
}

QComboBox QAbstractItemView {
    background-color: #18181b;
    border: 1px solid #27272a;
    selection-background-color: #4f46e5;
    selection-color: #ffffff;
    color: #e4e4e7;
    outline: none;
}

/* Question List & Cards */
QListWidget {
    background-color: #09090b;
    border: none;
    outline: none;
}

QListWidget::item {
    background-color: #18181b;
    border: 1px solid #27272a;
    border-radius: 6px;
    margin: 4px 6px;
    padding: 0px; /* Crucial: must be 0 when custom item widgets are set to prevent layout shifting/clipping */
}

QListWidget::item:hover {
    background-color: #27272a;
    border-color: #3f3f46;
}

QListWidget::item:selected {
    background-color: #27272a;
    border: 1px solid #4f46e5;
}

/* Labels */
QLabel {
    color: #e4e4e7;
}

QLabel#headingLabel {
    font-size: 20px;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.5px;
}

QLabel#subLabel {
    font-size: 12px;
    color: #71717a;
}

/* Scrollbars */
QScrollBar:vertical {
    background: #09090b;
    width: 8px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #27272a;
    min-height: 24px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background: #3f3f46;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background: #09090b;
    height: 8px;
}

QScrollBar::handle:horizontal {
    background: #27272a;
    min-width: 24px;
    border-radius: 4px;
}
"""
