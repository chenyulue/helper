from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QMainWindow,
    QWidget,
)
# from PyQt5.uic import loadUi

from . import resources_rc
from .Ui_MainWindow import Ui_mainWindow
from .Ui_CmpWidget import Ui_cmpWidget
from .Ui_AboutDialog import Ui_aboutDialog

# from ..assets import ASSETS
# UI_PATH = ASSETS.parent / "UI"

class Window(QMainWindow, Ui_mainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # loadUi(UI_PATH / "mainWindow.ui", self)
        self.setupUi(self)
        
        self.aboutDialog = AboutDialog(self)
        self.cmpWidget = CmpWidget()

        self._connectSignalsAndSlots()

    def _connectSignalsAndSlots(self):
        self.aboutAction.triggered.connect(self._showAboutDialog)
        self.cmpAction.triggered.connect(self._showCmpWidget)

    def _showAboutDialog(self):
        self.aboutDialog.exec_()

    def _showCmpWidget(self):
        self.cmpWidget.show()

class CmpWidget(QWidget, Ui_cmpWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # loadUi(UI_PATH / "cmpWidget.ui", self)
        self.setupUi(self)

class AboutDialog(QDialog, Ui_aboutDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # loadUi(UI_PATH / "aboutDialog.ui", self)
        self.setupUi(self)
    