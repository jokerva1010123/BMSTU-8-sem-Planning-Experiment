from interface import Ui_MainWindow
from PyQt5 import QtGui, QtWidgets
from model import Queue
import sys
from regression import *

class Window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.run_btn.clicked.connect(self.process)
        self.check_btn.clicked.connect(self.check)
        self.checkBox.stateChanged.connect(self.update_limits)
        self.results = [0 for i in range(8)]
        self.lin_x = ['x1', 'x2', 'x3']
        self.nonlin_x = ['x1', 'x2', 'x3', 'x1x2', 'x1x3', 'x2x3', 'x1x2x3']

    def update_limits(self):
        if self.checkBox.isChecked():
            self.service_sigma_float_check.setMaximum(1.00)
            self.service_sigma_float_check.setMinimum(-1.00)
            self.generator_float_check.setMaximum(1.00)
            self.generator_float_check.setMinimum(-1.00)
            self.service_float_check.setMaximum(1.00)
            self.service_float_check.setMinimum(-1.00)
        else:
            self.service_sigma_float_check.setMaximum(100.00)
            self.service_sigma_float_check.setMinimum(0.00)
            self.generator_float_check.setMaximum(100.00)
            self.generator_float_check.setMinimum(0.00)
            self.service_float_check.setMaximum(100.00)
            self.service_float_check.setMinimum(0.00)
        
    def get_results(self):
        sum = 0.0
        times = 50
        queue = Queue(self.min_gen_intensity, self.min_service_intensity, self.min_sigma)
        for i in range(times):
            sum += queue.start(self.time)
        self.results[0] = sum / times
        # print('12.5%')
        sum = 0.0
        queue = Queue(self.max_gen_intensity, self.min_service_intensity, self.min_sigma)
        for i in range(times):
            sum += queue.start(self.time)
        self.results[1] = sum / times
        # print('25%')
        sum = 0.0
        queue = Queue(self.min_gen_intensity, self.max_service_intensity, self.min_sigma)
        for i in range(times):
            sum += queue.start(self.time)
        self.results[2] = sum / times
        # print('37.5%')
        sum = 0.0
        queue = Queue(self.max_gen_intensity, self.max_service_intensity, self.min_sigma)
        for i in range(times):
            sum += queue.start(self.time)
        self.results[3] = sum / times
        # print('50%')
        sum = 0.0
        queue = Queue(self.min_gen_intensity, self.min_service_intensity, self.max_sigma)
        for i in range(times):
            sum += queue.start(self.time)
        self.results[4] = sum / times
        # print('62.5%')
        sum = 0.0
        queue = Queue(self.max_gen_intensity, self.min_service_intensity, self.max_sigma)
        for i in range(times):
            sum += queue.start(self.time)
        self.results[5] = sum / times
        # print('75%')
        sum = 0.0
        queue = Queue(self.min_gen_intensity, self.max_service_intensity, self.max_sigma)
        for i in range(times):
            sum += queue.start(self.time)
        self.results[6] = sum / times
        # print('87.5%')
        sum = 0.0
        queue = Queue(self.max_gen_intensity, self.max_service_intensity, self.max_sigma)
        for i in range(times):
            sum += queue.start(self.time)
        self.results[7] = sum / times
        # print('100%')

    def process(self):
        try:
            self.time = self.time_spinbox.value()
            self.max_sigma = self.service_sigma_float_max.value()
            self.max_gen_intensity = self.generator_float_max.value()
            self.max_service_intensity = self.service_float_max.value()
            
            self.min_sigma = self.service_sigma_float_min.value()
            self.min_gen_intensity = self.generator_float_min.value()
            self.min_service_intensity = self.service_float_min.value()

            self.get_results()
            self.matrix, self.lin_coeffs, self.nonlin_coeffs = get_matrix(8, self.results)

            self.nat_lin_coeffs = get_natural_coeffs(self.lin_coeffs, [self.min_gen_intensity, self.min_service_intensity, self.min_sigma],
                                                                        [self.max_gen_intensity, self.max_service_intensity, self.max_sigma], True)

            self.nat_nonlin_coeffs = get_natural_coeffs(self.nonlin_coeffs, [self.min_gen_intensity, self.min_service_intensity, self.min_sigma],
                                                                            [self.max_gen_intensity, self.max_service_intensity, self.max_sigma], False)
            
            self.lin_normal.setText(build_equation(self.lin_coeffs, self.lin_x))
            self.lin_natural.setText(build_equation(self.nat_lin_coeffs, self.lin_x))
            self.nonlin_normal.setText(build_equation(self.nonlin_coeffs, self.nonlin_x))
            self.nonlin_natural.setText(build_equation(self.nat_nonlin_coeffs, self.nonlin_x))

            for i in range(len(self.nonlin_coeffs)):
                self.coeff_table.setItem(0, i, QtWidgets.QTableWidgetItem("{:.2f}".format(self.nonlin_coeffs[i])))
            
            for i in range(len(self.matrix)):
                for j in range(len(self.matrix[0])):
                    self.result_table.setItem(i, j, QtWidgets.QTableWidgetItem("{:.2f}".format(self.matrix[i][j])))
        except:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Некорректный ввод")


    def check(self):
        try:
            self.sigma = self.service_sigma_float_check.value()
            self.gen_intense = self.generator_float_check.value()
            self.serv_intense = self.service_float_check.value()

            if self.checkBox.isChecked():
                norm_x1 = self.gen_intense
                norm_x2 = self.serv_intense
                norm_x3 = self.sigma
                self.sigma = self.sigma * (self.max_sigma - self.min_sigma) / 2.0 + (self.max_sigma + self.min_sigma) / 2.0
                self.gen_intense = self.gen_intense * (self.max_gen_intensity - self.min_gen_intensity) / 2.0 + (self.max_gen_intensity + self.min_gen_intensity) / 2.0
                self.serv_intense = self.serv_intense * (self.max_service_intensity - self.min_service_intensity) / 2.0 + (self.max_service_intensity + self.min_service_intensity) / 2.0
            
            else:
                norm_x1 = (self.gen_intense - (self.max_gen_intensity + self.min_gen_intensity) / 2) / (self.max_gen_intensity - self.min_gen_intensity) * 2
                norm_x2 = (self.serv_intense - (self.max_service_intensity + self.min_service_intensity) / 2) / (self.max_service_intensity - self.min_service_intensity) * 2
                norm_x3 = (self.sigma - (self.max_sigma + self.min_sigma) / 2) / (self.max_sigma - self.min_sigma) * 2
            
            self.result_table.setItem(8, 0, QtWidgets.QTableWidgetItem("{:.2f}".format(1.00)))
            self.result_table.setItem(8, 1, QtWidgets.QTableWidgetItem("{:.2f}".format(norm_x1)))
            self.result_table.setItem(8, 2, QtWidgets.QTableWidgetItem("{:.2f}".format(norm_x2)))
            self.result_table.setItem(8, 3, QtWidgets.QTableWidgetItem("{:.2f}".format(norm_x3)))
            self.result_table.setItem(8, 4, QtWidgets.QTableWidgetItem("{:.2f}".format(norm_x1 * norm_x2)))
            self.result_table.setItem(8, 5, QtWidgets.QTableWidgetItem("{:.2f}".format(norm_x1 * norm_x3)))
            self.result_table.setItem(8, 6, QtWidgets.QTableWidgetItem("{:.2f}".format(norm_x2 * norm_x3)))
            self.result_table.setItem(8, 7, QtWidgets.QTableWidgetItem("{:.2f}".format(norm_x1 * norm_x2 * norm_x3)))

            sum = 0.0
            times = 50
            
            queue = Queue(self.gen_intense, self.serv_intense, self.sigma)
            for i in range(times):
                sum += queue.start(self.time)
            check_result = sum / times
            self.result_table.setItem(8, 8, QtWidgets.QTableWidgetItem("{:.2f}".format(check_result)))
            
            lin_y = get_result(self.lin_coeffs, self.lin_x, [norm_x1, norm_x2, norm_x3])
            nonlin_y = get_result(self.nonlin_coeffs, self.nonlin_x, [norm_x1, norm_x2, norm_x3])
            
            self.result_table.setItem(8, 9, QtWidgets.QTableWidgetItem("{:.2f}".format(lin_y)))
            self.result_table.setItem(8, 10, QtWidgets.QTableWidgetItem("{:.2f}".format(nonlin_y)))
            self.result_table.setItem(8, 11, QtWidgets.QTableWidgetItem("{:.2f}".format(abs(lin_y - check_result))))
            self.result_table.setItem(8, 12, QtWidgets.QTableWidgetItem("{:.2f}".format(abs(nonlin_y - check_result))))
        except:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Некорректный ввод")

    def exit(self):
        sys.exit(0)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    win.show()
    app.exec()