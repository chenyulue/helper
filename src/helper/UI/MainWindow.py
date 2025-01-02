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

from . import resources_rc  # noqa: F401
from .Ui_MainWindow import Ui_mainWindow

from . import AboutDialog, SearchDialog, RefDialog, CmpWidget

from ..Config import TextFormatterConfig
from ..core.Types import RefBasis


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

        self.resize(1000, 618)

        self._add_widgets_for_toolbar()

        self._apply_default_style()

        self._connect_signals_and_slots()

    # ========================= 缺乏引用基础缺陷展示 ===================================
    def display_reference_basis(
        self,
        ref_basis: Iterator[tuple[int, dict[int, RefBasis]]],
        has_basis: set[int],
        lack_basis: set[int],
    ):
        n = 0
        for claim_number, bases in ref_basis:
            for position, basis in bases.items():
                if position in lack_basis:
                    start_pos, end_pos = self._format_ref_basis(
                        n + 1, claim_number, basis, has_basis
                    )
                    self.resultText.format_text(start_pos, end_pos, background=self.config.failure)
                    n += 1
                elif position in has_basis and self.showAllCheckBox.isChecked():
                    start_pos, end_pos = self._format_ref_basis(
                        n + 1, claim_number, basis, has_basis
                    )
                    self.resultText.format_text(start_pos, end_pos, background=self.config.success)
                    n += 1
                elif basis.hasbasis_checked is False and position not in has_basis:
                    start_pos, end_pos = self._format_ref_basis(
                        n + 1, claim_number, basis, has_basis
                    )
                    self.resultText.format_text(start_pos, end_pos, background=None)
                    n += 1
                elif (
                    isinstance(basis.hasbasis_checked, list)
                    and position not in has_basis
                ):
                    start_pos, end_pos = self._format_ref_basis(
                        n + 1, claim_number, basis, has_basis
                    )
                    self.resultText.format_text(start_pos, end_pos, background=None)
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
            "type": "reference basis",
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

        self.copyAction.triggered.connect(self._copy_text)
        self.cutAction.triggered.connect(self._cut_text)
        self.pasteAction.triggered.connect(self._paste_text)

        self.clearButton.clicked.connect(self._clear_text)

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

    def _clear_text(self):
        for child in self._get_all_children():
            match child:
                case QTextEdit() | QTextBrowser():
                    child.clear()
                    self._set_line_height(child, self.config.lineheight)
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

    def _copy_text(self):
        if self.focusWidget() in self._get_all_children():
            match self.focusWidget():
                case QTextEdit():
                    self.focusWidget().copy()  # type: ignore
                case _:
                    pass

    def _cut_text(self):
        if self.focusWidget() in self._get_all_children():
            match self.focusWidget():
                case QTextEdit():
                    self.focusWidget().copy()  # type: ignore
                case _:
                    self.focusWidget().cut()  # type: ignore

    def _paste_text(self):
        if self.focusWidget() in self._get_all_children():
            match self.focusWidget():
                case QTextEdit():
                    self.focusWidget().copy()  # type: ignore
                case _:
                    self.focusWidget().paste()  # type: ignore

    def _get_all_children(self, parent: QWidget | None = None) -> list[QWidget]:
        if parent is None:
            parent = self

        children = []
        for child in parent.children():
            children.append(child)
            children.extend(self._get_all_children(child))

        return children

    def _set_line_height(self, widget: QTextEdit | QTextBrowser, line_height: float):
        cursor = widget.textCursor()

        block_format = QTextBlockFormat()
        block_format.setLineHeight(
            line_height * 100, QTextBlockFormat.ProportionalHeight
        )

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
                    self._set_line_height(child, self.config.lineheight)
                case _:
                    pass
