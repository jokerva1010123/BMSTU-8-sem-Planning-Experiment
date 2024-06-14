import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox

from mainwindow import Ui_MainWindow
from experiment.exp import modelling, view


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_model.clicked.connect(self.onModelBtnClick)
        self.ui.pushButton_graph.clicked.connect(self.onGraphBtnClick)

    def addItemTableWidget(self, row, column, value):
        item = QTableWidgetItem()
        item.setText(str(value))
        self.ui.tableWidget.setItem(row, column, item)

    def onModelBtnClick(self):
        try:
            n_request = self.ui.spinbox_req.value()
            intensivity_gen = self.ui.spinbox_intensivity_gen.value()
            intensivity_proc = self.ui.spinbox_intensivity_oa.value()
            range_proc = self.ui.spinbox_intensivity_oa_range.value()
            
            result = modelling(
                n_request,
                1 / intensivity_gen,
                1 / intensivity_proc,
                range_proc
            )

            # System workload
            theor_workload = intensivity_gen / intensivity_proc
            exp_workload = (result['time'] - result['free_time']) / result['time']
            self.addItemTableWidget(0, 0, round(theor_workload, 3))
            self.addItemTableWidget(0, 1, round(exp_workload, 3))

            _translate = QtCore.QCoreApplication.translate
            # Avg time in machine
            self.ui.label_8.setText(_translate("MainWindow", f"Среднее время пребывания заявки в СМО: {round(result['avg_wait_time'], 3)}"))

            # Modelling time
            self.ui.label_9.setText(_translate("MainWindow", f"Общее время моделирования: {round(result['time'], 3)}"))

        except Exception as e:
            msgBox = QMessageBox()
            msgBox.setText('Произошла ошибка!\n' + repr(e))
            msgBox.show()
            msgBox.exec()

    def onGraphBtnClick(self):
        view()


if __name__ == "__main__":
    app = QApplication([])
    application = MyWindow()
    application.show()

    sys.exit(app.exec())
