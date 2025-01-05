from typing import Any, TypeAlias, Literal, cast
from itertools import chain
from contextlib import contextmanager

from PyQt5.QtWidgets import QApplication, QTextEdit, QTextBrowser
from PyQt5.QtGui import QClipboard

from .core import BaseChecker
from .core.Types import CheckType
from .checkers import CheckManager
from .parser import ClaimModel, DescriptionModel
from .UI import MainWindow
from .Config import TextFormatterConfig

ClickType: TypeAlias = Literal["<left>", "<double-L>", "<right>"]


class Application(QApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setApplicationName("helper")
        self.setApplicationVersion("0.1.0")
        self.setOrganizationName("江苏中心")

        self.textconfig = TextFormatterConfig.new()

        self.check_manager = CheckManager()

        self.claim = ClaimModel("")
        self.description = DescriptionModel("")

        self.main_window = MainWindow()

        self.results = {}
        self.claim_checkers = {}

        self.connect_signals_and_slots()

        self.main_window.show()

    def connect_signals_and_slots(self):
        self.main_window.checkButton.clicked.connect(self.start_checks)

        self.main_window.claimText.textChanged.connect(self.init_claim_checkers)
        self.main_window.resultText.textClicked.connect(self.on_text_clicked)

        self.main_window.claimCheckbox.stateChanged.connect(
            lambda: self.display_checkers(self.results)
        )
        self.main_window.descriptionCheckbox.stateChanged.connect(
            lambda: self.display_checkers(self.results)
        )
        self.main_window.abstractCheckbox.stateChanged.connect(
            lambda: self.display_checkers(self.results)
        )
        self.main_window.showAllCheckBox.stateChanged.connect(
            lambda: self.display_checkers(self.results)
        )

        self.main_window.pastePlainTextAction.triggered.connect(self._paste_plain_text)

    def init_claim_checkers(self) -> None:
        text = self.main_window.claimText.toPlainText()
        self.main_window.claimText.setExtraSelections([])
        self.claim.reset_model(text)

        self.claim_checkers = {
            (obj := check_type(self.claim)).name: obj
            for check_type in self.check_manager.checkers["claim"]
        }

    def run_checkers(self) -> dict[CheckType, tuple[BaseChecker, Any]]:
        result: dict[CheckType, Any] = {}
        for checker in chain(self.claim_checkers.values()):
            length = self.main_window.lengthSpinBox.value()
            result[checker.name] = (checker, checker.check(length=length))

        return result

    def display_checkers(self, results: dict[CheckType, tuple[BaseChecker, Any]]):
        self.main_window.resultText.clear()
        self.main_window._set_paragraph_format(
            self.main_window.resultText,
            self.textconfig.lineheight,
            self.textconfig.paragraph_spacing,
        )

        for name, (checker, result) in results.items():
            show_claim = self.main_window.claimCheckbox.isChecked()
            show_description = self.main_window.descriptionCheckbox.isChecked()
            show_abstract = self.main_window.abstractCheckbox.isChecked()
            checker.display(
                self.main_window,
                result,
                show_claim=show_claim,
                show_description=show_description,
                show_abstract=show_abstract,
            )

    def start_checks(self) -> None:
        self.results = self.run_checkers()
        self.display_checkers(self.results)

    def on_text_clicked(self, data: dict[str, Any], click_type: ClickType):
        if click_type == "<left>":
            self.handle_left_click(data)
        elif click_type == "<double-L>":
            self.handle_double_click(data)
        elif click_type == "<right>":
            self.handle_right_click(data)

    def handle_left_click(self, data):
        match data["type"]:
            case CheckType.CheckReferencePaths:
                self.open_ref_dialog(data)
            case CheckType.LackOfReferenceBasis:
                position = data["data"].position
                self.main_window.view_cursor_at_position(
                    self.main_window.claimText, position
                )

    def handle_double_click(self, data):
        match data["type"]:
            case CheckType.LackOfReferenceBasis:
                start_pos, end_pos = data["position"]
                term_pos = data["data"].position

                claim_position = data["data"].position
                claim_term = data["data"].term
                claim_pre, _ = data["data"].context.split(claim_term)
                ref_checkers = self.claim_checkers[CheckType.LackOfReferenceBasis]
                if term_pos not in ref_checkers.has_basis:
                    ref_checkers.update_has_basis(term_pos)

                    self.main_window.resultText.add_extra_format(
                        start_pos, end_pos, background=self.textconfig.success
                    )

                    with self.disable_signals() as self:
                        self.main_window.add_extra_format_for(
                            self.main_window.claimText,
                            start_pos=claim_position,
                            end_pos=claim_position + len(claim_pre),
                            background=self.textconfig.success,
                        )
                else:
                    ref_checkers.update_has_basis(term_pos, False)

                    self.main_window.resultText.add_extra_format(
                        start_pos, end_pos, background=None
                    )

                    with self.disable_signals() as self:
                        self.main_window.add_extra_format_for(
                            self.main_window.claimText,
                            start_pos=claim_position,
                            end_pos=claim_position + len(claim_pre),
                            background=None,
                        )
            case _:
                pass

    def handle_right_click(self, data):
        match data["type"]:
            case CheckType.LackOfReferenceBasis:
                start_pos, end_pos = data["position"]
                term_pos = data["data"].position

                claim_position = data["data"].position
                claim_term = data["data"].term
                claim_pre, _ = data["data"].context.split(claim_term)
                ref_checkers = self.claim_checkers[CheckType.LackOfReferenceBasis]
                if term_pos not in ref_checkers.lack_basis:
                    ref_checkers.update_lack_basis(term_pos)

                    self.main_window.resultText.add_extra_format(
                        start_pos, end_pos, background=self.textconfig.failure
                    )

                    with self.disable_signals() as self:
                        self.main_window.add_extra_format_for(
                            self.main_window.claimText,
                            start_pos=claim_position,
                            end_pos=claim_position + len(claim_pre),
                            background=self.textconfig.failure,
                        )
                else:
                    ref_checkers.update_lack_basis(term_pos, False)

                    self.main_window.resultText.add_extra_format(
                        start_pos, end_pos, background=None
                    )
                    with self.disable_signals() as self:
                        self.main_window.add_extra_format_for(
                            self.main_window.claimText,
                            start_pos=claim_position,
                            end_pos=claim_position + len(claim_pre),
                            background=None,
                        )
            case _:
                pass

    def open_ref_dialog(self, data):
        text = [
            f"<b>权利要求{key}</b>: {', '.join(str(v) for v in value)}"
            for key, value in data["data"].items()
        ]

        self.main_window.refDialog.refTextBrowser.clear()
        self.main_window.refDialog.refTextBrowser.setHtml("<br>".join(text))

        self.main_window.refDialog.show()

    def _paste_plain_text(self):
        clipboard = self.clipboard()
        plain_text = cast(QClipboard, clipboard).text()

        focus_widget = self.focusWidget()
        match focus_widget:
            case QTextBrowser():
                pass
            case QTextEdit():
                focus_widget.insertPlainText(plain_text)
            case _:
                pass

    @contextmanager
    def disable_signals(self):
        self.main_window.claimText.textChanged.disconnect(self.init_claim_checkers)
        try:
            yield self
        finally:
            self.main_window.claimText.textChanged.connect(self.init_claim_checkers)


if __name__ == "__main__":
    app = Application([])
    app.exec_()
