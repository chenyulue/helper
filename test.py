from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QKeyEvent, QDropEvent, QTextCursor, QTextCharFormat, QClipboard,QMimeData
from PyQt5.QtCore import pyqtSignal, Qt

class CustomTextEdit(QTextEdit):
    contentChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._previous_content = self.toPlainText()

    def keyPressEvent(self, event: QKeyEvent):
        super().keyPressEvent(event)
        current_content = self.toPlainText()
        if current_content != self._previous_content:
            self._previous_content = current_content
            self.contentChanged.emit()

    def insertFromMimeData(self, source: QMimeData):
        super().insertFromMimeData(source)
        current_content = self.toPlainText()
        if current_content != self._previous_content:
            self._previous_content = current_content
            self.contentChanged.emit()

    def paste(self):
        clipboard = QApplication.clipboard()
        mime_data = clipboard.mimeData()
        if mime_data.hasText():
            self.insertPlainText(mime_data.text())
            current_content = self.toPlainText()
            if current_content != self._previous_content:
                self._previous_content = current_content
                self.contentChanged.emit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QTextEdit Content Changed Signal Example")
        self.setGeometry(100, 100, 800, 600)

        # 创建自定义的 QTextEdit 实例
        self.text_edit = CustomTextEdit()

        # 连接自定义的 contentChanged 信号
        self.text_edit.contentChanged.connect(self.on_content_changed)

        # 标签用于显示信号触发情况
        self.content_changed_label = QLabel("contentChanged: Not triggered yet")

        # 按钮用于改变文本格式
        self.format_button = QPushButton("Change Text Format")
        self.format_button.clicked.connect(self.change_text_format)

        # 设置布局并将控件添加到主窗口
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.content_changed_label)
        layout.addWidget(self.format_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def on_content_changed(self):
        self.content_changed_label.setText("contentChanged: Triggered")

    def change_text_format(self):
        cursor = self.text_edit.textCursor()
        char_format = QTextCharFormat()
        char_format.setForeground(Qt.red)  # 改变文本颜色为红色
        cursor.mergeCharFormat(char_format)
        self.text_edit.setTextCursor(cursor)

if __name__ == "__main__":
    import sys
    from PyQt5.QtCore import Qt

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())



