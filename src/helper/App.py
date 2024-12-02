from PyQt5.QtWidgets import (
    QApplication,
)

from .UI import Window
from .models import CmpModel, ClaimModel

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

    def check_defects(self) -> None:
        self.check_claim_defects()

    def check_claim_defects(self) -> None:
        claims = self.window.claimText.toPlainText()
        self.claim_model.reset_model(claims)
        
        self.check_claim_ref_basis()

    def check_claim_ref_basis(self) -> None:
        if not self.window.segmentCheckBox.isChecked():
            length = self.window.lengthSpinBox.value()
            self.claim_model.check_all_reference_basis(length)
            self.window.display_reference_basis(self.claim_model.reference_basis)

    def compare_texts(self) -> None:
        self.window.cmpWidget.clear_format()
        
        a, b = self.window.cmpWidget.get_texts()
        self.cmp_model.set_seqs(a=a, b=b)

        cmp_result = self.cmp_model.compare()
        self.window.cmpWidget.format_text(cmp_result)
