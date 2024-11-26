from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox
from PyQt5.QtCore import Qt

class ToggleCheckBox(QCheckBox):
    def __init__(self, parent=None):
        super(ToggleCheckBox, self).__init__(parent)
        self.setFixedSize(60, 28)
        self.setStyleSheet("""
            /* Hide the default checkbox indicator */
            QCheckBox::indicator {
                width: 60px;
                height: 28px;
                border-radius: 14px;
                background-color: #ccc;
                position: absolute;
                left: 0;
                top: 0;
                transition: all 0.3s ease-in-out;
            }

            /* Change background color when checked */
            QCheckBox::indicator:checked {
                background-color: #76c7c0;
            }

            /* Create a custom slider */
            QCheckBox::indicator:after {
                content: '';
                width: 24px;
                height: 24px;
                border-radius: 12px;
                background-color: white;
                position: absolute;
                top: 2px;
                left: 2px; /* Initial position */
                transition: left 0.3s ease-in-out;
            }

            /* Move the slider to the right when checked */
            QCheckBox::indicator:checked:after {
                left: 34px; /* Final position */
            }
        """)

if __name__ == '__main__':
    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout()

    toggle_checkbox = ToggleCheckBox()
    toggle_checkbox.clicked.connect(lambda checked: print(f"Toggle is {'on' if checked else 'off'}"))
    layout.addWidget(toggle_checkbox)

    window.setLayout(layout)
    window.show()
    app.exec_()






