from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QTextBrowser, QWidget
from PyQt5.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat, QTextCursor, QColor

import bisect
import re
from typing import Any


class CustomTextBrowser(QTextBrowser):
    # 定义信号，当点击记录位置的文本时发送
    textClicked = pyqtSignal(dict, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.clickable_text = {}  # 记录信号传递的数据
        self.text_positions = []  # 记录文本位置及相关数据
        self.setTextInteractionFlags(Qt.NoTextInteraction)

    def add_text(
        self,
        text: str,
        *,
        record_position: bool = False,
        data: dict[str, Any] | None = None,
        foreground: str | None = None,
        background: str | None = None,
        bold: bool = False,
        italic: bool = False,
        underline: bool = False,
        strikethrough: bool = False,
    ) -> tuple[int, int]:
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        start_pos = cursor.position()

        char_format = QTextCharFormat()
        char_format.setFontItalic(italic)
        char_format.setFontStrikeOut(strikethrough)
        if underline:
            char_format.setUnderlineStyle(QTextCharFormat.SingleUnderline)
        if bold:
            char_format.setFontWeight(QFont.Bold)
        if foreground is not None:
            char_format.setForeground(QColor(foreground))
        if background is not None:
            char_format.setBackground(QColor(background))

        cursor.insertText(text, char_format)

        end_pos = cursor.position()

        if record_position:
            self.add_clickable_position(start_pos, end_pos, data)

        return start_pos, end_pos

    def format_text(
        self,
        start_pos: int,
        end_pos: int,
        *,
        foreground: str | None = None,
        background: str | None = None,
        bold: bool = False,
        italic: bool = False,
        underline: bool = False,
        strikethrough: bool = False,
    ):
        cursor = self.textCursor()
        cursor.setPosition(start_pos)
        cursor.setPosition(end_pos, QTextCursor.KeepAnchor)

        extra_selection = QTextBrowser.ExtraSelection()
        extra_selection.cursor = cursor

        char_format = QTextCharFormat()
        char_format.setFontUnderline(underline)
        char_format.setFontItalic(italic)
        char_format.setFontStrikeOut(strikethrough)

        if bold:
            char_format.setFontWeight(QFont.Bold)

        if foreground is not None:
            char_format.setForeground(QColor(foreground))

        if background is not None:
            char_format.setBackground(QColor(background))
        else:
            char_format.setBackground(QColor("white"))

        extra_selection.format = char_format

        existing_selection = self.extraSelections()
        existing_selection.append(extra_selection)

        self.setExtraSelections(existing_selection)

    def add_clickable_position(
        self, start_pos: int, end_pos: int, data: dict[str, Any] | None = None
    ):
        bisect.insort(self.text_positions, start_pos)
        bisect.insort(self.text_positions, end_pos)
        self.clickable_text[(start_pos, end_pos)] = data

    def mousePressEvent(self, event):
        """
        重写鼠标按下事件，处理左键单击。
        """
        if event.button() == Qt.LeftButton:
            data = self.handle_click(event)
            if data:
                self.textClicked.emit(data, "<left>")
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            data = self.handle_click(event)
            if data:
                self.textClicked.emit(data, "<double-L>")
        super().mouseDoubleClickEvent(event)

    def contextMenuEvent(self, event):
        data = self.handle_click(event)
        if data:
            self.textClicked.emit(data, "<right>")
        super().contextMenuEvent(event)

    def handle_click(self, event) -> dict[str, Any] | None:
        cursor = self.cursorForPosition(event.pos())
        index = bisect.bisect(self.text_positions, cursor.position())
        if index - 1 < 0 or index >= len(self.text_positions):
            return None
        return self.clickable_text.get(
            (self.text_positions[index - 1], self.text_positions[index])
        )

    def clear(self):
        self.text_positions = []
        self.clickable_text = {}
        super().clear()


class MyHighlighter(QSyntaxHighlighter):
    def __init__(
        self,
        parent: QWidget,
        pattern: str|None = None,
        *,
        foreground: str | None = None,
        background: str | None = None,
        bold: bool = False,
        italic: bool = False,
        underline: bool = False,
        strikethrough: bool = False,
    ):
        super().__init__(parent)
        self._pattern = pattern
        self._foreground = foreground
        self._background = background
        self._bold = bold
        self._italic = italic
        self._underline = underline
        self._strikethrough = strikethrough

    def highlightBlock(self, block):
        if self._pattern is None:
            return
        char_format = QTextCharFormat()
        char_format.setFontUnderline(self._underline)
        char_format.setFontItalic(self._italic)
        char_format.setFontStrikeOut(self._strikethrough)

        if self._bold:
            char_format.setFontWeight(QFont.Bold)

        if self._foreground is not None:
            char_format.setForeground(QColor(self._foreground))

        if self._background is not None:
            char_format.setBackground(QColor(self._background))

        regex = re.compile(self._pattern, re.IGNORECASE|re.MULTILINE)
        result = regex.search(block, 0)
        while result:
            self.setFormat(result.start(), result.end() - result.start(), char_format)
            result = regex.search(block, result.end())


# class ClickableTextBrowser(QTextBrowser):
#     text_clicked = pyqtSignal("QTextCursor")

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.setMouseTracking(True)
#         # self.setTextInteractionFlags(Qt.NoTextInteraction)

#         # self.phrases contains all phrases that should be clickable.
#         self.phrases = set()
#         self.cursors = []

#         # ExtraSelection object for highlighting phrases under the mouse cursor
#         self.selection = QTextBrowser.ExtraSelection()
#         self.selection.format.setBackground(Qt.blue)
#         self.selection.format.setForeground(Qt.white)
#         self.selected_cursor = None

#         # custom highlighter for highlighting all phrases
#         self.highlighter = MyHighlighter(self.phrases, self)
#         self.document().contentsChange.connect(self.text_has_changed)

#     @property
#     def selected_cursor(self):
#         return None if self.selection.cursor == QTextCursor() else self.selection.cursor

#     @selected_cursor.setter
#     def selected_cursor(self, cursor):
#         if cursor is None:
#             cursor = QTextCursor()
#         if self.selection.cursor != cursor:
#             self.selection.cursor = cursor
#             self.setExtraSelections([self.selection])

#     def mouseMoveEvent(self, event):
#         """Update currently selected cursor"""
#         cursor = self.cursorForPosition(event.pos())
#         self.selected_cursor = self.find_selected_cursor(cursor)

#     def mouseReleaseEvent(self, event):
#         """Emit self.selected_cursor signal when currently hovering over selectable phrase"""
#         if self.selected_cursor:
#             self.text_clicked.emit(self.selected_cursor)
#             self.selected_cursor = None

#     def add_phrase(self, phrase):
#         """Add phrase to set of phrases and update list of text cursors"""
#         if phrase not in self.phrases:
#             self.phrases.add(phrase)
#             self.find_cursors(phrase)
#             self.highlighter.rehighlight()

#     def find_cursors(self, phrase):
#         """Find all occurrences of phrase in the current document and add corresponding text cursor
#         to self.cursors"""
#         if not phrase:
#             return
#         self.moveCursor(self.textCursor().Start)
#         while self.find(phrase):
#             cursor = self.textCursor()
#             bisect.insort(self.cursors, cursor)
#         self.moveCursor(self.textCursor().Start)

#     def find_selected_cursor(self, cursor):
#         """return text cursor corresponding to current mouse position or None if mouse not currently
#         over selectable phrase"""
#         position = cursor.position()
#         index = bisect.bisect(self.cursors, cursor)
#         if index < len(self.cursors) and self.cursors[index].anchor() <= position:
#             return self.cursors[index]
#         return None

#     def text_has_changed(self):
#         self.cursors.clear()
#         self.selected_cursor = None
#         for phrase in self.phrases:
#             self.find_cursors(phrase)
#             self.highlighter.rehighlight()
