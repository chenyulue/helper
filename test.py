from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTextEdit, QTextBrowser
from PyQt5.uic import loadUi
from pathlib import Path

# 假设你有一个名为 Ui_mainWindow 的 UI 类
class Ui_mainWindow:
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)

        # 示例 QTextEdit 和 QTextBrowser
        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(10, 10, 780, 290)
        self.textEdit.setObjectName("textEdit")

        self.textBrowser = QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(10, 310, 780, 280)
        self.textBrowser.setObjectName("textBrowser")

class Window(QMainWindow, Ui_mainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # 假设有其他对话框和小部件
        # self.aboutDialog = AboutDialog(self)
        # self.searchDialog = SearchDialog(self)
        # self.refDialog = RefDialog(self)
        # self.cmpWidget = CmpWidget()

        self._add_widgets_for_toolbar()
        self._init_format()

    def _add_widgets_for_toolbar(self):
        # 添加工具栏小部件的逻辑
        pass

    def _init_format(self):
        self.setStyleSheet("""
            QTextEdit {
                font-size: 24px;
            }
            QTextBrowser {
                font-size: 14px;
            }
        """)

if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    app.exec_()



