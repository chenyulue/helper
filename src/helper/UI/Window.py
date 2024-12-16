from collections.abc import Iterator
import re

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
    QMessageBox,
)
from PyQt5.QtGui import (
    QTextCursor,
    QTextCharFormat,
    QTextBlockFormat,
    QTextDocument,
    QColor,
    QFont,
)
from PyQt5.QtCore import Qt

from typing import Any
from ..models import OpCode, RefBasis, SMALL_DEFECTS, RefBasisConfirmed

from . import resources_rc  # noqa: F401
from .Ui_MainWindow import Ui_mainWindow
from .Ui_CmpWidget import Ui_cmpWidget
from .Ui_AboutDialog import Ui_aboutDialog
from .Ui_SearchDialog import Ui_searchDialog
from .Ui_RefDialog import Ui_refDialog

RED = "red"
BLUE = "blue"
PINK = "pink"
GREEN = "#95FA9B"
DEFAULT_FONT_SIZE = 12


class Window(QMainWindow, Ui_mainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # loadUi(UI_PATH / "mainWindow.ui", self)
        self.setupUi(self)

        self.resize(1000, 618)

        self.aboutDialog = AboutDialog(self)
        self.searchDialog = SearchDialog(self)
        self.refDialog = RefDialog(self)
        self.cmpWidget = CmpWidget()

        self._add_widgets_for_toolbar()

        self._connectSignalsAndSlots()

        self._apply_style_sheet()

    # --------------------- 显示引用缺陷检查结果 ------------------------
    def display_reference_basis(
        self, ref_basis: dict[int, dict[int, RefBasis]], confirmed: RefBasisConfirmed
    ):
        n = 0
        for claim_number, bases in ref_basis.items():
            for position, basis in bases.items():
                if position in confirmed.lack_basis:
                    start_pos, end_pos = self._format_ref_basis(
                        n + 1, claim_number, basis, confirmed
                    )
                    self.resultText.format_text(start_pos, end_pos, background=PINK)
                    n += 1
                elif (
                    position in confirmed.has_basis and self.showAllCheckBox.isChecked()
                ):
                    start_pos, end_pos = self._format_ref_basis(
                        n + 1, claim_number, basis, confirmed
                    )
                    self.resultText.format_text(start_pos, end_pos, background=GREEN)
                    n += 1
                elif (
                    basis.hasbasis_checked is False
                    and position not in confirmed.has_basis
                ):
                    start_pos, end_pos = self._format_ref_basis(
                        n + 1, claim_number, basis, confirmed
                    )
                    self.resultText.format_text(start_pos, end_pos, background=None)
                    n += 1
                elif (
                    isinstance(basis.hasbasis_checked, list)
                    and position not in confirmed.has_basis
                ):
                    start_pos, end_pos = self._format_ref_basis(
                        n + 1, claim_number, basis, confirmed
                    )
                    self.resultText.format_text(start_pos, end_pos, background=None)
                    n += 1

    def _format_ref_basis(
        self,
        number: int,
        claim_number: int,
        basis: RefBasis,
        confirmed: RefBasisConfirmed,
    ) -> tuple[int, int]:
        if basis.term in basis.context:
            pre, post = basis.context.split(basis.term)
        else:
            pre, post = basis.context.split(basis.term[0])
            post = ""

        start_pos, _ = self.resultText.add_text(
            f"{number}、权利要求{claim_number}中“{pre}"
        )
        self.resultText.add_text(basis.term, foreground=RED, underline=True)

        if basis.position in confirmed.has_basis:
            expr = "没有"
        elif basis.hasbasis_checked is False:
            expr = "存在"
        elif isinstance(basis.hasbasis_checked, list):
            expr = f"在引用路径不包括{', '.join(str(i) for i in basis.hasbasis_checked)}时存在"

        _, end_pos = self.resultText.add_text(
            f"{post}”{expr}缺乏引用基础的表述 ({basis.position})\n"
        )

        data = {
            "type": "reference basis",
            "data": basis,
            "position": (start_pos, end_pos),
            "claim_num": claim_number,
        }
        self.resultText.add_clickable_position(start_pos, end_pos, data)

        return start_pos, end_pos

    # -------------------- 显示多引多缺陷检查结果 --------------------------------
    def display_multiple_dependencies(self, multi_deps: dict[int, list[int]]) -> None:
        n = 0
        start_pos, end_pos = self.resultText.add_text(
            "☛ 多引多缺陷\n", bold=True, underline=True
        )
        self.resultText.format_text(start_pos, end_pos, background="white")

        for claim_num, deps in multi_deps.items():
            start_pos, end_pos = self._format_multiple_deps(n + 1, claim_num, deps)
            self.resultText.format_text(start_pos, end_pos, background="white")
            n += 1

    def _format_multiple_deps(
        self, number: int, claim_num: int, deps: list[int]
    ) -> tuple[int, int]:
        deps_str = ", ".join(str(i) for i in deps)

        start_pos, _ = self.resultText.add_text(
            f"{number}、权利要求{claim_num}引用权项"
        )
        self.resultText.add_text(f"{deps_str}", bold=True)
        _, end_pos = self.resultText.add_text("时存在多引多的缺陷\n")

        data = {
            "type": "multiple dependencies",
            "data": [claim_num, deps],
            "position": (start_pos, end_pos),
        }
        self.resultText.add_clickable_position(start_pos, end_pos, data)

        return start_pos, end_pos

    # ======================= 显示其他小缺陷检查结果 =============================
    def display_small_defects(self, defects: dict[SMALL_DEFECTS, list[Any]]) -> None:
        if defects:
            start_pos, end_pos = self.resultText.add_text(
                "☛ 其他小缺陷\n", bold=True, underline=True
            )
            self.resultText.format_text(start_pos, end_pos, background="white")

        n = 0
        if defects.get("non_alternative_reference"):
            self._format_non_alternative_reference(
                n + 1, defects["non_alternative_reference"]
            )
            n += 1
        if defects.get("no_title_domain"):
            self._format_no_title_domain(n + 1, defects["no_title_domain"])
            n += 1
        if defects.get("claim_phrases_unintegrity"):
            self._format_claim_phrases_unintegrity(
                n + 1, defects["claim_phrases_unintegrity"]
            )
            n += 1

    def _format_non_alternative_reference(self, number: int, claim_numbers: list[int]):
        self.resultText.add_text(f"{number}、存在非择一引用缺陷的权利要求：")

        for i, claim_num in enumerate(claim_numbers):
            if i == len(claim_numbers) - 1:
                text = f"[{claim_num}]"
            else:
                text = f"[{claim_num}]、"
            data = {"type": "small defects", "data": claim_num}
            self.resultText.add_text(text, bold=True, record_position=True, data=data)
        self.resultText.add_text("\n")

    def _format_no_title_domain(self, number: int, claim_numbers: list[int]):
        self.resultText.add_text(f"{number}、技术主题没有体现出技术领域的权利要求：")

        for i, claim_num in enumerate(claim_numbers):
            if i == len(claim_numbers) - 1:
                text = f"[{claim_num}]"
            else:
                text = f"[{claim_num}]、"
            data = {"type": "small defects", "data": claim_num}
            self.resultText.add_text(text, bold=True, record_position=True, data=data)
        self.resultText.add_text("\n")

    def _format_claim_phrases_unintegrity(
        self, number: int, claim_numbers: list[tuple[int, str]]
    ):
        self.resultText.add_text(f"{number}、“权利要求”这一措辞表述不完整的权利要求：")

        for i, claim_num in enumerate(claim_numbers):
            if i == len(claim_numbers) - 1:
                text = f"[{claim_num[0]}中为“{claim_num[1]}”]"
            else:
                text = f"[{claim_num[0]}中为“{claim_num[1]}”]、"
            data = {"type": "small defects", "data": claim_num[0]}
            self.resultText.add_text(text, bold=True, record_position=True, data=data)
        self.resultText.add_text("\n")

    # ------------------------- 添加工具栏小控件 ------------------------------------
    def _add_widgets_for_toolbar(self) -> None:
        self.segmentCheckBox = QCheckBox("分词模式", parent=self.widgetToolBar)
        self.segmentCheckBox.setEnabled(False) # 分词模式暂时没有实现，取消勾选功能
        
        label = QLabel("最短截词长度:", parent=self.widgetToolBar)
        self.lengthSpinBox = QSpinBox(parent=self.widgetToolBar)
        self.checkButton = QPushButton("检查", parent=self.widgetToolBar)
        self.clearButton = QPushButton("清空", parent=self.widgetToolBar)

        self.checkButton.setStyleSheet("font-weight: bold;")
        self.clearButton.setStyleSheet("font-weight: bold;")

        self.lengthSpinBox.setRange(1, 20)
        self.lengthSpinBox.setValue(2)
        self.lengthSpinBox.lineEdit().setReadOnly(True)  # type: ignore

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
        self.widgetToolBar.addWidget(self.clearButton)

    # ------------------------- 一些槽函数 --------------------------------
    def _connectSignalsAndSlots(self):
        self.aboutAction.triggered.connect(self._showAboutDialog)
        self.cmpAction.triggered.connect(self._showCmpWidget)
        self.searchAction.triggered.connect(self._showSearchDialog)

        self.copyAction.triggered.connect(self._copy_text)
        self.cutAction.triggered.connect(self._cut_text)
        self.pasteAction.triggered.connect(self._paste_text)

        self.clearButton.clicked.connect(self._clear_text)

    def _clear_text(self):
        for textWidget in [
            self.claimText,
            self.descriptionText,
            self.figureText,
            self.abstractText,
            self.resultText,
        ]:
            textWidget.clear()

    def _showAboutDialog(self) -> None:
        self.aboutDialog.exec_()

    def _showCmpWidget(self) -> None:
        self.cmpWidget.show()

    def _showSearchDialog(self) -> None:
        self.searchDialog.show()
        self.searchDialog.searchLineEdit.setFocus()

    def _showWarningDialog(self, message: str) -> None:
        warning_box = QMessageBox(parent=self)
        warning_box.setWindowTitle("警告")
        warning_box.setText(message)
        warning_box.setIcon(QMessageBox.Warning)
        warning_box.setStandardButtons(QMessageBox.Ok)
        warning_box.show()

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

    # ------------------------ 一些格式化函数 --------------------------
    def _apply_style_sheet(self):
        self.setStyleSheet(f"""
            QTextEdit {{
                font-size: {DEFAULT_FONT_SIZE}pt;
            }}
            QTextBrowser {{
                font-size: {DEFAULT_FONT_SIZE}pt;
            }}
        """)

    def set_line_spacing(
        self, widget: QTextEdit | QTextBrowser, line_spacing: int | float
    ) -> None:
        cursor = widget.textCursor()  # 获取光标
        cursor.select(QTextCursor.Document)  # 选择整个文档

        # 设置段落格式
        block_format = QTextBlockFormat()
        block_format.setLineHeight(
            line_spacing * 100, QTextBlockFormat.ProportionalHeight
        )

        # 应用到文档
        cursor.mergeBlockFormat(block_format)
        cursor.clearSelection()

        widget.setTextCursor(cursor)  # 重置光标

    def clear_widget_formatting(self, widget: QTextEdit):
        widget.setExtraSelections([])

        text = widget.toPlainText()

        new_doc = QTextDocument()

        font = QFont()
        font.setPointSize(DEFAULT_FONT_SIZE)
        new_doc.setDefaultFont(font)

        new_doc.setPlainText(text)

        widget.setDocument(new_doc)

        widget.moveCursor(QTextCursor.Start)

    def format_widget_text(
        self,
        widget: QTextEdit,
        start_pos: int,
        end_pos: int,
        *,
        foreground: str | None = None,
        background: str | None = None,
        bold: bool = False,
        italic: bool = False,
        underline: bool = False,
        strikethrough: bool = False,
    ):
        cursor = widget.textCursor()
        cursor.setPosition(start_pos)
        cursor.setPosition(end_pos, QTextCursor.KeepAnchor)

        char_format = QTextCharFormat()
        char_format.setFontUnderline(underline)
        char_format.setFontItalic(italic)
        char_format.setFontStrikeOut(strikethrough)

        if bold:
            font = QFont()
            font.setBold(True)
            font.setPointSize(14)
            char_format.setFont(font)

        if foreground is not None:
            char_format.setForeground(QColor(foreground))

        if background is not None:
            char_format.setBackground(QColor(background))

        if foreground or background or italic or underline or strikethrough:
            extra_selection = QTextBrowser.ExtraSelection()
            extra_selection.cursor = cursor
            extra_selection.format = char_format

            existing_selection = widget.extraSelections()
            existing_selection.append(extra_selection)

            widget.setExtraSelections(existing_selection)

        if bold:
            cursor.mergeCharFormat(char_format)

    def format_widget_with_pattern(
        self, widget: QTextEdit | QTextBrowser, pattern: str, *args, **kwargs
    ):
        regex = re.compile(pattern, re.IGNORECASE | re.MULTILINE)
        block = widget.toPlainText()

        result = regex.search(block, 0)
        while result:
            self.format_widget_text(
                widget, result.start(), result.end(), *args, **kwargs
            )
            result = regex.search(block, result.end())

    def view_cursor_at_position(self, widget: QTextEdit, position: int):
        cursor = QTextCursor(widget.document())
        cursor.setPosition(position)
        widget.setTextCursor(cursor)


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
            self._add_formatted_text(
                self.resultText, a[index_a[0] : index_a[1]], bold=False
            )

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

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)  # type: ignore


class SearchDialog(QDialog, Ui_searchDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)  # type: ignore


class RefDialog(QDialog, Ui_refDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)  # type: ignore
