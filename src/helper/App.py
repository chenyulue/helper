from PyQt5.QtWidgets import QApplication, QTextBrowser, QTextEdit, QMessageBox
from PyQt5.QtGui import QTextCursor

from typing import Any, TypeAlias, Literal, Callable

from .UI import Window
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

        self._first_check = True

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
        try:
            self.claim_model.reset_model(claims)
            self._first_check = True
        except ValueError as e:
            self.window._showWarningDialog(str(e))

    def check_defects(self) -> None:
        self.check_claim_defects()

        self.display_check_result()

    def check_claim_defects(self) -> None:
        # 如果是第一次检查，格式化相关文本
        if self._first_check:
            widget = self.window.claimText
            self.format_text(widget, self.window.clear_widget_formatting)
            self.format_text(widget, self.window.set_line_spacing, line_spacing=1.5)
            self.format_text(
                widget,
                self.window.format_widget_with_pattern,
                pattern=r"^[0-9]{1,3}\.",
                bold=True,
            )
        self._first_check = False

        self.check_claim_ref_basis()

        self.check_claim_multiple_dependencies()

        self.check_claim_small_defects()

    def check_claim_ref_basis(self) -> None:
        if not self.window.segmentCheckBox.isChecked():
            length = self.window.lengthSpinBox.value()
            self.claim_model.check_all_reference_basis(length)

    def check_claim_multiple_dependencies(self) -> None:
        self.claim_model.check_all_multiple_dependencies()

    def check_claim_small_defects(self):
        self.claim_model.check_all_alternative_reference()

    def display_check_result(self) -> None:
        self.window.resultText.clear()

        if self.window.claimCheckbox.isChecked():
            self.window.resultText.add_text("👉【 权利要求缺陷 】 ", bold=True)
            ref_paths = self.claim_model.get_all_reference_paths()
            self.window.resultText.add_text(
                "(查看引用关系)\n",
                foreground="blue",
                underline=True,
                record_position=True,
                bold=True,
                data={"type": "open ref_dialog", "data": ref_paths},
            )

            self.window.display_reference_basis(self.claim_model.reference_basis)

            if self.claim_model.multiple_dependencies:
                self.window.display_multiple_dependencies(self.claim_model.multiple_dependencies)
            
            self.window.display_small_defects(self.claim_model.small_defects)

        self.window.set_line_spacing(self.window.resultText, 1.5)
        self.window.resultText.moveCursor(QTextCursor.Start)

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
            self.window.view_cursor_at_position(self.window.claimText, position)
        elif data["type"] == "multiple dependencies":
            claim_num = data["data"][0]
            claim_position = self.claim_model.claims[claim_num - 1].start_pos
            self.window.view_cursor_at_position(self.window.claimText, claim_position)
            self.format_text(
                self.window.claimText,
                self.window.format_widget_text,
                start_pos=claim_position,
                end_pos=claim_position + len(str(claim_num))+1,
                background="yellow",
            )
        elif data["type"] == "small defects":
            claim_num = data["data"]
            claim_position = self.claim_model.claims[claim_num - 1].start_pos
            self.window.view_cursor_at_position(self.window.claimText, claim_position)
            self.format_text(
                self.window.claimText,
                self.window.format_widget_text,
                start_pos=claim_position,
                end_pos=claim_position + len(str(claim_num)) + 1,
                background="#95F7FC"
            )

    def handle_double_click(self, data):
        # TODO
        if data["type"] == "reference basis":
            start_pos, end_pos = data["position"]
            key = data["data"].position
            claim_number = data["claim_num"]

            claim_position = data["data"].position
            claim_term = data["data"].term
            claim_pre, _ = data["data"].context.split(claim_term)
            if (
                self.claim_model.reference_basis[claim_number][key].hasbasis_confirmed
                is not True
            ):
                self.window.resultText.format_text(start_pos, end_pos, background=GREEN)
                self.claim_model.reference_basis[claim_number][
                    key
                ].hasbasis_confirmed = True

                self.format_text(
                    self.window.claimText,
                    self.window.format_widget_text,
                    start_pos=claim_position,
                    end_pos=claim_position + len(claim_pre),
                    background=GREEN,
                )
            else:
                self.window.resultText.format_text(start_pos, end_pos, background="white")
                self.claim_model.reference_basis[claim_number][
                    key
                ].hasbasis_confirmed = None

                self.format_text(
                    self.window.claimText,
                    self.window.format_widget_text,
                    start_pos=claim_position,
                    end_pos=claim_position + len(claim_pre),
                    background="white",
                )

    def handle_right_click(self, data):
        # TODO
        if data["type"] == "reference basis":
            start_pos, end_pos = data["position"]
            key = data["data"].position
            claim_number = data["claim_num"]

            claim_position = data["data"].position
            claim_term = data["data"].term
            claim_pre, _ = data["data"].context.split(claim_term)
            if (
                self.claim_model.reference_basis[claim_number][key].hasbasis_confirmed
                is not False
            ):
                self.window.resultText.format_text(start_pos, end_pos, background=PINK)
                self.claim_model.reference_basis[claim_number][
                    key
                ].hasbasis_confirmed = False

                self.format_text(
                    self.window.claimText,
                    self.window.format_widget_text,
                    start_pos=claim_position,
                    end_pos=claim_position + len(claim_pre),
                    background=PINK,
                )
            else:
                self.window.resultText.format_text(start_pos, end_pos, background="white")
                self.claim_model.reference_basis[claim_number][
                    key
                ].hasbasis_confirmed = None

                self.format_text(
                    self.window.claimText,
                    self.window.format_widget_text,
                    start_pos=claim_position,
                    end_pos=claim_position + len(claim_pre),
                    background="white",
                )

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

    def format_text(
        self, widget: QTextEdit | QTextBrowser, fun: Callable, **kwargs
    ):
        if isinstance(widget, QTextEdit):
            widget.textChanged.disconnect(self.reset_claim_model)

        fun(widget=widget, **kwargs)

        if isinstance(widget, QTextEdit):
            widget.textChanged.connect(self.reset_claim_model)
