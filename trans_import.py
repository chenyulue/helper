import sys

file = sys.argv[1]

with open(file, "r+", encoding="utf-8") as f:
    content = f.read()
    if file.endswith("Ui_MainWindow.py"):
        content = content.replace(
            "from PyQt5 import QtCore, QtGui, QtWidgets",
            (
                "from PyQt5 import QtCore, QtGui, QtWidgets\n\n"
                "from .CutomWidgets import CustomTextBrowser\n\n"
                "QtWidgets.QTextBrowser = CustomTextBrowser"
            ),
        )
    f.seek(0)
    f.write(content.replace("import resources_rc", "from . import resources_rc"))
    f.truncate()
