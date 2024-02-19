from PyQt5 import QtWidgets
import sys
import app_window


if (__name__ == "__main__"):
    app = QtWidgets.QApplication([])
    application = app_window.AppWindow()
    sys.exit(app.exec())
