from PyQt5.QtWidgets import QApplication, QTextBrowser, QTextEdit
from PyQt5.QtGui import QTextCursor, QTextBlockFormat, QTextCharFormat, QColor, QFont

from typing import Any, TypeAlias, Literal

from .UI import Window, MyHighlighter
from .models import CmpModel, ClaimModel

ClickType: TypeAlias = Literal["<left>", "<double-L>", "right"]

GREEN = "#95FA9B"
PINK = "pink"


class App(QApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setApplicationName("helper")
        self.setApplicationVersion("0.1.0")
        self.setOrganizationName("江苏中心")

        self.window = Window()

        self.cmp_model = CmpModel()
        self.claim_model = ClaimModel("")

        self.connectSignalsAndSlots()

        self.window.show()

    def connectSignalsAndSlots(self):
        self.window.cmpWidget.cmpButton.clicked.connect(self.compare_texts)
        self.window.checkButton.clicked.connect(self.check_defects)

        self.window.resultText.textClicked.connect(self.on_text_clicked)

        self.window.claimText.textChanged.connect(self.reset_claim_model)

    def reset_claim_model(self):
        claims = self.window.claimText.toPlainText()
        self.claim_model.reset_model(claims)

        print("Triggered")

    def check_defects(self) -> None:
        self.check_claim_defects()

        self.display_check_result()

    def check_claim_defects(self) -> None:
        # self.clear_formatting(self.window.claimText)
        # self.set_line_spacing(self.window.claimText, 1.2)
        # self.claim_highlighter = MyHighlighter(self.window.claimText, r"^[0-9]{1,3}\.", bold=True)

        self.check_claim_ref_basis()

    def check_claim_ref_basis(self) -> None:
        if not self.window.segmentCheckBox.isChecked():
            length = self.window.lengthSpinBox.value()
            self.claim_model.check_all_reference_basis(length)

    def display_check_result(self) -> None:
        self.window.resultText.clear()

        if self.window.claimCheckbox.isChecked():
            self.window.resultText.add_text("【 权利要求缺陷 】 ", bold=True)
            ref_paths = self.claim_model.get_all_reference_paths()
            self.window.resultText.add_text(
                "(查看引用关系)\n",
                foreground="blue",
                underline=True,
                record_position=True,
                data={"type": "open ref_dialog", "data": ref_paths},
            )

            self.window.display_reference_basis(self.claim_model.reference_basis)

        # self.set_line_spacing(self.window.resultText, 1.5)

    def on_text_clicked(self, data: dict[str, Any], click_type: ClickType):
        if click_type == "<left>":
            self.handle_left_click(data)
        elif click_type == "<double-L>":
            self.handle_double_click(data)
        elif click_type == "<right>":
            self.handle_right_click(data)

    def handle_left_click(self, data):
        if data["type"] == "open ref_dialog":
            self.open_ref_dialog(data)
        elif data["type"] == "reference basis":
            position = data["data"].position
            term = data["data"].term
            pre, _ = data["data"].context.split(term)
            start_pos, end_pos = data["position"]
            self.center_cursor_at_position(self.window.claimText, position)
            color = self.get_widget_text_color(
                self.window.resultText, start_pos, end_pos
            )
            print(color)
            self.format_widget_text(
                self.window.claimText, position, position + len(pre), background=color
            )

    def handle_double_click(self, data):
        # TODO
        if data["type"] == "reference basis":
            start_pos, end_pos = data["position"]
            key = data["data"].position
            claim_number = data["claim_num"]
            if (
                self.claim_model.reference_basis[claim_number][key].hasbasis_confirmed
                is not True
            ):
                self.window.resultText.format_text(start_pos, end_pos, background=GREEN)
                self.claim_model.reference_basis[claim_number][
                    key
                ].hasbasis_confirmed = True
            else:
                self.window.resultText.format_text(start_pos, end_pos, background=None)
                self.claim_model.reference_basis[claim_number][
                    key
                ].hasbasis_confirmed = None

    def handle_right_click(self, data):
        # TODO
        if data["type"] == "reference basis":
            start_pos, end_pos = data["position"]
            key = data["data"].position
            claim_number = data["claim_num"]
            if (
                self.claim_model.reference_basis[claim_number][key].hasbasis_confirmed
                is not False
            ):
                self.window.resultText.format_text(start_pos, end_pos, background=PINK)
                self.claim_model.reference_basis[claim_number][
                    key
                ].hasbasis_confirmed = False
            else:
                self.window.resultText.format_text(start_pos, end_pos, background=None)
                self.claim_model.reference_basis[claim_number][
                    key
                ].hasbasis_confirmed = None

    def open_ref_dialog(self, data):
        text = [
            f"<b>权利要求{key}</b>: {', '.join(str(v) for v in value)}"
            for key, value in data["data"].items()
        ]

        self.window.refDialog.refTextBrowser.clear()
        self.window.refDialog.refTextBrowser.setHtml("<br>".join(text))

        self.window.refDialog.show()

    def compare_texts(self) -> None:
        self.window.cmpWidget.clear_format()

        a, b = self.window.cmpWidget.get_texts()
        self.cmp_model.set_seqs(a=a, b=b)

        cmp_result = self.cmp_model.compare()
        self.window.cmpWidget.format_text(cmp_result)

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

    def clear_formatting(self, widget: QTextEdit):
        cursor = QTextCursor(widget.document())
        cursor.beginEditBlock()
        cursor.select(QTextCursor.Document)

        # 移除所有字符格式
        char_format = QTextCharFormat()
        char_format.clearBackground()
        char_format.clearForeground()
        cursor.setCharFormat(char_format)

        cursor.endEditBlock()

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

        extra_selection = QTextBrowser.ExtraSelection()
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

    def get_widget_text_color(
        self, widget: QTextBrowser, start_pos: int, end_pos: int, *, background: bool = True
    ) -> str:
        # TODO
        extra_selections = widget.extraSelections()

        for selection in extra_selections:
            if start_pos <= selection.cursor.position() <= end_pos:
                if background:
                    return selection.format.background().color().name()
                else:
                    return selection.format.foreground().color().name()

    def center_cursor_at_position(self, widget: QTextEdit, position: int):
        cursor = QTextCursor(widget.document())
        cursor.setPosition(position)
        widget.setTextCursor(cursor)

        rect = widget.cursorRect(cursor)
        content_height = widget.viewport().height()
        offset_y = (content_height - rect.height()) // 2 - rect.y()
        widget.verticalScrollBar().setValue(
            widget.verticalScrollBar().value() + offset_y
        )
