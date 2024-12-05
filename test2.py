from PyQt5.QtWidgets import QApplication, QTextBrowser, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QTextCursor, QColor
from PyQt5.QtCore import Qt, QEvent

class ClickableTextBrowser(QTextBrowser):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clickable_ranges = []

    def add_clickable_text(self, text, start_action, double_click_action, right_click_action):
        cursor = self.textCursor()
        cursor.insertText(text)
        range_start = cursor.position() - len(text)
        range_end = cursor.position()
        self.clickable_ranges.append((range_start, range_end, start_action, double_click_action, right_click_action))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            for start, end, action, _, _ in self.clickable_ranges:
                cursor = self.cursorForPosition(event.pos())
                position = cursor.position()
                if start <= position < end:
                    if action is not None:
                        action()
                    break
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            for start, end, _, action, _ in self.clickable_ranges:
                cursor = self.cursorForPosition(event.pos())
                position = cursor.position()
                if start <= position < end:
                    action()
                    break
        super().mouseDoubleClickEvent(event)

    def contextMenuEvent(self, event):
        for start, end, _, _, action in self.clickable_ranges:
            cursor = self.cursorForPosition(event.pos())
            position = cursor.position()
            if start <= position < end:
                action()
                return
        super().contextMenuEvent(event)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.browser = ClickableTextBrowser()
        self.browser.add_clickable_text("Click me once", self.on_single_click, None, None)
        self.browser.add_clickable_text("\nDouble click me", None, self.on_double_click, None)
        self.browser.add_clickable_text("\nRight click me", None, None, self.on_right_click)

        layout.addWidget(self.browser)
        self.setLayout(layout)

    def on_single_click(self):
        self.browser.setTextColor(QColor("red"))
        self.browser.append("\nSingle clicked!")
        self.browser.setTextColor(QColor("black"))

    def on_double_click(self):
        self.browser.setTextColor(QColor("blue"))
        self.browser.append("\nDouble clicked!")
        self.browser.setTextColor(QColor("black"))

    def on_right_click(self):
        self.browser.setTextColor(QColor("green"))
        self.browser.append("\nRight clicked!")
        self.browser.setTextColor(QColor("black"))

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()



