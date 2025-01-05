from typing import cast, Callable

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
    QMenu,
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

from . import resources_rc  # noqa: F401
from .Ui_MainWindow import Ui_mainWindow

from . import AboutDialog, SearchDialog, RefDialog, CmpWidget

from ..Config import TextFormatterConfig
from ..core.Types import RefBasis, CheckType


class MainWindow(QMainWindow, Ui_mainWindow):
    def __init__(
        self, parent: QWidget | None = None, config: TextFormatterConfig | None = None
    ):
        super().__init__(parent)
        self.setupUi(self)

        self.config = config or TextFormatterConfig()

        self.aboutDialog = AboutDialog(self)
        self.searchDialog = SearchDialog(self)
        self.refDialog = RefDialog(self)
        self.cmpWidget = CmpWidget()

        self.display_funcs: dict[str, Callable] = {}

        self.resize(1200, 742)

        self._add_widgets_for_toolbar()

        self._apply_default_style()

        self._connect_signals_and_slots()

    # ========================= 缺乏引用基础缺陷展示 ===================================
    def display_reference_basis(
        self,
        ref_basis: dict[int, dict[int, RefBasis]],
        has_basis: set[int],
        lack_basis: set[int],
        all_ref_paths: list[list[int]],
    ):
        self.resultText.add_text("👉【 权利要求缺陷 】 ", bold=True)
        self.resultText.add_text(
            "(查看引用关系)\n",
            foreground="blue",
            underline=True,
            record_position=True,
            bold=True,
            data={"type": CheckType.CheckReferencePaths, "data": all_ref_paths},
        )

        n = 0
        for claim_number, bases in ref_basis.items():
            for position, basis in bases.items():
                if position in lack_basis:
                    start_pos, end_pos = self._format_ref_basis(
                        n + 1, claim_number, basis, has_basis
                    )
                    self.resultText.add_extra_format(
                        start_pos, end_pos, background=self.config.failure
                    )
                    n += 1
                elif position in has_basis and self.showAllCheckBox.isChecked():
                    start_pos, end_pos = self._format_ref_basis(
                        n + 1, claim_number, basis, has_basis
                    )
                    self.resultText.add_extra_format(
                        start_pos, end_pos, background=self.config.success
                    )
                    n += 1
                elif basis.hasbasis_checked is False and position not in has_basis:
                    start_pos, end_pos = self._format_ref_basis(
                        n + 1, claim_number, basis, has_basis
                    )
                    self.resultText.add_extra_format(
                        start_pos, end_pos, background=None
                    )
                    n += 1
                elif (
                    isinstance(basis.hasbasis_checked, list)
                    and position not in has_basis
                ):
                    start_pos, end_pos = self._format_ref_basis(
                        n + 1, claim_number, basis, has_basis
                    )
                    self.resultText.add_extra_format(
                        start_pos, end_pos, background=None
                    )
                    n += 1

    def _format_ref_basis(
        self,
        number: int,
        claim_number: int,
        basis: RefBasis,
        has_basis: set[int],
    ) -> tuple[int, int]:
        if basis.term in basis.context:
            pre, post = basis.context.split(basis.term)
        else:
            pre, post = basis.context.split(basis.term[0])
            post = ""

        start_pos, _ = self.resultText.add_text(
            f"{number}、权利要求{claim_number}中“{pre}"
        )
        self.resultText.add_text(
            basis.term, foreground=self.config.danger, underline=True
        )

        if basis.position in has_basis:
            expr = "没有"
        elif basis.hasbasis_checked is False:
            expr = "存在"
        elif isinstance(basis.hasbasis_checked, list):
            expr = f"在引用路径不包括{', '.join(str(i) for i in basis.hasbasis_checked)}时存在"

        _, end_pos = self.resultText.add_text(
            f"{post}”{expr}缺乏引用基础的表述 ({basis.position})\n"
        )

        data = {
            "type": CheckType.LackOfReferenceBasis,
            "data": basis,
            "position": (start_pos, end_pos),
            "claim_num": claim_number,
        }
        self.resultText.add_clickable_position(start_pos, end_pos, data)

        return start_pos, end_pos

    def _connect_signals_and_slots(self):
        self.aboutAction.triggered.connect(self._showAboutDialog)
        self.cmpAction.triggered.connect(self._showCmpWidget)
        self.searchAction.triggered.connect(self._showSearchDialog)

        self.undoAction.triggered.connect(self._undo)
        self.redoAction.triggered.connect(self._redo)

        self.copyAction.triggered.connect(self._copy_text)
        self.cutAction.triggered.connect(self._cut_text)
        self.pasteAction.triggered.connect(self._paste_text)
        # self.pastePlainTextAction.triggered.connect(self._paste_plain_text)

        self.selectAllAction.triggered.connect(self._select_all_text)

        for child in self._get_all_children():
            match child:
                case QTextBrowser():
                    pass
                case QTextEdit():
                    child.customContextMenuRequested.connect(
                        self._show_custom_context_menu
                    )
                case _:
                    pass

        self.clearButton.clicked.connect(self._clear_text)

    def view_cursor_at_position(self, widget: QTextEdit, position: int):
        cursor = QTextCursor(widget.document())
        cursor.setPosition(position)
        widget.setTextCursor(cursor)

    def _add_widgets_for_toolbar(self) -> None:
        self.segmentCheckBox = QCheckBox("分词模式", parent=self.widgetToolBar)
        self.segmentCheckBox.setEnabled(False)  # 分词模式暂时没有实现，取消勾选功能

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

    def _show_custom_context_menu(self, position):
        text_edit = self.sender()

        menu = QMenu(self)

        menu.addAction(self.undoAction)
        menu.addAction(self.redoAction)

        menu.addSeparator()

        menu.addAction(self.copyAction)
        menu.addAction(self.cutAction)
        menu.addAction(self.pasteAction)
        menu.addAction(self.pastePlainTextAction)

        menu.addSeparator()

        menu.addAction(self.selectAllAction)

        menu.exec_(text_edit.mapToGlobal(position)) # type: ignore

    def _clear_text(self):
        for child in self._get_all_children():
            match child:
                case QTextEdit() | QTextBrowser():
                    child.clear()
                    self._set_paragraph_format(
                        child, self.config.lineheight, self.config.paragraph_spacing
                    )
                case _:
                    pass

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

    def _redo(self):
        if self.focusWidget() in self._get_all_children():
            match self.focusWidget():
                case QTextBrowser():
                    pass
                case QTextEdit():
                    self.focusWidget().redo()  # type: ignore
                case _:
                    pass

    def _undo(self):
        if self.focusWidget() in self._get_all_children():
            match self.focusWidget():
                case QTextBrowser():
                    pass
                case QTextEdit():
                    self.focusWidget().undo()  # type: ignore
                case _:
                    pass

    def _copy_text(self):
        if self.focusWidget() in self._get_all_children():
            match self.focusWidget():
                case QTextBrowser():
                    pass
                case QTextEdit():
                    self.focusWidget().copy()  # type: ignore
                case _:
                    pass

    def _cut_text(self):
        if self.focusWidget() in self._get_all_children():
            match self.focusWidget():
                case QTextBrowser():
                    pass
                case QTextEdit():
                    self.focusWidget().cut()  # type: ignore
                case _:
                    pass

    def _paste_text(self):
        if self.focusWidget() in self._get_all_children():
            match self.focusWidget():
                case QTextBrowser():
                    pass
                case QTextEdit():
                    self.focusWidget().paste()  # type: ignore
                case _:
                    pass

    def _select_all_text(self):
        if self.focusWidget() in self._get_all_children():
            match self.focusWidget():
                case QTextBrowser():
                    pass
                case QTextEdit():
                    self.focusWidget().selectAll()  # type: ignore
                case _:
                    pass

    def _get_all_children(self, parent: QWidget | None = None) -> list[QWidget]:
        if parent is None:
            parent = self

        children = []
        for child in parent.children():
            children.append(child)
            children.extend(self._get_all_children(cast(QWidget, child)))

        return children

    def add_extra_format_for(
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

        extra_selection = QTextEdit.ExtraSelection()
        extra_selection.cursor = cursor

        char_format = QTextCharFormat()
        char_format.setFontUnderline(underline)
        char_format.setFontItalic(italic)
        char_format.setFontStrikeOut(strikethrough)

        if bold:
            char_format.setFontWeight(QFont.Bold)

        if foreground is not None:
            char_format.setForeground(QColor(foreground))

        if background is not None:
            char_format.setBackground(QColor(background))
        else:
            char_format.setBackground(QColor("white"))

        extra_selection.format = char_format

        existing_selection = widget.extraSelections()
        existing_selection.append(extra_selection)

        widget.setExtraSelections(existing_selection)

    def _set_paragraph_format(
        self,
        widget: QTextEdit | QTextBrowser,
        line_height: float,
        paragraph_spacing: float,
    ):
        cursor = widget.textCursor()

        block_format = QTextBlockFormat()
        block_format.setLineHeight(
            line_height * 100, QTextBlockFormat.ProportionalHeight
        )
        block_format.setBottomMargin(paragraph_spacing)

        cursor.setBlockFormat(block_format)

    def _apply_default_style(self):
        self.setStyleSheet(
            f"""
            QTextEdit {{
                font-size: {self.config.fontsize}pt;
                line-height: 150%;
            }}
            QTextBrowser {{
                font-size: {self.config.fontsize}pt;
            }}
        """
        )

        for child in self._get_all_children():
            match child:
                case QTextEdit() | QTextBrowser():
                    self._set_paragraph_format(
                        child, self.config.lineheight, self.config.paragraph_spacing
                    )
                case _:
                    pass
