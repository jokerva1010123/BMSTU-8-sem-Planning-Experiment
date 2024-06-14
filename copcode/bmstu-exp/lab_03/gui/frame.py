import math

import tkinter as tk
from tkinter import messagebox

from experiment.exp import modelling
from .table import Table


class FrameFFE(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        label = tk.Label(self,text="Полный факторный эксперимент")
        label.grid(column=0)

        self.MainTable = Table(master=self, rows=18, columns=17)
        self.MainTable.grid(column=0, row=1, padx=5, pady=5)

        self.MainTable.set_row(0, [
            '№', "x0", "x1", "x2", "x3", "x4", "x1x2", "x1x3", "x1x4", "x2x3", "x2x4", "x3x4",
            "y", "ŷ_lin", "ŷ_pnl", "|y - ŷ_lin|", "|y - ŷ_pnl|"
        ])

        self.formula_frame = tk.Frame(
            master=self,
            highlightbackground="lightgrey",
            highlightthickness=1)

        self.lin_formula = tk.StringVar()
        self.not_lin_formula = tk.StringVar()
        lin_label = tk.Label(self.formula_frame, text="Линейная модель: ")
        lin_label.grid(row=0, column=0, sticky="e")
        lin_formula_label = tk.Label(self.formula_frame, textvariable=self.lin_formula)
        lin_formula_label.grid(row=0, column=1, sticky="w")

        sep = tk.Label(self.formula_frame, text="*" * 44)
        sep.grid(row=1, column=0, columnspan=2, sticky="we")

        not_lin_label = tk.Label(self.formula_frame, text="Частично нелинейная модель: ")
        not_lin_label.grid(row=2, column=0, sticky="e")
        not_lin_formula_label = tk.Label(self.formula_frame, textvariable=self.not_lin_formula)
        not_lin_formula_label.grid(row=2, column=1, sticky="w")

        self.formula_frame.grid(column=0, row=2)

    def set_x_values(self):
        for i in range(len(self.x_table)):
            self.MainTable.set_column(i + 1, self.x_table[i])

    def _modelling(self):
        y = []

        i_lam = (self.lambda_max - self.lambda_min) / 2
        lam0 = (self.lambda_max + self.lambda_min) / 2
        i_lam2 = (self.lambda2_max -self.lambda2_min) / 2
        lam02 = (self.lambda2_max + self.lambda2_min) / 2
        i_mu = (self.mu_max - self.mu_min)/2
        mu0 = (self.mu_max + self.mu_min)/2
        i_standdev = (self.mu_disp_max - self.mu_disp_min) / 2
        standdev0 = (self.mu_disp_max + self.mu_disp_min) / 2

        for i in range(len(self.x_table[0])):
            result = modelling(
                clients_number=self.count,
                mean1=(1 / (self.x_table[1][i] * i_lam + lam0)),
                mean2=(1 / (self.x_table[2][i]* i_lam2 + lam02)),
                mean3=(1 / (self.x_table[3][i]* i_mu + mu0)),
                standdev=(self.x_table[4][i] * i_standdev + standdev0),
            )
            y.append(result['avg_wait_time'])
        return y

    def count_one(self, lam, lam2, mu, disp):
        if (lam < self.lambda_min) or (lam > self.lambda_max) or (lam2 < self.lambda_min) \
                or (lam2 > self.lambda_max) or (mu < self.mu_min) or (mu > self.mu_max):
            messagebox.showerror(title="error", message="Точка не входит в промежуток варьирования!")
            return

        result = modelling(
                clients_number=self.count,
                mean1=(1 / lam),
                mean2=(1 / lam2),
                mean3=(1 / mu),
                standdev=disp
            )
        
        i_lam = (self.lambda_max - self.lambda_min) / 2
        lam0 = (self.lambda_max + self.lambda_min) / 2
        i_lam2 = (self.lambda2_max -self.lambda2_min) / 2
        lam02 = (self.lambda2_max + self.lambda2_min) / 2
        i_mu = (self.mu_max - self.mu_min)/2
        mu0 = (self.mu_max + self.mu_min)/2
        i_standdev = (self.mu_disp_max - self.mu_disp_min) / 2
        standdev = (self.mu_disp_max + self.mu_disp_min) / 2

        x0 = 1
        x1 = (lam - lam0) / i_lam
        x2 = (lam2  - lam02) / i_lam2
        x3 = (mu - mu0) / i_mu
        x4 = (disp - standdev) / i_standdev
        x12 = x1 * x2
        x13 = x1 * x3
        x14 = x1 * x4
        x23 = x2 * x3
        x24 = x2 * x4
        x34 = x3 * x4

        x123 = x1*x2*x3
        x124 = x1*x2*x4
        x134 = x1*x3*x4
        x234 = x2*x3*x4

        x1234 = x1*x2*x3*x4

        line = [x0, x1, x2, x3, x4, x12, x13, x14, x23, x24, x34]
        line2 = [x0, x1, x2, x3, x4, x12, x13, x14, x23, x24, x34, x123, x124, x134, x234, x1234]

        y = result['avg_wait_time']

        y_lin = 0
        for j in range(4 + 1):
            y_lin += line2[j] * self.b[j]

        y_nl = 0
        for j in range(len(line2)):
            y_nl += line2[j] * self.b[j]

        y_lin_per = abs(y - y_lin)
        y_nl_per = abs(y - y_nl)

        line += [y, y_lin, y_nl, y_lin_per, y_nl_per]

        self.MainTable.set_row(17, line, 1)
        self.MainTable.set(17, 0, "Точка ФП")

    def run_ffe(self, lambda_min, lambda_max, lambda2_min, lambda2_max, mu_min, mu_max, disp_min, disp_max, count):
        self.lambda_max = lambda_max
        self.lambda_min = lambda_min
        self.lambda2_max = lambda2_max
        self.lambda2_min = lambda2_min
        self.mu_max = mu_max
        self.mu_min = mu_min
        self.mu_disp_min = disp_min
        self.mu_disp_max = disp_max

        self.count = count
        factors_amount = 4
        N0 = 2 ** (factors_amount)
        x0 = [1 for i in range(N0)]
        x1 = [1 if i%2==1 else -1 for i in range(N0)]
        x2 = [-1 if i%4 < 2 else 1 for i in range(N0)]
        x3 = [-1 if i%8 < 4 else 1 for i in range(N0)]
        x4 = [-1 if i%16 < 8 else 1 for i in range(N0)]

        x12 = [x1[i] * x2[i] for i in range(N0)]
        x13 = [x1[i] * x3[i] for i in range(N0)]
        x14 = [x1[i] * x4[i] for i in range(N0)]
        x23 = [x2[i] * x3[i] for i in range(N0)]
        x24 = [x2[i] * x4[i] for i in range(N0)]
        x34 = [x3[i] * x4[i] for i in range(N0)]

        x123 = [x1[i]*x2[i]*x3[i] for i in range(N0)]
        x124 = [x1[i]*x2[i]*x4[i] for i in range(N0)]
        x134 = [x1[i]*x3[i]*x4[i] for i in range(N0)]
        x234 = [x2[i]*x3[i]*x4[i] for i in range(N0)]

        x1234 = [x1[i]*x2[i]*x3[i]*x4[i] for i in range(N0)]

        for i in range(N0 + 1):
            self.MainTable.set(i + 1, 0, i + 1)
        self.x_table = [x0, x1, x2, x3, x4, x12, x13, x14, x23, x24, x34]
        self.x_table2 = [x0, x1, x2, x3, x4, x12, x13, x14, x23, x24, x34, x123, x124, x134, x234, x1234]
        self.set_x_values()

        y = self._modelling()

        b = []
        for i in range(len(self.x_table2)):
            b.append(self._count_b(self.x_table2[i], y))

        print(b)

        self.MainTable.set_column(12, y)
        self.b = b

        # Считаем линейную и частично не линейную модели
        y_lin = self._calc_polynomial(self.x_table2, b, factors_amount + 1)
        y_nl = self._calc_polynomial(self.x_table2, b, len(b))
        print(f"real: {y}, nl: {y_nl}")

        y_lin_per = [abs(y[i] - y_lin[i]) for i in range(len(y))]
        y_nl_per = [abs(y[i] - y_nl[i]) for i in range(len(y))]

        self.MainTable.set_column(13, y_lin)
        self.MainTable.set_column(14, y_nl)
        self.MainTable.set_column(15, y_lin_per)
        self.MainTable.set_column(16, y_nl_per)
        self.MainTable.set_row(N0 + 1, ['-'] * 17, 1)

        lin_str = "y = " + str('{:.5f}'.format(b[0]))

        for i in range (1, factors_amount + 1):
            if (b[i] > 0):
                lin_str += " + " + str('{:.3f}'.format(b[i])) + " * x" + str(i)
            else:
                lin_str += " - " + str('{:.3f}'.format(math.fabs(b[i]))) + " * x" + str(i)

        print(lin_str)
        x_indexes = [
            "0", "1", "2", "3", "4",
            "1x2", "1x3", "1x4", "2x3", "2x4", "3x4",
            "1x2x3", "1x2x4", "1x3x4", "2x3x4",
            "1x2x3x4"
        ]
        not_lin_str = "y = {:.5g}".format(b[0])
        for i in range (1, len(b)):
            if i % 4 == 0:
                not_lin_str += '\n'
            if (b[i] > 0):
                not_lin_str += " + " + str('{:.5g}'.format(b[i])) + " * x" + x_indexes[i]
            else:
                not_lin_str += " - " + str('{:.5g}'.format(math.fabs(b[i]))) + " * x" + x_indexes[i]
        print(not_lin_str)

        self.lin_formula.set(lin_str)
        self.not_lin_formula.set(not_lin_str)

    def _count_b(self, x, y): 
        sum = 0
        for i in range(len(x)):
            sum += x[i] * y[i]
        return sum / len(x)

    def _calc_polynomial(self, x_table, b, l):
        y_lin = []
        for i in range(len(x_table[0])):
            # x = x_table[i] 
            y = 0
            for j in range(l):
                print(f"CELL [{j}][{i}]", x_table[j][i], b[j])
                y += x_table[j][i] * b[j]
            y_lin.append(y)
        return y_lin


class FramePFE(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        label = tk.Label(self,text="Дробный факторный эксперимент")
        label.grid(row=0)

        self.MainTable = Table(master=self, rows=10, columns=17)
        self.MainTable.grid(column=0, row=1, padx=5, pady=5)

        self.MainTable.set_row(0, [
            '№',"x0", "x1", "x2", "x3", "x4",
            "x1x2", "x1x3", "x1x4", "x2x3", "x2x4", "x3x4",
            "y", "ŷ_lin", "ŷ_pnl", "|y - ŷ_lin|", "|y - ŷ_pnl|"
        ])

        self.formula_frame = tk.Frame(
            master=self,
            highlightbackground="lightgrey",
            highlightthickness=1)

        self.lin_formula = tk.StringVar()
        self.not_lin_formula = tk.StringVar()
        lin_label = tk.Label(  self.formula_frame, text="Линейная модель: ")
        lin_label.grid(row=0, column=0, sticky="e")
        lin_formula_label = tk.Label(self.formula_frame, textvariable=self.lin_formula)
        lin_formula_label.grid(row=0, column=1, sticky="w")

        not_lin_label = tk.Label(self.formula_frame, text="Частично нелинейная модель: ")
        not_lin_label.grid(row=1, column=0, sticky="e")
        not_lin_formula_label = tk.Label(self.formula_frame, textvariable=self.not_lin_formula)
        not_lin_formula_label.grid(row=1, column=1, sticky="w")

        self.formula_frame.grid(column=0, row=2, padx=10, pady=10)


    def set_x_values(self):
        for i in range(len(self.x_table)):
            self.MainTable.set_column(i + 1, self.x_table[i])

    def _modelling(self):
        y = []

        i_lam = (self.lambda_max - self.lambda_min) / 2
        lam0 = (self.lambda_max + self.lambda_min) / 2
        i_lam2 = (self.lambda2_max -self.lambda2_min) / 2
        lam02 = (self.lambda2_max + self.lambda2_min) / 2
        i_mu = (self.mu_max - self.mu_min)/2
        mu0 = (self.mu_max + self.mu_min)/2
        i_standdev = (self.mu_disp_max - self.mu_disp_min) / 2
        standdev0 = (self.mu_disp_max + self.mu_disp_min) / 2

        for i in range(len(self.x_table[0])):
            result = modelling(
                clients_number=self.count,
                mean1=(1 / (self.x_table[1][i] * i_lam + lam0)),
                mean2=(1 / (self.x_table[2][i]* i_lam2 + lam02)),
                mean3=(1 / (self.x_table[3][i]* i_mu + mu0)),
                standdev=(self.x_table[4][i] * i_standdev + standdev0),
            )
            y.append(result['avg_wait_time'])
        return y

    def count_one(self, lam, lam2, mu, disp):
        if (lam < self.lambda_min) or (lam > self.lambda_max) or (lam2 < self.lambda_min) \
                or (lam2 > self.lambda_max) or (mu < self.mu_min) or (mu > self.mu_max):
            messagebox.showerror(title="error", message="Точка не входит в промежуток варьирования!")
            return

        result = modelling(
                clients_number=self.count,
                mean1=(1 / lam),
                mean2=(1 / lam2),
                mean3=(1 / mu),
                standdev=disp
            )
        print(result)
        
        i_lam = (self.lambda_max - self.lambda_min) / 2
        lam0 = (self.lambda_max + self.lambda_min) / 2
        i_lam2 = (self.lambda2_max -self.lambda2_min) / 2
        lam02 = (self.lambda2_max + self.lambda2_min) / 2
        i_mu = (self.mu_max - self.mu_min) / 2
        mu0 = (self.mu_max + self.mu_min) / 2
        i_standdev = (self.mu_disp_max - self.mu_disp_min) / 2
        standdev = (self.mu_disp_max + self.mu_disp_min) / 2

        x0 = 1
        x1 = (lam - lam0) / i_lam
        x2 = (lam2  - lam02) / i_lam2
        x3 = (mu - mu0) / i_mu
        x4 = (disp - standdev) / i_standdev
        x12 = x1 * x2
        x13 = x1 * x3
        x14 = x1 * x4
        x23 = x2 * x3
        x24 = x2 * x4
        x34 = x3 * x4

        x123 = x1*x2*x3
        x124 = x1*x2*x4
        x134 = x1*x3*x4
        x234 = x2*x3*x4

        x1234 = x1*x2*x3*x4

        line = [x0, x1, x2, x3, x4, x12, x13, x14, x23, x24, x34]
        line2 = [x0, x1, x2, x3, x4, x12, x13, x14, x23, x24, x34, x123, x124, x134, x234, x1234]

        y = result['avg_wait_time']

        y_lin = 0
        for j in range(4 + 1):
            y_lin += line2[j] * self.b[j]

        y_nl = 0
        for j in range(len(line2)):
            y_nl += line2[j] * self.b[j]

        y_lin_per = abs(y - y_lin)
        y_nl_per = abs(y - y_nl)

        line += [y, y_lin, y_nl, y_lin_per, y_nl_per]

        self.MainTable.set_row(9, line, 1)
        self.MainTable.set(9, 0, "Точка ФП")


    def run_pfe(self, lambda_min, lambda_max, lambda2_min, lambda2_max, mu_min, mu_max, disp_min, disp_max, count):
        self.lambda_max = lambda_max
        self.lambda_min = lambda_min
        self.lambda2_max = lambda2_max
        self.lambda2_min = lambda2_min
        self.mu_max = mu_max
        self.mu_min = mu_min
        self.mu_disp_min = disp_min
        self.mu_disp_max = disp_max

        self.count = count
        factors_amount = 4
        N0 = 2 ** (factors_amount - 1)
        x0 = [1 for i in range(N0)]
        x1 = [1 if i%2==1 else -1 for i in range(N0)]
        x2 = [-1 if i%4 < 2 else 1 for i in range(N0)]
        x3 = [-1 if i%8 < 4 else 1 for i in range(N0)]
        x4 = [x1[i] * x2[i] * x3[i] for i in range(N0)]

        x12 = [x1[i] * x2[i] for i in range(N0)]
        x13 = [x1[i] * x3[i] for i in range(N0)]
        x14 = [x1[i] * x4[i] for i in range(N0)]
        x23 = [x2[i] * x3[i] for i in range(N0)]
        x24 = [x2[i] * x4[i] for i in range(N0)]
        x34 = [x3[i] * x4[i] for i in range(N0)]

        x123 = [x1[i]*x2[i]*x3[i] for i in range(N0)]
        x124 = [x1[i]*x2[i]*x4[i] for i in range(N0)]
        x134 = [x1[i]*x3[i]*x4[i] for i in range(N0)]
        x234 = [x2[i]*x3[i]*x4[i] for i in range(N0)]
        
        x1234 = [x1[i]*x2[i]*x3[i]*x4[i] for i in range(N0)]

        for i in range(N0 + 1):
            self.MainTable.set(i + 1, 0, i + 1)

        self.x_table = [x0, x1, x2, x3, x4, x12, x13, x14, x23, x24, x34]
        self.x_table2 = [x0, x1, x2, x3, x4, x12, x13, x14, x23, x24, x34, x123, x124, x134, x234, x1234]
        self.set_x_values()

        y = self._modelling()

        b = []
        for i in range(len(self.x_table2)):
            b.append(self._count_b(self.x_table2[i], y))
        print(b)

        self.MainTable.set_column(12, y)
        self.b = b

        b_nl = b[:5] + [el / 2 for el in b[5:11]] + [0] * 5  # + [el / 2 for el in b[10:4:-1]]
        print(b_nl)
        self.b_nl = b_nl

        # Считаем линейную и частично не линейную модели
        # print(f"ALARM!!!!! {len(self.x_table2)}x{len(self.x_table2[0])}, {len(b)}, {len(b_nl)}, {factors_amount + 1}")
        y_lin = self._calc_polynomial(self.x_table2, b, factors_amount + 1)
        # print(f"ALARM!!!!! {len(self.x_table2)}, {len(b_nl)}")
        y_nl = self._calc_polynomial(self.x_table2, b_nl, len(b_nl))

        y_lin_per = [abs(y[i] - y_lin[i]) for i in range(len(y))]
        y_nl_per = [abs(y[i] - y_nl[i]) for i in range(len(y))]

        self.MainTable.set_column(13, y_lin)
        self.MainTable.set_column(14, y_nl)
        self.MainTable.set_column(15, y_lin_per)
        self.MainTable.set_column(16, y_nl_per)
        # self.MainTable.set_row(N0 + 1, [''] * 25, 1)

        lin_str = "y = {:.3f}".format(b[0])

        for i in range (1, factors_amount + 1):
            if (b[i] > 0):
                lin_str += " + " + str('{:.3f}'.format(b[i])) + " * x" + str(i)
            else:
                lin_str += " - " + str('{:.3f}'.format(math.fabs(b[i]))) + " * x" + str(i)

        print(lin_str)
        x_indexes = [
            "0", "1", "2", "3", "4",
            "1x2", "1x3", "1x4", "2x3", "2x4", "3x4",
            "1x2x3", "1x2x4", "1x3x4", "2x3x4",
            "1x2x3x4",
        ]

        not_lin_str = "y = " + str('{:.5g}'.format(b[0]))
        for i in range (1, len(b_nl)):
            if i % 4 == 0:
                not_lin_str += '\n'
            if (b_nl[i] >= 0):
                not_lin_str += " + " + str('{:.5g}'.format(b_nl[i])) + " * x" + x_indexes[i]
            else:
                not_lin_str += " - " + str('{:.5g}'.format(math.fabs(b_nl[i]))) + " * x" + x_indexes[i]
        # print(not_lin_str)

        self.lin_formula.set(lin_str)
        self.not_lin_formula.set(not_lin_str)


    def _count_b(self, x, y): 
        sum = 0
        for i in range(len(x)):
            sum += x[i] * y[i]
        return sum / len(x)

    def _calc_polynomial(self, x_table, b, l):
        y_lin = []
        for i in range(len(x_table[0])):
            # x = x_table[i] 
            y = 0
            for j in range(l):
                y += x_table[j][i] * b[j]
            # y = max(0.0, y)
            y_lin.append(max(0.0, y))
        return y_lin
