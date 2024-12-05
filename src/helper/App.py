from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QTextBrowser, QVBoxLayout

from typing import Any, TypeAlias, Literal

from .UI import Window
from .models import CmpModel, ClaimModel

ClickType: TypeAlias = Literal["<left>", "<double-L>", "right"]

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

    def check_defects(self) -> None:
        self.check_claim_defects()

        self.display_check_result()

    def check_claim_defects(self) -> None:
        claims = self.window.claimText.toPlainText()
        self.claim_model.reset_model(claims)

        self.check_claim_ref_basis()

    def display_check_result(self) -> None:
        self.window.resultText.clear()

        if self.window.claimCheckbox.isChecked():
            self.window.resultText.add_text("【 权利要求缺陷 】 ", bold=True)
            ref_paths = self.claim_model.get_all_reference_paths()
            self.window.resultText.add_text(
                "(查看引用关系)\n",
                forground="blue",
                underline=True,
                record_position=True,
                data={"type": "open ref_dialog", "data": ref_paths}
            )

            self.window.display_reference_basis(self.claim_model.reference_basis)

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

    def handle_double_click(self, data):
        # TODO
        pass

    def handle_right_click(self, data):
        # TODO
        pass

    def open_ref_dialog(self, data):
        text = [f"权利要求{key}: {', '.join(str(v) for v in value)}" for key, value in data["data"].items()]

        self.window.refDialog.refTextBrowser.clear()
        self.window.refDialog.refTextBrowser.setPlainText('\n'.join(text))

        self.window.refDialog.show()

    def check_claim_ref_basis(self) -> None:
        if not self.window.segmentCheckBox.isChecked():
            length = self.window.lengthSpinBox.value()
            self.claim_model.check_all_reference_basis(length)

    def compare_texts(self) -> None:
        self.window.cmpWidget.clear_format()

        a, b = self.window.cmpWidget.get_texts()
        self.cmp_model.set_seqs(a=a, b=b)

        cmp_result = self.cmp_model.compare()
        self.window.cmpWidget.format_text(cmp_result)
