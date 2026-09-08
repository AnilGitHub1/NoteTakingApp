"""
Modern Professional Dark Theme stylesheet for PyQt6 / PySide6 Desktop Application.
"""

DARK_STYLESHEET = """
/* Global Application Styling */
QWidget {
    background-color: #121316;
    color: #e5e7eb;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    font-size: 13px;
    selection-background-color: #4f46e5;
    selection-color: #ffffff;
}

/* Main Window & Panels */
QMainWindow {
    background-color: #121316;
}

QSplitter::handle {
    background-color: #262930;
    width: 2px;
}

QSplitter::handle:hover {
    background-color: #6366f1;
}

/* Sidebar Container */
#sidebarWidget {
    background-color: #17181c;
    border-right: 1px solid #272a31;
}

/* Navigation Buttons */
QPushButton.nav-btn {
    background-color: transparent;
    color: #9ca3af;
    border: none;
    border-radius: 8px;
    padding: 10px 14px;
    text-align: left;
    font-size: 13px;
    font-weight: 500;
}

QPushButton.nav-btn:hover {
    background-color: #212329;
    color: #f3f4f6;
}

QPushButton.nav-btn:checked, QPushButton.nav-btn.active {
    background-color: #2d3039;
    color: #ffffff;
    font-weight: 600;
    border-left: 3px solid #6366f1;
}

/* Action Buttons */
QPushButton.primary-btn {
    background-color: #6366f1;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 8px 18px;
    font-weight: 600;
    font-size: 13px;
}

QPushButton.primary-btn:hover {
    background-color: #4f46e5;
}

QPushButton.primary-btn:pressed {
    background-color: #4338ca;
}

QPushButton.secondary-btn {
    background-color: #22242a;
    color: #e5e7eb;
    border: 1px solid #363a45;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 500;
}

QPushButton.secondary-btn:hover {
    background-color: #2a2d36;
    border-color: #4b5262;
    color: #ffffff;
}

QPushButton.danger-btn {
    background-color: #2a1b1d;
    color: #f87171;
    border: 1px solid #7f1d1d;
    border-radius: 6px;
    padding: 6px 14px;
    font-weight: 500;
}

QPushButton.danger-btn:hover {
    background-color: #3e1b1e;
    border-color: #ef4444;
    color: #fca5a5;
}

/* Quick Filter Buttons */
QPushButton.filter-pill {
    background-color: #1e2026;
    border: 1px solid #2e323b;
    border-radius: 14px;
    padding: 5px 12px;
    font-size: 12px;
    font-weight: 500;
    color: #9ca3af;
}

QPushButton.filter-pill:hover {
    background-color: #272a33;
    color: #f3f4f6;
}

QPushButton.filter-pill:checked {
    background-color: #2e3340;
    border-color: #6366f1;
    color: #ffffff;
}

/* Inputs & Form Controls */
QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #18191e;
    color: #f3f4f6;
    border: 1px solid #2d3039;
    border-radius: 6px;
    padding: 8px 10px;
    selection-background-color: #4f46e5;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border: 1px solid #6366f1;
    background-color: #1c1d24;
}

/* Code Editor specifically */
QTextEdit#codeEditor, QPlainTextEdit#codeEditor, QTextEdit#readOnlyCodeViewer {
    background-color: #15161b;
    color: #abb2bf;
    border: 1px solid #292c35;
    border-radius: 6px;
    font-family: "Cascadia Code", "Fira Code", "Courier New", Courier, monospace;
    font-size: 13px;
    line-height: 1.5;
}

/* ComboBoxes */
QComboBox {
    background-color: #18191e;
    color: #e5e7eb;
    border: 1px solid #2d3039;
    border-radius: 6px;
    padding: 6px 10px;
    min-height: 22px;
}

QComboBox:hover {
    border-color: #3e4350;
}

QComboBox:focus {
    border-color: #6366f1;
}

QComboBox::drop-down {
    border: none;
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 24px;
}

QComboBox QAbstractItemView {
    background-color: #1c1d24;
    border: 1px solid #363a45;
    selection-background-color: #4f46e5;
    selection-color: #ffffff;
    color: #e5e7eb;
    outline: none;
}

/* Question List & Cards */
QListWidget {
    background-color: #141519;
    border: none;
    outline: none;
}

QListWidget::item {
    background-color: #18191f;
    border: 1px solid #272a33;
    border-radius: 8px;
    margin: 4px 6px;
    padding: 10px;
}

QListWidget::item:hover {
    background-color: #1f2129;
    border-color: #3b3f4d;
}

QListWidget::item:selected {
    background-color: #252833;
    border: 1px solid #6366f1;
}

/* Labels */
QLabel {
    color: #e5e7eb;
}

QLabel#headingLabel {
    font-size: 18px;
    font-weight: 700;
    color: #ffffff;
}

QLabel#subLabel {
    font-size: 12px;
    color: #9ca3af;
}

/* Difficulty Badges */
.badge-easy {
    background-color: rgba(34, 197, 94, 0.15);
    color: #4ade80;
    border: 1px solid rgba(34, 197, 94, 0.4);
    border-radius: 12px;
    padding: 3px 10px;
    font-weight: 600;
    font-size: 11px;
}

.badge-medium {
    background-color: rgba(245, 158, 11, 0.15);
    color: #fbbf24;
    border: 1px solid rgba(245, 158, 11, 0.4);
    border-radius: 12px;
    padding: 3px 10px;
    font-weight: 600;
    font-size: 11px;
}

.badge-hard {
    background-color: rgba(239, 68, 68, 0.15);
    color: #f87171;
    border: 1px solid rgba(239, 68, 68, 0.4);
    border-radius: 12px;
    padding: 3px 10px;
    font-weight: 600;
    font-size: 11px;
}

/* Scrollbars */
QScrollBar:vertical {
    background: #141519;
    width: 8px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #2f333e;
    min-height: 24px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background: #474d5d;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background: #141519;
    height: 8px;
}

QScrollBar::handle:horizontal {
    background: #2f333e;
    min-width: 24px;
    border-radius: 4px;
}

/* Status Bar */
QStatusBar {
    background-color: #121316;
    color: #9ca3af;
    border-top: 1px solid #23252c;
    font-size: 11px;
}
"""
