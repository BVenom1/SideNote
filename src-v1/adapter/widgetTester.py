from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCore import QRect

import sys

def test(title: str, create_widget):
    app = QApplication(sys.argv)
    test_widget = create_widget()
    window = QMainWindow()
    window.setWindowTitle(title)
    window.setGeometry(QRect(100, 100, 800, 600))
    window.setCentralWidget(test_widget)

    window.show()
    app.exec()