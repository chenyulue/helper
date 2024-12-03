from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QTextBrowser, QApplication, QMessageBox, QWidget
from PyQt5.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat, QTextCursor

import bisect, re


class MyHighlighter(QSyntaxHighlighter):
    def __init__(self, keywords, parent):
        super().__init__(parent)
        self.keywords = keywords

    def highlightBlock(self, block):
        if not self.keywords:
            return
        charFormat = QTextCharFormat()
        charFormat.setFontWeight(QFont.Bold)
        charFormat.setForeground(Qt.darkMagenta)
        regex = re.compile('|'.join(self.keywords), re.IGNORECASE)
        result = regex.search(block, 0)
        while result:
            self.setFormat(result.start(),result.end()-result.start(), charFormat)
            result = regex.search(block, result.end())


class MyBrowser(QTextBrowser):
    text_clicked = pyqtSignal("QTextCursor")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMouseTracking(True)
        self.setTextInteractionFlags(Qt.NoTextInteraction)

        # self.phrases contains all phrases that should be clickable.
        self.phrases = set()
        self.cursors = []

        # ExtraSelection object for highlighting phrases under the mouse cursor
        self.selection = QTextBrowser.ExtraSelection()
        self.selection.format.setBackground(Qt.blue)
        self.selection.format.setForeground(Qt.white)
        self.selected_cursor = None

        # custom highlighter for highlighting all phrases
        self.highlighter = MyHighlighter(self.phrases, self)
        self.document().contentsChange.connect(self.text_has_changed)

    @property
    def selected_cursor(self):
        return None if self.selection.cursor == QTextCursor() else self.selection.cursor

    @selected_cursor.setter
    def selected_cursor(self, cursor):
        if cursor is None:
            cursor = QTextCursor()
        if self.selection.cursor != cursor:
            self.selection.cursor = cursor
            self.setExtraSelections([self.selection])

    def mouseMoveEvent(self, event):
        ''' Update currently selected cursor '''
        cursor = self.cursorForPosition(event.pos())
        self.selected_cursor = self.find_selected_cursor(cursor)

    def mouseReleaseEvent(self, event):
        ''' Emit self.selected_cursor signal when currently hovering over selectable phrase'''
        if self.selected_cursor:
            self.text_clicked.emit(self.selected_cursor)
            self.selected_cursor = None

    def add_phrase(self, phrase):
        ''' Add phrase to set of phrases and update list of text cursors'''
        if phrase not in self.phrases:
            self.phrases.add(phrase)
            self.find_cursors(phrase)
            self.highlighter.rehighlight()

    def find_cursors(self, phrase):
        ''' Find all occurrences of phrase in the current document and add corresponding text cursor
        to self.cursors '''
        if not phrase:
            return
        self.moveCursor(self.textCursor().Start)
        while self.find(phrase):
            cursor = self.textCursor()
            bisect.insort(self.cursors, cursor)
        self.moveCursor(self.textCursor().Start)

    def find_selected_cursor(self, cursor):
        ''' return text cursor corresponding to current mouse position or None if mouse not currently
        over selectable phrase'''
        position = cursor.position()
        index = bisect.bisect(self.cursors, cursor)
        if index < len(self.cursors) and self.cursors[index].anchor() <= position:
            return self.cursors[index]
        return None

    def text_has_changed(self):
        self.cursors.clear()
        self.selected_cursor = None
        for phrase in self.phrases:
            self.find_cursors(phrase)
            self.highlighter.rehighlight()


def text_message(widget):
    def inner(cursor):
        text = cursor.selectedText()
        pos = cursor.selectionStart()
        QMessageBox.information(widget, 'Information',
                f'You have clicked on the phrase <b>{text}</b><br>'
                f'which starts at position {pos} in the text')
    return inner


if __name__=="__main__":
    app = QApplication([])
    window = MyBrowser()
    window.resize(400,300)
    information = text_message(window)

    text = '''
    <h1>Title</h1>
    <p>This is a random text with. The following words are highlighted</p>
    <ul>
    <li>keyword1</li>
    <li>keyword2</li>
    </ul>
    <p>Click on either keyword1 or keyword2 to get more info. 
    '''

    window.add_phrase('keyword1')
    window.add_phrase('keyword2')
    window.setText(text)
    window.text_clicked.connect(information)
    window.show()
    app.exec()