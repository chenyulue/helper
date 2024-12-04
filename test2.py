from PyQt5.QtWidgets import QTextBrowser, QApplication
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import Qt, pyqtSignal


class CustomTextBrowser(QTextBrowser):
    # 定义信号，当点击记录位置的文本时发送
    textClicked = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.text_positions = []  # 记录文本位置及相关数据

    def add_text(self, text, record_position=False, data=None):
        """
        添加文本到 QTextBrowser 中。
        :param text: 要添加的文本
        :param record_position: 是否记录文本位置
        :param data: 记录的附加数据
        """
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        start_pos = cursor.position()

        cursor.insertText(text)
        end_pos = cursor.position()

        if record_position:
            # 保存文本起止位置及附加数据
            self.text_positions.append((start_pos, end_pos, data))

    def mousePressEvent(self, event):
        """
        重写鼠标按下事件，处理左键单击。
        """
        if event.button() == Qt.LeftButton:
            self.handle_click(event)
        super().mousePressEvent(event)

    def handle_click(self, event):
        """
        处理左键单击事件，发送信号。
        """
        cursor = self.cursorForPosition(event.pos())
        pos = cursor.position()

        for start, end, data in self.text_positions:
            if start <= pos <= end:
                # 找到点击的记录位置，发送信号并附加数据
                if data is not None:
                    self.textClicked.emit(data)
                else:
                    self.textClicked.emit(f"位置范围: ({start}, {end})")
                break


# 示例运行
if __name__ == "__main__":
    import sys

    def on_text_clicked(data):
        print(f"点击的文本数据: {data}")

    app = QApplication(sys.argv)
    browser = CustomTextBrowser()
    browser.resize(600, 400)
    browser.show()

    # 添加普通文本
    browser.add_text("这是一段普通文本。\n", record_position=False)

    # 添加可交互文本，附带数据
    browser.add_text("这是可交互的文本1。\n", record_position=True, data="数据1")
    browser.add_text("这是可交互的文本2。\n", record_position=True, data="数据2")

    # 连接信号到槽
    browser.textClicked.connect(on_text_clicked)

    sys.exit(app.exec_())
