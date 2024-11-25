from PyQt5.QtWidgets import (
    QApplication
)
import qdarktheme

from helper.App import App

def main() -> None:
    qdarktheme.enable_hi_dpi()
    app = App([])
    qdarktheme.setup_theme("light")
    app.exec_()

if __name__ == "__main__":
    main()