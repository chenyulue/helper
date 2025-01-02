from PyQt5.QtWidgets import QApplication

from helper.UI import MainWindow

def test_main_window():
    app = QApplication([])
    window = MainWindow()
    window.resultText.add_text("我是中国人\n", foreground="red")
    window.resultText.add_text("你是美国人", underline=True)
    window.show()
    app.exec_()