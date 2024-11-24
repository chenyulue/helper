from PyQt5.QtWidgets import (
    QApplication
)
import qdarktheme

from helper.UI import Window

def main() -> None:
    qdarktheme.enable_hi_dpi()
    app = QApplication([])
    qdarktheme.setup_theme("light")
    win = Window()
    win.show()
    app.exec_()

if __name__ == "__main__":
    main()