from PyQt5.QtWidgets import QApplication, QMainWindow, QTextBrowser, QVBoxLayout, QWidget
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QColor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.text_browser = QTextBrowser()
        layout = QVBoxLayout()
        container = QWidget()
        container.setLayout(layout)
        layout.addWidget(self.text_browser)
        self.setCentralWidget(container)

        # 示例文本
        self.text_browser.setText("这是一个示例文本，我们将对其进行格式化。\n"
                                 "这里是一些更多文本，用于演示不同的格式选项。""这是一个示例文本，我们将对其进行格式化。\n"
                                 "这里是一些更多文本，用于演示不同的格式选项。")

        # 应用格式化
        self.apply_format(10, 20, 'color', QColor('red'))
        self.apply_format(10, 20, 'underline')
        self.apply_format(30, 40, 'underline')
        self.apply_format(50, 60, 'strikethrough')

    def apply_format(self, start_pos, end_pos, format_type, color=None):
        document = self.text_browser.document()
        cursor = QTextCursor(document)
        cursor.setPosition(start_pos)
        cursor.setPosition(end_pos, QTextCursor.KeepAnchor)

        char_format = QTextCharFormat()

        if format_type == 'color':
            if color:
                char_format.setForeground(color)
        elif format_type == 'underline':
            char_format.setUnderlineStyle(QTextCharFormat.SingleUnderline)
        elif format_type == 'strikethrough':
            char_format.setFontStrikeOut(True)

        cursor.mergeCharFormat(char_format)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()






