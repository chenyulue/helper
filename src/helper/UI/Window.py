from collections.abc import Iterator

from PyQt5.QtWidgets import (
    QDialog,
    QMainWindow,
    QWidget,
    QTextEdit,
    QTextBrowser,
)
from PyQt5.QtGui import (
    QTextCursor,
    QTextCharFormat,
    QColor,
)
# from PyQt5.uic import loadUi

from ..models import OpCode

from . import resources_rc  # noqa: F401
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

    def get_texts(self) -> tuple[str, str]:
        return self.aText.toPlainText(), self.bText.toPlainText()

    def format_text(self, opcodes: Iterator[tuple[OpCode, int, int, int, int]]) -> None:
        for tag, i1, i2, j1, j2 in opcodes:
            if tag == "delete":
                self._format_delete_text((i1, i2), (j1, j2))
            elif tag == "replace":
                self._format_replace_text((i1, i2), (j1, j2))
            elif tag == "insert":
                self._format_insert_text((i1, i2), (j1, j2))

    def clear_format(self) -> None:
        text_a = self.aText.toPlainText()
        text_b = self.bText.toPlainText()
        self.aText.clear()
        self.bText.clear()
        self.aText.setPlainText(text_a)
        self.bText.setPlainText(text_b)

    def _format_delete_text(
        self, index_a: tuple[int, int], index_b: tuple[int, int]
    ) -> None:
        self._apply_format(
            self.aText,
            index_a[0],
            index_a[1],
            color="red",
        )

    def _format_replace_text(
        self, index_a: tuple[int, int], index_b: tuple[int, int]
    ) -> None:
        self._apply_format(
            self.aText,
            index_a[0],
            index_a[1],
            color="red",
        )
        self._apply_format(
            self.bText,
            index_b[0],
            index_b[1],
            color="blue",
        )

    def _format_insert_text(
        self, index_a: tuple[int, int], index_b: tuple[int, int]
    ) -> None:
        self._apply_format(
            self.bText,
            index_b[0],
            index_b[1],
            color="blue",
        )

    def _apply_format(
        self,
        text_widget: QTextEdit | QTextBrowser,
        start_pos: int,
        end_pos: int,
        *,
        color: str = "",
        underline: bool = False,
        strikethrough: bool = False,
    ) -> None:
        if isinstance(text_widget, QTextBrowser):
            document = text_widget.document()
            cursor = QTextCursor(document)
        else:
            cursor = text_widget.textCursor()

        cursor.setPosition(start_pos)
        cursor.setPosition(end_pos, QTextCursor.KeepAnchor)

        char_format = QTextCharFormat()

        if color:
            char_format.setForeground(QColor(color))
        if underline:
            char_format.setUnderlineStyle(QTextCharFormat.SingleUnderline)
        if strikethrough:
            char_format.setFontStrikeOut(True)

        cursor.mergeCharFormat(char_format)


class AboutDialog(QDialog, Ui_aboutDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # loadUi(UI_PATH / "aboutDialog.ui", self)
        self.setupUi(self)
