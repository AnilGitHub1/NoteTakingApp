"""
Code Syntax Highlighter for PyQt6 / PySide6.
Provides syntax coloring for Python, C++, Java, and general code snippets
inside the code editor and viewer areas.
"""

import re

try:
    from PyQt6.QtCore import QRegularExpression
    from PyQt6.QtGui import QColor, QFont, QSyntaxHighlighter, QTextCharFormat
except ImportError:
    from PySide6.QtCore import QRegularExpression
    from PySide6.QtGui import QColor, QFont, QSyntaxHighlighter, QTextCharFormat


class DSACodeHighlighter(QSyntaxHighlighter):
    """
    Sleek Dark-Theme Code Syntax Highlighter supporting keywords, types,
    strings, numbers, comments, and function definitions.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []

        # Color Palette tuned for high contrast dark theme
        keyword_color = QColor("#c678dd")    # Purple
        type_color = QColor("#e5c07b")       # Golden yellow
        builtin_color = QColor("#61afef")    # Cyan / Blue
        string_color = QColor("#98c379")     # Green
        comment_color = QColor("#5c6370")    # Muted Slate
        number_color = QColor("#d19a66")     # Orange
        function_color = QColor("#61afef")   # Sky blue
        decorator_color = QColor("#e06c75")  # Red / Coral

        # 1. Keywords
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(keyword_color)
        keyword_format.setFontWeight(QFont.Weight.Bold)
        keywords = [
            r"\bdef\b", r"\bclass\b", r"\breturn\b", r"\bif\b", r"\belse\b",
            r"\belif\b", r"\bfor\b", r"\bwhile\b", r"\bin\b", r"\bimport\b",
            r"\bfrom\b", r"\btry\b", r"\bexcept\b", r"\bfinally\b", r"\bwith\b",
            r"\bas\b", r"\bpass\b", r"\bbreak\b", r"\bcontinue\b", r"\byield\b",
            r"\blambda\b", r"\band\b", r"\bor\b", r"\bnot\b", r"\bis\b",
            r"\bassert\b", r"\bglobal\b", r"\bnonlocal\b", r"\bdel\b",
            # Common C++ / Java additions for multi-language DSA
            r"\bpublic\b", r"\bprivate\b", r"\bprotected\b", r"\bstatic\b",
            r"\bvoid\b", r"\bconst\b", r"\bauto\b", r"\bnew\b", r"\bdelete\b",
            r"\btemplate\b", r"\btypename\b", r"\bstruct\b"
        ]
        for pattern in keywords:
            rule = (QRegularExpression(pattern), keyword_format)
            self.highlighting_rules.append(rule)

        # 2. Types & Constants
        type_format = QTextCharFormat()
        type_format.setForeground(type_color)
        types = [
            r"\bint\b", r"\bfloat\b", r"\bstr\b", r"\bbool\b", r"\blist\b",
            r"\bdict\b", r"\bset\b", r"\btuple\b", r"\bNone\b", r"\bTrue\b",
            r"\bFalse\b", r"\bself\b", r"\bvector\b", r"\bstring\b", r"\bListNode\b",
            r"\bTreeNode\b", r"\bNode\b", r"\bOptional\b", r"\bList\b", r"\bDict\b"
        ]
        for pattern in types:
            rule = (QRegularExpression(pattern), type_format)
            self.highlighting_rules.append(rule)

        # 3. Built-in functions
        builtin_format = QTextCharFormat()
        builtin_format.setForeground(builtin_color)
        builtins = [
            r"\blen\b", r"\brange\b", r"\benumerate\b", r"\bprint\b", r"\bmin\b",
            r"\bmax\b", r"\bsum\b", r"\bsorted\b", r"\bmap\b", r"\bfilter\b",
            r"\bzip\b", r"\babs\b", r"\ball\b", r"\bany\b", r"\bappend\b", r"\bpop\b"
        ]
        for pattern in builtins:
            rule = (QRegularExpression(pattern), builtin_format)
            self.highlighting_rules.append(rule)

        # 4. Function definitions
        function_format = QTextCharFormat()
        function_format.setForeground(function_color)
        function_format.setFontWeight(QFont.Weight.Bold)
        self.highlighting_rules.append((QRegularExpression(r"\b[A-Za-z0-9_]+(?=\()"), function_format))

        # 5. Decorators
        decorator_format = QTextCharFormat()
        decorator_format.setForeground(decorator_color)
        self.highlighting_rules.append((QRegularExpression(r"@[A-Za-z0-9_]+"), decorator_format))

        # 6. Numbers
        number_format = QTextCharFormat()
        number_format.setForeground(number_color)
        self.highlighting_rules.append((QRegularExpression(r"\b\d+(\.\d+)?\b"), number_format))

        # 7. Strings (Double and single quotes)
        self.string_format = QTextCharFormat()
        self.string_format.setForeground(string_color)
        self.highlighting_rules.append((QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"'), self.string_format))
        self.highlighting_rules.append((QRegularExpression(r"'[^'\\]*(\\.[^'\\]*)*'"), self.string_format))

        # 8. Single-line comments (# in Python, // in C++/Java)
        comment_format = QTextCharFormat()
        comment_format.setForeground(comment_color)
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression(r"#[^\n]*"), comment_format))
        self.highlighting_rules.append((QRegularExpression(r"//[^\n]*"), comment_format))

        # Multi-line strings / docstrings pattern
        self.multi_line_comment_format = QTextCharFormat()
        self.multi_line_comment_format.setForeground(string_color)
        self.comment_start_expression = QRegularExpression(r'"""|\'\'\'')
        self.comment_end_expression = QRegularExpression(r'"""|\'\'\'')

    def highlightBlock(self, text: str) -> None:
        """Applies formatting rules to the specified text block."""
        for pattern, fmt in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)

        # Handle multi-line docstrings (""" or ''')
        self.setCurrentBlockState(0)
        start_index = 0
        if self.previousBlockState() != 1:
            match = self.comment_start_expression.match(text)
            start_index = match.capturedStart()
        else:
            start_index = 0

        while start_index >= 0:
            match = self.comment_end_expression.match(text, start_index)
            end_index = match.capturedStart()
            comment_length = 0
            if end_index == -1:
                self.setCurrentBlockState(1)
                comment_length = len(text) - start_index
            else:
                comment_length = end_index - start_index + match.capturedLength()

            self.setFormat(start_index, comment_length, self.string_format)
            match = self.comment_start_expression.match(text, start_index + comment_length)
            start_index = match.capturedStart()
