from collections.abc import Iterator

from PyQt5.QtWidgets import (
    QDialog,
    QMainWindow,
    QWidget,
    QTextEdit,
    QTextBrowser,
    QCheckBox,
    QLabel,
    QSpinBox,
    QPushButton,
    QSizePolicy,
)
from PyQt5.QtGui import (
    QTextCursor,
    QTextCharFormat,
    QTextDocument,
    QColor,
    QFont,
)
from PyQt5.QtCore import Qt
# from PyQt5.uic import loadUi

from ..models import OpCode, RefBasis

from . import resources_rc  # noqa: F401
from .Ui_MainWindow import Ui_mainWindow
from .Ui_CmpWidget import Ui_cmpWidget
from .Ui_AboutDialog import Ui_aboutDialog
from .Ui_SearchDialog import Ui_searchDialog

# from ..assets import ASSETS
# UI_PATH = ASSETS.parent / "UI"

RED = "red"
BLUE = "blue"


class Window(QMainWindow, Ui_mainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # loadUi(UI_PATH / "mainWindow.ui", self)
        self.setupUi(self)

        self.aboutDialog = AboutDialog(self)
        self.searchDialog = SearchDialog(self)
        self.cmpWidget = CmpWidget()

        self._add_widgets_for_toolbar()

        self._connectSignalsAndSlots()

    def display_reference_basis(self, ref_basis: dict[int, dict[int, RefBasis]]):
        # TODO:
        self.resultText.clear()
        
        for claim_number, bases in ref_basis.items():
            for position, basis in bases.items():
                if basis.hasbasis_confirmed is False:
                    self.resultText.append(f"{claim_number}-{basis.position} {basis.term} confirmed")
                elif basis.hasbasis_confirmed is None and basis.hasbasis_checked is False:
                    self.resultText.append(f"{claim_number}-{basis.position} {basis.term} not confirmed")

    def _add_widgets_for_toolbar(self) -> None:
        self.segmentCheckBox = QCheckBox("分词模式", parent=self.widgetToolBar)
        label = QLabel("最短截词长度:", parent=self.widgetToolBar)
        self.lengthSpinBox = QSpinBox(parent=self.widgetToolBar)
        self.checkButton = QPushButton("检查", parent=self.widgetToolBar)
        self.removeButton = QPushButton("清空", parent=self.widgetToolBar)

        self.checkButton.setStyleSheet("font-weight: bold;")
        self.removeButton.setStyleSheet("font-weight: bold;")

        self.lengthSpinBox.setRange(1, 20)
        self.lengthSpinBox.lineEdit().setReadOnly(True) # type: ignore

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.widgetToolBar.addWidget(spacer)
        
        self.widgetToolBar.addWidget(self.segmentCheckBox)

        self.widgetToolBar.addSeparator()
        
        self.widgetToolBar.addWidget(label)
        self.widgetToolBar.addWidget(self.lengthSpinBox)
        
        self.widgetToolBar.addSeparator()

        spacer1 = QWidget()
        spacer1.setFixedSize(10, 10)
        self.widgetToolBar.addWidget(self.checkButton)
        self.widgetToolBar.addWidget(spacer1)
        self.widgetToolBar.addWidget(self.removeButton)

    def _connectSignalsAndSlots(self):
        self.aboutAction.triggered.connect(self._showAboutDialog)
        self.cmpAction.triggered.connect(self._showCmpWidget)
        self.searchAction.triggered.connect(self._showSearchDialog)

        self.copyAction.triggered.connect(self._copy_text)
        self.cutAction.triggered.connect(self._cut_text)
        self.pasteAction.triggered.connect(self._paste_text)

    def _showAboutDialog(self) -> None:
        self.aboutDialog.exec_()

    def _showCmpWidget(self) -> None:
        self.cmpWidget.show()

    def _showSearchDialog(self) -> None:
        self.searchDialog.show()
        self.searchDialog.searchLineEdit.setFocus()

    def _copy_text(self):
        if self.focusWidget() in [
            self.claimText,
            self.descriptionText,
            self.figureText,
            self.abstractText,
        ]:
            self.focusWidget().copy()  # type: ignore

    def _cut_text(self):
        if self.focusWidget() in [
            self.claimText,
            self.descriptionText,
            self.figureText,
            self.abstractText,
        ]:
            self.focusWidget().cut()  # type: ignore

    def _paste_text(self):
        if self.focusWidget() in [
            self.claimText,
            self.descriptionText,
            self.figureText,
            self.abstractText,
        ]:
            self.focusWidget().paste()  # type: ignore


class CmpWidget(QWidget, Ui_cmpWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # loadUi(UI_PATH / "cmpWidget.ui", self)
        self.setupUi(self)

    def get_texts(self) -> tuple[str, str]:
        return self.aText.toPlainText(), self.bText.toPlainText()

    def format_text(self, opcodes: Iterator[tuple[OpCode, int, int, int, int]]) -> None:
        text_a = self.aText.toPlainText()
        text_b = self.bText.toPlainText()

        for tag, i1, i2, j1, j2 in opcodes:
            if tag == "delete":
                self._format_delete_text((i1, i2), (j1, j2), (text_a, text_b))
            elif tag == "replace":
                self._format_replace_text((i1, i2), (j1, j2), (text_a, text_b))
            elif tag == "insert":
                self._format_insert_text((i1, i2), (j1, j2), (text_a, text_b))
            else:
                self._format_equal_text((i1, i2), (text_a, text_b))

    def clear_format(self) -> None:
        text_a = self.aText.toPlainText()
        text_b = self.bText.toPlainText()

        newdoc_a = QTextDocument()
        newdoc_b = QTextDocument()
        newdoc_a.setPlainText(text_a)
        newdoc_b.setPlainText(text_b)

        self.aText.setDocument(newdoc_a)
        self.bText.setDocument(newdoc_b)

        self.resultText.clear()

    def _format_delete_text(
        self,
        index_a: tuple[int, int],
        index_b: tuple[int, int],
        texts: tuple[str, str] | None = None,
    ) -> None:
        self._apply_format(
            self.aText,
            index_a[0],
            index_a[1],
            color=RED,
        )
        if texts is not None:
            a, _ = texts
            self._add_formatted_text(
                self.resultText,
                a[index_a[0] : index_a[1]],
                color=RED,
                strikethrough=True,
            )

    def _format_replace_text(
        self,
        index_a: tuple[int, int],
        index_b: tuple[int, int],
        texts: tuple[str, str] | None = None,
    ) -> None:
        self._apply_format(
            self.aText,
            index_a[0],
            index_a[1],
            color=RED,
        )
        self._apply_format(
            self.bText,
            index_b[0],
            index_b[1],
            color=BLUE,
        )
        if texts is not None:
            a, b = texts
            self._add_formatted_text(
                self.resultText,
                a[index_a[0] : index_a[1]],
                color=RED,
                strikethrough=True,
            )
            self._add_formatted_text(
                self.resultText, b[index_b[0] : index_b[1]], color=BLUE, underline=True
            )

    def _format_insert_text(
        self,
        index_a: tuple[int, int],
        index_b: tuple[int, int],
        texts: tuple[str, str] | None = None,
    ) -> None:
        self._apply_format(
            self.bText,
            index_b[0],
            index_b[1],
            color=BLUE,
        )
        if texts is not None:
            _, b = texts
            self._add_formatted_text(
                self.resultText, b[index_b[0] : index_b[1]], color=BLUE, underline=True
            )

    def _format_equal_text(
        self, index_a: tuple[int, int], texts: tuple[str, str] | None = None
    ):
        if texts is not None:
            a, _ = texts
            self._add_formatted_text(self.resultText, a[index_a[0] : index_a[1]], bold=False)

    def _apply_format(
        self,
        text_widget: QTextEdit,
        start_pos: int,
        end_pos: int,
        *,
        color: str = "",
        underline: bool = False,
        strikethrough: bool = False,
    ) -> None:
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

    def _add_formatted_text(
        self,
        browser: QTextBrowser,
        text: str,
        *,
        color: str = "",
        underline: bool = False,
        strikethrough: bool = False,
        bold: bool = True,
    ) -> None:
        cursor = self.resultText.textCursor()
        format = QTextCharFormat()

        if color:
            format.setForeground(QColor(color))
        if underline:
            format.setUnderlineStyle(QTextCharFormat.SingleUnderline)
        if strikethrough:
            format.setFontStrikeOut(True)
        if bold:
            format.setFontWeight(QFont.Bold)

        cursor.insertText(text, format)


class AboutDialog(QDialog, Ui_aboutDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        # loadUi(UI_PATH / "aboutDialog.ui", self)
        self.setupUi(self)

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint) # type: ignore


class SearchDialog(QDialog, Ui_searchDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint) # type: ignore
