#!/usr/bin/env python3
"""
==============================================================================
DSA Note-Taking Desktop App
==============================================================================
A 100% offline, local desktop application for software engineers to track, 
review, and master Data Structures and Algorithms interview questions.

Core Technical Specs:
- GUI Framework: PyQt6 (with automatic fallback to PySide6)
- Persistence: Embedded SQLite (dsa_notes.db)
- Local Assets: Safe image copying to ./dsa_assets/ with unique identifiers
- Code Highlighting: Custom QSyntaxHighlighter for code blocks
- Design: Clean modern dark mode theme with ergonomic developer layout
==============================================================================
"""

import os
import sys
from typing import Optional

# Graceful import handling for PyQt6 or PySide6
try:
    from PyQt6.QtCore import Qt, QSize, QTimer
    from PyQt6.QtGui import (
        QFont, QPixmap, QIcon, QAction, QKeySequence, QGuiApplication,
        QShortcut, QPainter, QBrush, QColor
    )
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QLabel, QLineEdit, QTextEdit, QPushButton, QComboBox, QRadioButton,
        QButtonGroup, QSplitter, QListWidget, QListWidgetItem, QStackedWidget,
        QFileDialog, QMessageBox, QFrame, QScrollArea, QSizePolicy
    )
    QT_FRAMEWORK = "PyQt6"
except ImportError:
    try:
        from PySide6.QtCore import Qt, QSize, QTimer
        from PySide6.QtGui import (
            QFont, QPixmap, QIcon, QAction, QKeySequence, QGuiApplication,
            QShortcut, QPainter, QBrush, QColor
        )
        from PySide6.QtWidgets import (
            QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
            QLabel, QLineEdit, QTextEdit, QPushButton, QComboBox, QRadioButton,
            QButtonGroup, QSplitter, QListWidget, QListWidgetItem, QStackedWidget,
            QFileDialog, QMessageBox, QFrame, QScrollArea, QSizePolicy
        )
        QT_FRAMEWORK = "PySide6"
    except ImportError:
        print("ERROR: Neither PyQt6 nor PySide6 is installed.")
        print("Please install PyQt6 with: pip install PyQt6")
        sys.exit(1)

from database import (
    init_db, seed_sample_data, add_question, update_question,
    delete_question, get_question, get_all_questions, get_all_topics,
    get_stats, save_local_asset, resolve_asset_path, DEFAULT_DB_PATH, DEFAULT_ASSETS_DIR
)
from highlighter import DSACodeHighlighter
from theme import DARK_STYLESHEET

STANDARD_TOPICS = [
    "Array", "String", "Hash Table", "Two Pointers", "Sliding Window",
    "Dynamic Programming", "Trees & BST", "Graphs", "Heap / Priority Queue",
    "Binary Search", "Linked List", "Stack & Queue", "Backtracking",
    "Greedy", "Bit Manipulation", "Trie", "Math & Geometry", "System Design"
]


class MainWindow(QMainWindow):
    """Main Application Window for DSA Note-Taking."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("DSA Notes")
        self.resize(1280, 840)
        self.setMinimumSize(980, 640)

        # Active state tracking
        self.current_editing_id: Optional[int] = None
        self.current_selected_id: Optional[int] = None
        self.active_difficulty_filter: str = "All"
        self.attached_image_source_path: Optional[str] = None
        self.existing_relative_image_path: Optional[str] = None
        self._current_detail_pixmap: Optional[QPixmap] = None
        self._previous_view_index: int = 0

        self.setWindowIcon(self._create_app_icon())
        self._setup_ui()
        self._setup_shortcuts()
        self._load_topics_into_combo()
        self.refresh_question_list()
        self.refresh_stats_badges()

    def _create_app_icon(self) -> QIcon:
        """Generates a crisp modern 64x64 pixmap icon for the application window and taskbar."""
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw rounded dark background badge
        painter.setBrush(QBrush(QColor("#18181b")))
        painter.setPen(QColor("#4f46e5"))
        painter.drawRoundedRect(2, 2, 60, 60, 14, 14)

        # Draw lightning symbol
        font = QFont("Segoe UI" if sys.platform == "win32" else ".AppleSystemUIFont", 24, QFont.Weight.Bold)
        painter.setFont(font)
        painter.setPen(QColor("#60a5fa"))
        painter.drawText(pixmap.rect(), int(Qt.AlignmentFlag.AlignCenter), "⚡")
        painter.end()

        return QIcon(pixmap)

    def _setup_shortcuts(self):
        """Binds cross-platform keyboard shortcuts (translates to Cmd on macOS, Ctrl on Windows)."""
        # Ctrl/Cmd+N -> New Question
        self.sc_new = QShortcut(QKeySequence.StandardKey.New, self)
        self.sc_new.activated.connect(self.open_add_form)

        # Ctrl/Cmd+F -> Focus Search
        self.sc_find = QShortcut(QKeySequence.StandardKey.Find, self)
        self.sc_find.activated.connect(self._focus_search)

        # Ctrl/Cmd+S -> Save in Form
        self.sc_save = QShortcut(QKeySequence.StandardKey.Save, self)
        self.sc_save.activated.connect(self._on_shortcut_save)

        # Ctrl/Cmd+1 -> All Questions Dashboard
        self.sc_view1 = QShortcut(QKeySequence("Ctrl+1"), self)
        self.sc_view1.activated.connect(lambda: self.switch_view(0))

        # Ctrl/Cmd+2 -> Categories & Topics
        self.sc_view2 = QShortcut(QKeySequence("Ctrl+2"), self)
        self.sc_view2.activated.connect(lambda: self.switch_view(2))

        # Escape -> Context-sensitive back or clear search
        self.sc_esc = QShortcut(QKeySequence(Qt.Key.Key_Escape), self)
        self.sc_esc.activated.connect(self._on_escape)

    def _focus_search(self):
        """Switches to dashboard and focuses search input."""
        self.switch_view(0)
        self.search_input.setFocus()
        self.search_input.selectAll()

    def _on_shortcut_save(self):
        """Triggers form save when in form view."""
        if self.stack.currentIndex() == 1:
            self._save_question_form()

    def _on_escape(self):
        """Context-sensitive Escape action."""
        if self.stack.currentIndex() == 1:
            self._cancel_form()
        elif self.stack.currentIndex() == 2:
            self.switch_view(0)
        else:
            if self.search_input.text():
                self.search_input.clear()

    def _cancel_form(self):
        """Cancels form editing and returns to previous view."""
        self.switch_view(self._previous_view_index)

    def _rescale_detail_image(self):
        """Smoothly adapts attached diagram preview to available detail panel width."""
        if hasattr(self, "_current_detail_pixmap") and self._current_detail_pixmap and not self._current_detail_pixmap.isNull():
            avail_w = max(240, self.detail_panel.width() - 80)
            scaled = self._current_detail_pixmap.scaled(
                avail_w, 420,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.detail_image_label.setPixmap(scaled)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._rescale_detail_image()

    def _setup_ui(self):
        """Constructs the master layout: Sidebar on the left, Stacked Central area on right."""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QHBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Left Sidebar Navigation
        self.sidebar = self._create_sidebar()
        main_layout.addWidget(self.sidebar)

        # 2. Main Stacked Views (Dashboard, Add/Edit Form, Topics Browser)
        self.stack = QStackedWidget()
        self.dashboard_view = self._create_dashboard_view()
        self.form_view = self._create_form_view()
        self.topics_view = self._create_topics_view()

        self.stack.addWidget(self.dashboard_view)  # index 0
        self.stack.addWidget(self.form_view)       # index 1
        self.stack.addWidget(self.topics_view)     # index 2

        main_layout.addWidget(self.stack, 1)

        # Status Bar (Hidden to remove extra technical details)
        self.statusBar().hide()

    # =========================================================================
    # SIDEBAR NAVIGATION COMPONENT
    # =========================================================================
    def _create_sidebar(self) -> QWidget:
        sidebar = QWidget()
        sidebar.setObjectName("sidebarWidget")
        sidebar.setFixedWidth(240)
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(16, 20, 16, 16)
        layout.setSpacing(12)

        # App Brand Header
        brand_layout = QHBoxLayout()
        brand_icon = QLabel("⚡")
        brand_icon.setStyleSheet("font-size: 20px;")
        brand_title = QLabel("DSA Notes")
        brand_title.setStyleSheet("font-size: 17px; font-weight: 800; color: #ffffff; letter-spacing: 0.5px;")
        brand_layout.addWidget(brand_icon)
        brand_layout.addWidget(brand_title)
        brand_layout.addStretch()
        layout.addLayout(brand_layout)
        layout.addSpacing(10)

        # Primary Navigation Buttons
        self.btn_nav_all = QPushButton("📂  All Questions")
        self.btn_nav_all.setProperty("class", "nav-btn active")
        self.btn_nav_all.clicked.connect(lambda: self.switch_view(0))
        layout.addWidget(self.btn_nav_all)

        self.btn_nav_topics = QPushButton("🏷️  Categories && Topics")
        self.btn_nav_topics.setProperty("class", "nav-btn")
        self.btn_nav_topics.clicked.connect(lambda: self.switch_view(2))
        layout.addWidget(self.btn_nav_topics)

        self.btn_nav_add = QPushButton("➕  Add New Question")
        self.btn_nav_add.setProperty("class", "nav-btn")
        self.btn_nav_add.setStyleSheet("background-color: #27272a; color: #60a5fa; font-weight: 600;")
        self.btn_nav_add.clicked.connect(self.open_add_form)
        layout.addWidget(self.btn_nav_add)

        # Section Divider: Quick Difficulty Filters
        layout.addSpacing(10)
        filter_header = QLabel("DIFFICULTY FILTER")
        filter_header.setStyleSheet("color: #52525b; font-size: 11px; font-weight: 700; letter-spacing: 1px;")
        layout.addWidget(filter_header)

        self.diff_btn_group = QButtonGroup(self)
        self.btn_diff_all = QPushButton("All Difficulties")
        self.btn_diff_easy = QPushButton("🟢 Easy")
        self.btn_diff_medium = QPushButton("🟡 Medium")
        self.btn_diff_hard = QPushButton("🔴 Hard")

        for btn, diff in [
            (self.btn_diff_all, "All"),
            (self.btn_diff_easy, "Easy"),
            (self.btn_diff_medium, "Medium"),
            (self.btn_diff_hard, "Hard")
        ]:
            btn.setProperty("class", "filter-pill")
            btn.setCheckable(True)
            self.diff_btn_group.addButton(btn)
            btn.clicked.connect(lambda checked, d=diff: self.set_difficulty_filter(d))
            layout.addWidget(btn)

        self.btn_diff_all.setChecked(True)

        layout.addStretch()

        return sidebar

    # =========================================================================
    # VIEW 1: DASHBOARD / EXPLORER (SPLIT VIEW)
    # =========================================================================
    def _create_dashboard_view(self) -> QWidget:
        view = QWidget()
        layout = QVBoxLayout(view)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Top Bar: Search input & Topic filter dropdown
        top_bar = QHBoxLayout()
        top_bar.setSpacing(10)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍  Search questions by title, problem, tag, or notes... (Ctrl+F)")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.textChanged.connect(self.refresh_question_list)
        top_bar.addWidget(self.search_input, 3)

        self.topic_filter_combo = QComboBox()
        self.topic_filter_combo.addItem("All Topics")
        self.topic_filter_combo.currentTextChanged.connect(self.refresh_question_list)
        top_bar.addWidget(self.topic_filter_combo, 1)

        self.btn_new_quick = QPushButton("+ New")
        self.btn_new_quick.setProperty("class", "primary-btn")
        self.btn_new_quick.clicked.connect(self.open_add_form)
        top_bar.addWidget(self.btn_new_quick)

        layout.addLayout(top_bar)

        # Splitter: Left Question List & Right Read-Only Detail View Panel
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.setChildrenCollapsible(False)

        # Left: Questions List Card Column
        left_container = QWidget()
        left_container.setMinimumWidth(280)
        left_layout = QVBoxLayout(left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(6)

        self.question_count_label = QLabel("Questions (0)")
        self.question_count_label.setStyleSheet("color: #a1a1aa; font-size: 12px; font-weight: 600;")
        left_layout.addWidget(self.question_count_label)

        self.question_list_widget = QListWidget()
        self.question_list_widget.itemSelectionChanged.connect(self._on_question_selected)
        left_layout.addWidget(self.question_list_widget)

        self.splitter.addWidget(left_container)

        # Right: Read-Only Detail View Panel
        self.detail_panel = self._create_detail_panel()
        self.detail_panel.setMinimumWidth(420)
        self.splitter.addWidget(self.detail_panel)
        self.splitter.splitterMoved.connect(lambda pos, idx: self._rescale_detail_image())

        # Set splitter balance: 35% list, 65% reader
        self.splitter.setSizes([380, 720])
        layout.addWidget(self.splitter, 1)

        return view

    def _create_detail_panel(self) -> QWidget:
        """Constructs the Read-Only Details Panel for reviewing questions."""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: 1px solid #27272a; border-radius: 8px; background-color: #121316; }")

        panel = QWidget()
        self.detail_layout = QVBoxLayout(panel)
        self.detail_layout.setContentsMargins(24, 24, 24, 24)
        self.detail_layout.setSpacing(16)

        # Placeholder message when no question is selected
        self.empty_detail_label = QLabel("Select a question from the list to review details.")
        self.empty_detail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_detail_label.setStyleSheet("color: #71717a; font-size: 14px; padding: 40px;")
        self.detail_layout.addWidget(self.empty_detail_label)

        # Actual Detail Content Container (hidden by default until a question is clicked)
        self.detail_content_widget = QWidget()
        dc_layout = QVBoxLayout(self.detail_content_widget)
        dc_layout.setContentsMargins(0, 0, 0, 0)
        dc_layout.setSpacing(14)

        # Header Row: Title + Badges + Edit/Delete Buttons
        header_row = QHBoxLayout()
        self.detail_title = QLabel("Question Title")
        self.detail_title.setStyleSheet("font-size: 20px; font-weight: 800; color: #ffffff;")
        self.detail_title.setWordWrap(True)
        header_row.addWidget(self.detail_title, 1)

        self.detail_diff_badge = QLabel("Medium")
        self.detail_diff_badge.setProperty("class", "badge-medium")
        header_row.addWidget(self.detail_diff_badge)

        self.detail_topic_badge = QLabel("Array")
        self.detail_topic_badge.setStyleSheet("background-color: #27272a; color: #93c5fd; border-radius: 12px; padding: 4px 10px; font-size: 11px; font-weight: 600;")
        header_row.addWidget(self.detail_topic_badge)

        # Action Buttons
        self.btn_edit_current = QPushButton("✏️ Edit")
        self.btn_edit_current.setProperty("class", "secondary-btn")
        self.btn_edit_current.clicked.connect(self._edit_current_question)
        header_row.addWidget(self.btn_edit_current)

        self.btn_delete_current = QPushButton("🗑️ Delete")
        self.btn_delete_current.setProperty("class", "danger-btn")
        self.btn_delete_current.clicked.connect(self._delete_current_question)
        header_row.addWidget(self.btn_delete_current)

        dc_layout.addLayout(header_row)

        # Problem Statement
        dc_layout.addWidget(self._make_section_title("Problem Statement"))
        self.detail_problem = QLabel()
        self.detail_problem.setWordWrap(True)
        self.detail_problem.setStyleSheet("background-color: #18181b; border: 1px solid #27272a; border-radius: 6px; padding: 12px; font-size: 13px; line-height: 1.6; color: #e4e4e7;")
        dc_layout.addWidget(self.detail_problem)

        # Examples Section
        dc_layout.addWidget(self._make_section_title("Examples & Test Cases"))
        self.detail_examples = QLabel()
        self.detail_examples.setWordWrap(True)
        self.detail_examples.setStyleSheet("background-color: #18181b; border: 1px solid #27272a; border-radius: 6px; padding: 12px; font-family: monospace; font-size: 12px; color: #a1a1aa;")
        dc_layout.addWidget(self.detail_examples)

        # Personal Notes / Approach
        dc_layout.addWidget(self._make_section_title("Personal Notes & Approach"))
        self.detail_notes = QLabel()
        self.detail_notes.setWordWrap(True)
        self.detail_notes.setStyleSheet("background-color: #18181b; border: 1px solid #27272a; border-radius: 6px; padding: 12px; font-size: 13px; color: #e4e4e7;")
        dc_layout.addWidget(self.detail_notes)

        # Local Image Attachment Section
        self.image_container = QWidget()
        img_layout = QVBoxLayout(self.image_container)
        img_layout.setContentsMargins(0, 0, 0, 0)
        img_layout.setSpacing(6)
        img_layout.addWidget(self._make_section_title("Attached Diagram / Screenshot"))

        self.detail_image_label = QLabel()
        self.detail_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.detail_image_label.setStyleSheet("background-color: #18181b; border: 1px solid #27272a; border-radius: 6px; padding: 8px;")
        img_layout.addWidget(self.detail_image_label)

        self.detail_image_path_label = QLabel()
        self.detail_image_path_label.setStyleSheet("color: #71717a; font-size: 11px;")
        img_layout.addWidget(self.detail_image_path_label)

        dc_layout.addWidget(self.image_container)

        # Code Block Section with Copy Code Button
        code_header = QHBoxLayout()
        code_header.addWidget(self._make_section_title("Solution Code"))
        code_header.addStretch()

        self.btn_copy_code = QPushButton("📋 Copy Code")
        self.btn_copy_code.setProperty("class", "secondary-btn")
        self.btn_copy_code.clicked.connect(self._copy_code_to_clipboard)
        code_header.addWidget(self.btn_copy_code)
        dc_layout.addLayout(code_header)

        self.detail_code_viewer = QTextEdit()
        self.detail_code_viewer.setObjectName("readOnlyCodeViewer")
        self.detail_code_viewer.setReadOnly(True)
        self.detail_code_viewer.setMinimumHeight(180)
        # Apply syntax highlighter to the reader
        self.reader_highlighter = DSACodeHighlighter(self.detail_code_viewer.document())
        dc_layout.addWidget(self.detail_code_viewer)

        self.detail_layout.addWidget(self.detail_content_widget)
        self.detail_content_widget.setVisible(False)

        scroll_area.setWidget(panel)
        return scroll_area

    def _make_section_title(self, title: str) -> QLabel:
        lbl = QLabel(title)
        lbl.setStyleSheet("font-size: 12px; font-weight: 700; color: #a1a1aa; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px;")
        return lbl

    # =========================================================================
    # VIEW 2: "ADD / EDIT QUESTION" FORM PANEL
    # =========================================================================
    def _create_form_view(self) -> QWidget:
        self.form_scroll_area = QScrollArea()
        self.form_scroll_area.setWidgetResizable(True)
        self.form_scroll_area.setStyleSheet("QScrollArea { border: none; background-color: #121316; }")

        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(32, 24, 32, 32)
        layout.setSpacing(16)

        # Form Title
        self.form_header_label = QLabel("Add New DSA Question")
        self.form_header_label.setObjectName("headingLabel")
        layout.addWidget(self.form_header_label)

        # Row 1: Title Input
        layout.addWidget(QLabel("Question Title *"))
        self.input_title = QLineEdit()
        self.input_title.setPlaceholderText("e.g. Merge k Sorted Lists, LRU Cache, Two Sum...")
        layout.addWidget(self.input_title)

        # Row 2: Topic & Difficulty side-by-side
        meta_row = QHBoxLayout()
        meta_row.setSpacing(16)

        # Topic
        topic_col = QVBoxLayout()
        topic_col.addWidget(QLabel("Topic / Tag *"))
        self.input_topic = QComboBox()
        self.input_topic.setEditable(True)
        self.input_topic.addItems(STANDARD_TOPICS)
        topic_col.addWidget(self.input_topic)
        meta_row.addLayout(topic_col, 2)

        # Difficulty Level (Radio Buttons)
        diff_col = QVBoxLayout()
        diff_col.addWidget(QLabel("Difficulty *"))
        diff_radio_layout = QHBoxLayout()
        self.diff_form_group = QButtonGroup(self)

        self.radio_easy = QRadioButton("Easy")
        self.radio_medium = QRadioButton("Medium")
        self.radio_hard = QRadioButton("Hard")
        self.radio_medium.setChecked(True)

        for rb in (self.radio_easy, self.radio_medium, self.radio_hard):
            self.diff_form_group.addButton(rb)
            diff_radio_layout.addWidget(rb)

        diff_col.addLayout(diff_radio_layout)
        meta_row.addLayout(diff_col, 2)
        layout.addLayout(meta_row)

        # Row 3: Problem Statement
        layout.addWidget(QLabel("Problem Statement"))
        self.input_problem = QTextEdit()
        self.input_problem.setPlaceholderText("Paste or describe the problem requirements, constraints, and inputs/outputs...")
        self.input_problem.setMinimumHeight(100)
        layout.addWidget(self.input_problem)

        # Row 4: Examples
        layout.addWidget(QLabel("Examples & Test Cases"))
        self.input_examples = QTextEdit()
        self.input_examples.setPlaceholderText("Input: nums = [2,7,11,15], target = 9\nOutput: [0,1]")
        self.input_examples.setMinimumHeight(80)
        layout.addWidget(self.input_examples)

        # Row 5: Personal Notes / Approach
        layout.addWidget(QLabel("Personal Notes, Approach & Complexity"))
        self.input_notes = QTextEdit()
        self.input_notes.setPlaceholderText("Key insights, edge cases to remember, O(N) time complexity and space trade-offs...")
        self.input_notes.setMinimumHeight(90)
        layout.addWidget(self.input_notes)

        # Row 6: Code Block Area
        layout.addWidget(QLabel("Code Solution (Monospace + Syntax Highlighting)"))
        self.input_code = QTextEdit()
        self.input_code.setObjectName("codeEditor")
        self.input_code.setPlaceholderText("class Solution:\n    def solve(self, ...):")
        self.input_code.setMinimumHeight(160)
        # Apply QSyntaxHighlighter
        self.code_highlighter = DSACodeHighlighter(self.input_code.document())
        layout.addWidget(self.input_code)

        # Row 7: Picture / Image Attachment
        layout.addWidget(QLabel("Picture / Diagram Attachment"))
        img_picker_box = QFrame()
        img_picker_box.setStyleSheet("background-color: #18181b; border: 1px dashed #3f3f46; border-radius: 8px; padding: 12px;")
        img_picker_layout = QVBoxLayout(img_picker_box)

        btn_browse_row = QHBoxLayout()
        self.btn_browse_img = QPushButton("📁 Browse Image...")
        self.btn_browse_img.setProperty("class", "secondary-btn")
        self.btn_browse_img.clicked.connect(self._browse_image_file)
        btn_browse_row.addWidget(self.btn_browse_img)

        self.btn_remove_img = QPushButton("❌ Remove Image")
        self.btn_remove_img.setProperty("class", "danger-btn")
        self.btn_remove_img.clicked.connect(self._clear_attached_image)
        self.btn_remove_img.setVisible(False)
        btn_browse_row.addWidget(self.btn_remove_img)

        self.form_image_path_label = QLabel("No image attached (optional).")
        self.form_image_path_label.setStyleSheet("color: #71717a; font-size: 12px;")
        btn_browse_row.addWidget(self.form_image_path_label, 1)

        img_picker_layout.addLayout(btn_browse_row)

        # Preview thumbnail inside form
        self.form_image_preview = QLabel()
        self.form_image_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.form_image_preview.setVisible(False)
        img_picker_layout.addWidget(self.form_image_preview)

        layout.addWidget(img_picker_box)

        # Bottom Action Bar
        action_row = QHBoxLayout()
        action_row.addStretch()

        self.btn_cancel_form = QPushButton("Cancel (Esc)")
        self.btn_cancel_form.setProperty("class", "secondary-btn")
        self.btn_cancel_form.clicked.connect(self._cancel_form)
        action_row.addWidget(self.btn_cancel_form)

        self.btn_save_form = QPushButton("💾 Save Question (Ctrl+S)")
        self.btn_save_form.setProperty("class", "primary-btn")
        self.btn_save_form.clicked.connect(self._save_question_form)
        action_row.addWidget(self.btn_save_form)

        layout.addLayout(action_row)

        self.form_scroll_area.setWidget(panel)
        return self.form_scroll_area

    # =========================================================================
    # VIEW 3: CATEGORIES & TOPICS BROWSER
    # =========================================================================
    def _create_topics_view(self) -> QWidget:
        view = QWidget()
        layout = QVBoxLayout(view)
        layout.setContentsMargins(32, 28, 32, 32)
        layout.setSpacing(16)

        title = QLabel("Categories & Topics")
        title.setObjectName("headingLabel")
        layout.addWidget(title)

        desc = QLabel("Explore your question collection grouped by data structure and algorithmic pattern.")
        desc.setStyleSheet("color: #71717a; font-size: 13px; margin-bottom: 8px;")
        layout.addWidget(desc)

        self.topics_list_widget = QListWidget()
        self.topics_list_widget.itemClicked.connect(self._on_topic_card_clicked)
        layout.addWidget(self.topics_list_widget, 1)

        return view

    # =========================================================================
    # BUSINESS LOGIC & SLOTS
    # =========================================================================
    def switch_view(self, index: int):
        """Switches the active stacked widget view and updates sidebar button styles."""
        if self.stack.currentIndex() != index:
            self._previous_view_index = self.stack.currentIndex()
        self.stack.setCurrentIndex(index)
        self.btn_nav_all.setChecked(index == 0)
        self.btn_nav_topics.setChecked(index == 2)
        self.btn_nav_add.setChecked(index == 1)

        if index == 0:
            self.refresh_question_list()
        elif index == 2:
            self.refresh_topics_view()

    def set_difficulty_filter(self, difficulty: str):
        self.active_difficulty_filter = difficulty
        self.switch_view(0)
        self.refresh_question_list()

    def _load_topics_into_combo(self):
        """Populates topic dropdowns with predefined topics plus existing DB topics."""
        db_topics = [t[0] for t in get_all_topics()]
        combined = sorted(list(set(STANDARD_TOPICS + db_topics)))

        self.topic_filter_combo.blockSignals(True)
        self.topic_filter_combo.clear()
        self.topic_filter_combo.addItem("All Topics")
        for t in combined:
            self.topic_filter_combo.addItem(t)
        self.topic_filter_combo.blockSignals(False)

    def refresh_question_list(self):
        """Fetches questions matching active query, topic, and difficulty filters."""
        search_query = self.search_input.text()
        topic_filter = self.topic_filter_combo.currentText()
        if topic_filter == "All Topics":
            topic_filter = None

        difficulty = self.active_difficulty_filter if self.active_difficulty_filter != "All" else None

        questions = get_all_questions(
            search_query=search_query,
            topic=topic_filter,
            difficulty=difficulty
        )

        self.question_count_label.setText(f"Questions ({len(questions)})")
        self.question_list_widget.clear()

        for q in questions:
            diff = q["difficulty"]
            diff_icon = "🟢" if diff == "Easy" else ("🟡" if diff == "Medium" else "🔴")

            item_widget = QWidget()
            item_layout = QVBoxLayout(item_widget)
            item_layout.setContentsMargins(12, 10, 12, 10)
            item_layout.setSpacing(4)

            # Top row: Title + Difficulty
            top_row = QHBoxLayout()
            title_lbl = QLabel(q["title"])
            title_lbl.setStyleSheet("font-size: 14px; font-weight: 700; color: #f4f4f5;")
            top_row.addWidget(title_lbl, 1)

            diff_lbl = QLabel(f"{diff_icon} {diff}")
            diff_lbl.setStyleSheet(f"font-size: 11px; font-weight: 600; color: {'#4ade80' if diff == 'Easy' else ('#fbbf24' if diff == 'Medium' else '#f87171')};")
            top_row.addWidget(diff_lbl)
            item_layout.addLayout(top_row)

            # Bottom row: Topic tag + snippet
            bottom_row = QHBoxLayout()
            tag_lbl = QLabel(q["topic"])
            tag_lbl.setStyleSheet("color: #93c5fd; font-size: 11px; background-color: #1e293b; padding: 2px 6px; border-radius: 4px;")
            bottom_row.addWidget(tag_lbl)

            if q["image_path"]:
                img_indicator = QLabel("📷 Image")
                img_indicator.setStyleSheet("color: #a1a1aa; font-size: 10px;")
                bottom_row.addWidget(img_indicator)

            bottom_row.addStretch()
            item_layout.addLayout(bottom_row)

            # Add to QListWidget
            list_item = QListWidgetItem()
            # Set explicit size hint so layout does not clip and displays perfectly on all resolutions
            list_item.setSizeHint(QSize(0, 72))
            list_item.setData(Qt.ItemDataRole.UserRole, q["id"])

            self.question_list_widget.addItem(list_item)
            self.question_list_widget.setItemWidget(list_item, item_widget)

        # Select first item if available
        if self.question_list_widget.count() > 0:
            self.question_list_widget.setCurrentRow(0)
        else:
            self._current_detail_pixmap = None
            self.detail_content_widget.setVisible(False)
            if search_query.strip():
                self.empty_detail_label.setText(f"No questions match '{search_query}'.\nPress Esc or click the clear button to reset search.")
            else:
                self.empty_detail_label.setText("No questions found in this filter.\nClick '+ New' to create one.")
            self.empty_detail_label.setVisible(True)

    def _on_question_selected(self):
        """Triggered when an item in the left list is selected."""
        selected_items = self.question_list_widget.selectedItems()
        if not selected_items:
            self._current_detail_pixmap = None
            self.detail_content_widget.setVisible(False)
            self.empty_detail_label.setVisible(True)
            return

        q_id = selected_items[0].data(Qt.ItemDataRole.UserRole)
        self.current_selected_id = q_id
        q = get_question(q_id)
        if not q:
            return

        self.empty_detail_label.setVisible(False)
        self.detail_content_widget.setVisible(True)

        # Populate Details
        self.detail_title.setText(q["title"])
        self.detail_topic_badge.setText(q["topic"])

        diff = q["difficulty"]
        self.detail_diff_badge.setText(diff)
        if diff == "Easy":
            self.detail_diff_badge.setStyleSheet("background-color: rgba(34, 197, 94, 0.2); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.4); border-radius: 12px; padding: 4px 10px; font-weight: 700; font-size: 11px;")
        elif diff == "Medium":
            self.detail_diff_badge.setStyleSheet("background-color: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); border-radius: 12px; padding: 4px 10px; font-weight: 700; font-size: 11px;")
        else:
            self.detail_diff_badge.setStyleSheet("background-color: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); border-radius: 12px; padding: 4px 10px; font-weight: 700; font-size: 11px;")

        self.detail_problem.setText(q["problem_statement"] or "No problem description provided.")
        self.detail_examples.setText(q["examples"] or "No examples provided.")
        self.detail_notes.setText(q["notes"] or "No notes provided.")
        self.detail_code_viewer.setPlainText(q["code"] or "")

        # Local image rendering
        img_path = resolve_asset_path(q["image_path"])
        if img_path and os.path.exists(img_path):
            self.image_container.setVisible(True)
            self._current_detail_pixmap = QPixmap(img_path)
            self.detail_image_path_label.setText(f"File: {os.path.basename(img_path)}")
            self._rescale_detail_image()
        else:
            self._current_detail_pixmap = None
            self.image_container.setVisible(False)

    def _copy_code_to_clipboard(self):
        """Copies the solution code to clipboard with user feedback."""
        code_text = self.detail_code_viewer.toPlainText()
        if not code_text.strip():
            self.statusBar().showMessage("No code to copy.", 2000)
            return

        clipboard = QGuiApplication.clipboard()
        clipboard.setText(code_text)

        orig_text = self.btn_copy_code.text()
        self.btn_copy_code.setText("✅ Copied!")
        self.statusBar().showMessage("Code copied to clipboard!", 2500)
        QTimer.singleShot(1800, lambda: self.btn_copy_code.setText(orig_text))

    def open_add_form(self):
        """Clears form fields and opens Add Question view."""
        self.current_editing_id = None
        self.form_header_label.setText("Add New DSA Question")
        self.input_title.clear()
        self.input_topic.setCurrentIndex(0)
        self.radio_medium.setChecked(True)
        self.input_problem.clear()
        self.input_examples.clear()
        self.input_notes.clear()
        self.input_code.clear()
        self._clear_attached_image()
        self.switch_view(1)
        if hasattr(self, "form_scroll_area"):
            self.form_scroll_area.verticalScrollBar().setValue(0)
        self.input_title.setFocus()

    def _edit_current_question(self):
        """Loads selected question into the form for editing."""
        if not self.current_selected_id:
            return

        q = get_question(self.current_selected_id)
        if not q:
            return

        self.current_editing_id = q["id"]
        self.form_header_label.setText(f"Edit Question: {q['title']}")
        self.input_title.setText(q["title"])

        # Set topic
        idx = self.input_topic.findText(q["topic"])
        if idx >= 0:
            self.input_topic.setCurrentIndex(idx)
        else:
            self.input_topic.setEditText(q["topic"])

        # Set difficulty
        diff = q["difficulty"]
        if diff == "Easy":
            self.radio_easy.setChecked(True)
        elif diff == "Medium":
            self.radio_medium.setChecked(True)
        else:
            self.radio_hard.setChecked(True)

        self.input_problem.setPlainText(q["problem_statement"] or "")
        self.input_examples.setPlainText(q["examples"] or "")
        self.input_notes.setPlainText(q["notes"] or "")
        self.input_code.setPlainText(q["code"] or "")

        # Image
        self.attached_image_source_path = None
        self.existing_relative_image_path = q["image_path"]
        resolved_img = resolve_asset_path(q["image_path"])

        if resolved_img and os.path.exists(resolved_img):
            self.form_image_path_label.setText(f"Attached: {os.path.basename(resolved_img)}")
            self.btn_remove_img.setVisible(True)
            pix = QPixmap(resolved_img)
            if not pix.isNull():
                self.form_image_preview.setPixmap(pix.scaled(300, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
                self.form_image_preview.setVisible(True)
        else:
            self._clear_attached_image()

        self.switch_view(1)
        if hasattr(self, "form_scroll_area"):
            self.form_scroll_area.verticalScrollBar().setValue(0)
        self.input_title.setFocus()

    def _delete_current_question(self):
        """Deletes selected question after confirmation."""
        if not self.current_selected_id:
            return

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to permanently delete this DSA question and any attached local image?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            delete_question(self.current_selected_id)
            self.current_selected_id = None
            self.refresh_question_list()
            self.refresh_stats_badges()
            self._load_topics_into_combo()
            self.statusBar().showMessage("Question deleted successfully.", 3000)

    def _browse_image_file(self):
        """Opens file dialog for user to select an image from their local machine."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Diagram or Screenshot",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.webp)"
        )
        if file_path:
            self.attached_image_source_path = file_path
            self.form_image_path_label.setText(f"Selected: {os.path.basename(file_path)}")
            self.btn_remove_img.setVisible(True)

            pix = QPixmap(file_path)
            if not pix.isNull():
                self.form_image_preview.setPixmap(pix.scaled(320, 160, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
                self.form_image_preview.setVisible(True)

    def _clear_attached_image(self):
        """Clears image selection in form."""
        self.attached_image_source_path = None
        self.existing_relative_image_path = None
        self.form_image_path_label.setText("No image attached (optional).")
        self.btn_remove_img.setVisible(False)
        self.form_image_preview.clear()
        self.form_image_preview.setVisible(False)

    def _save_question_form(self):
        """Validates and persists the question into SQLite, copying any attached asset."""
        title = self.input_title.text().strip()
        if not title:
            QMessageBox.warning(self, "Validation Error", "Question title is required!")
            self.input_title.setFocus()
            return

        topic = self.input_topic.currentText().strip()
        if not topic:
            topic = "General"

        if self.radio_easy.isChecked():
            difficulty = "Easy"
        elif self.radio_hard.isChecked():
            difficulty = "Hard"
        else:
            difficulty = "Medium"

        problem = self.input_problem.toPlainText().strip()
        examples = self.input_examples.toPlainText().strip()
        notes = self.input_notes.toPlainText().strip()
        code = self.input_code.toPlainText()

        # Handle local asset copying
        final_image_path = self.existing_relative_image_path
        if self.attached_image_source_path:
            # Safely copy into ./dsa_assets/ and generate unique filename
            saved_path = save_local_asset(self.attached_image_source_path)
            if saved_path:
                final_image_path = saved_path

        if self.current_editing_id:
            # Update existing
            update_question(
                question_id=self.current_editing_id,
                title=title,
                difficulty=difficulty,
                topic=topic,
                problem_statement=problem,
                examples=examples,
                notes=notes,
                code=code,
                image_path=final_image_path
            )
            saved_id = self.current_editing_id
            self.statusBar().showMessage(f"Updated '{title}' successfully.", 3000)
        else:
            # Insert new
            saved_id = add_question(
                title=title,
                difficulty=difficulty,
                topic=topic,
                problem_statement=problem,
                examples=examples,
                notes=notes,
                code=code,
                image_path=final_image_path
            )
            self.statusBar().showMessage(f"Saved new question '{title}' into SQLite.", 3000)

        self._load_topics_into_combo()
        self.refresh_stats_badges()
        self.switch_view(0)

        # Select the newly saved or updated item
        for i in range(self.question_list_widget.count()):
            item = self.question_list_widget.item(i)
            if item.data(Qt.ItemDataRole.UserRole) == saved_id:
                self.question_list_widget.setCurrentItem(item)
                break

    def refresh_topics_view(self):
        """Refreshes the categories & topics list widget."""
        self.topics_list_widget.clear()
        topics = get_all_topics()

        for topic_name, count in topics:
            item_widget = QWidget()
            item_layout = QHBoxLayout(item_widget)
            item_layout.setContentsMargins(16, 12, 16, 12)

            name_lbl = QLabel(f"📁  {topic_name}")
            name_lbl.setStyleSheet("font-size: 14px; font-weight: 700; color: #ffffff;")
            item_layout.addWidget(name_lbl, 1)

            count_pill = QLabel(f"{count} {'question' if count == 1 else 'questions'}")
            count_pill.setStyleSheet("background-color: #27272a; color: #a5b4fc; padding: 4px 10px; border-radius: 4px; font-size: 11px; font-weight: 600; border: 1px solid #3f3f46;")
            item_layout.addWidget(count_pill)

            list_item = QListWidgetItem()
            list_item.setSizeHint(QSize(0, 56))
            list_item.setData(Qt.ItemDataRole.UserRole, topic_name)

            self.topics_list_widget.addItem(list_item)
            self.topics_list_widget.setItemWidget(list_item, item_widget)

    def _on_topic_card_clicked(self, item: QListWidgetItem):
        """Clicking a topic navigates to the Questions Explorer filtered by that topic."""
        topic_name = item.data(Qt.ItemDataRole.UserRole)
        idx = self.topic_filter_combo.findText(topic_name)
        if idx >= 0:
            self.topic_filter_combo.setCurrentIndex(idx)
        self.switch_view(0)

    def refresh_stats_badges(self):
        """Updates sidebar difficulty filter buttons with live counts from SQLite."""
        stats = get_stats()
        self.btn_diff_all.setText(f"All ({stats['total']})")
        self.btn_diff_easy.setText(f"🟢 Easy ({stats['easy']})")
        self.btn_diff_medium.setText(f"🟡 Medium ({stats['medium']})")
        self.btn_diff_hard.setText(f"🔴 Hard ({stats['hard']})")


def main():
    """Application entry point with High-DPI scaling and platform typography."""
    # 1. Initialize SQLite schema & pre-seed default samples if database is brand new
    init_db()
    seed_sample_data()

    # 2. Configure High-DPI support prior to QApplication instantiation
    if hasattr(Qt.ApplicationAttribute, "AA_EnableHighDpiScaling"):
        try:
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
        except Exception:
            pass
    if hasattr(Qt.ApplicationAttribute, "AA_UseHighDpiPixmaps"):
        try:
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
        except Exception:
            pass

    # 3. Launch GUI Application
    app = QApplication(sys.argv)
    app.setApplicationName("DSANoteTaker")
    app.setOrganizationName("DSANoteTaker")
    app.setApplicationDisplayName("DSA Note Taker")

    # High-DPI rounding policy if supported
    if hasattr(QGuiApplication, "setHighDpiScaleFactorRoundingPolicy"):
        try:
            QGuiApplication.setHighDpiScaleFactorRoundingPolicy(
                Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
            )
        except Exception:
            pass

    # Platform-tailored typography
    app_font = app.font()
    if sys.platform == "darwin":
        app_font.setFamilies([".AppleSystemUIFont", "SF Pro Text", "Helvetica Neue", "Helvetica", "sans-serif"])
        app_font.setPointSize(12)
    elif sys.platform == "win32":
        app_font.setFamilies(["Segoe UI", "Arial", "sans-serif"])
        app_font.setPointSize(10)
    else:
        app_font.setFamilies(["Ubuntu", "DejaVu Sans", "sans-serif"])
        app_font.setPointSize(10)
    app.setFont(app_font)

    app.setStyle("Fusion")
    app.setStyleSheet(DARK_STYLESHEET)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
