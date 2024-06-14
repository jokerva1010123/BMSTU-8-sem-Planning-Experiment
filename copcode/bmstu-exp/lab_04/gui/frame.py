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

        self.MainTable = Table(master=self, rows=27, columns=19)
        self.MainTable.grid(column=0, row=1, padx=5, pady=5)

        self.MainTable.set_row(0, [
            '№', "x0", "x1", "x2", "x3", "x4", "x1x2", "x1x3", "x1x4", "x2x3", "x2x4", "x3x4",
            "x1^2 - S", "x2^2 - S", "x3^2 - S", "x4^2 - S", "Y", "Y'", "|Y - Y'|"
        ])


        self.formula_frame = tk.Frame(
            master=self,
            highlightbackground="lightgrey",
            highlightthickness=1)

        self.not_lin_formula = tk.StringVar()

        sep = tk.Label(self.formula_frame, text="*" * 44)
        sep.grid(row=1, column=0, columnspan=2, sticky="we")

        not_lin_label = tk.Label(self.formula_frame, text="Частично нелинейная модель: ")
        not_lin_label.grid(row=2, column=0, sticky="e")
        not_lin_formula_label = tk.Label(self.formula_frame, textvariable=self.not_lin_formula)
        not_lin_formula_label.grid(row=2, column=1, sticky="w")

        self.formula_frame.grid(column=0, row=2)

        N = 25
        N0 = 16
        self.S = math.sqrt(N0 / N)
        self.alpha = math.sqrt(1/2 * (math.sqrt( N * N0 ) - N0))

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

        x11=x1*x1 - self.S
        x22=x2*x2 - self.S
        x33=x3*x3 - self.S
        x44=x4*x4 - self.S

        x11c=x1*x1
        x22c=x2*x2
        x33c=x3*x3
        x44c=x4*x4

        line = [x0, x1, x2, x3, x4, x12, x13, x14, x23, x24, x34, x11, x22, x33, x44]
        linec = [x11c, x22c, x33c, x44c]
        # line_full = [x0, x1, x2, x3, x4, x12, x13, x14, x23, x24, x34, x11, x22, x33, x44, x11c, x22c, x33c, x44c, x123, x124, x134, x234, x1234]
        # line = [x0, x1, x2, x3, x4, x12, x13, x14, x23, x24, x34]
        # line2 = [x0, x1, x2, x3, x4, x12, x13, x14, x23, x24, x34, x123, x124, x134, x234, x1234]
        # line = [x0, x1, x2, x3, x4, x5, x12, x13, x14, x15, x23, x24, x25, x34, x35, x45, x11, x22, x33, x44, x55]
        # linec = [x11c, x22c, x33c, x44c, x55c]

        y = result['avg_wait_time']

        y_nl = 0
        for j in range(len(line) - 4):
            y_nl += line[j] * self.b[j]
        for j in range(4):
            y_nl += linec[j] * self.b[j + len(line) - 4]

        y_nl_per = abs(y - y_nl)

        line += [y, y_nl, y_nl_per]

        self.MainTable.set_row(26, line, 1)
        self.MainTable.set(26, 0, "Точка ФП")

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
        N = N0 + 2 * factors_amount + 1

        x0 = [1 for i in range(N)]
        x1 = [1 if i%2==1 else -1 for i in range(N0)] + [self.alpha, -self.alpha] + [0] * 7
        x2 = [-1 if i%4 < 2 else 1 for i in range(N0)] + [0] * 2 + [self.alpha, -self.alpha] + [0] * 5
        x3 = [-1 if i%8 < 4 else 1 for i in range(N0)] + [0] * 4 + [self.alpha, -self.alpha] + [0] * 3
        x4 = [-1 if i%16 < 8 else 1 for i in range(N0)] + [0] * 6 + [self.alpha, -self.alpha] + [0]

        x12 = [x1[i] * x2[i] for i in range(N)]
        x13 = [x1[i] * x3[i] for i in range(N)]
        x14 = [x1[i] * x4[i] for i in range(N)]
        x23 = [x2[i] * x3[i] for i in range(N)]
        x24 = [x2[i] * x4[i] for i in range(N)]
        x34 = [x3[i] * x4[i] for i in range(N)]

        x11 = [x1[i] * x1[i] - self.S for i in range(N)]
        x22 = [x2[i] * x2[i] - self.S for i in range(N)]
        x33 = [x3[i] * x3[i] - self.S for i in range(N)]
        x44 = [x4[i] * x4[i] - self.S for i in range(N)]

        x11c = [x1[i] * x1[i] for i in range(N)]
        x22c = [x2[i] * x2[i] for i in range(N)]
        x33c = [x3[i] * x3[i] for i in range(N)]
        x44c = [x4[i] * x4[i] for i in range(N)]

        x123 = [x1[i]*x2[i]*x3[i] for i in range(N)]
        x124 = [x1[i]*x2[i]*x4[i] for i in range(N)]
        x134 = [x1[i]*x3[i]*x4[i] for i in range(N)]
        x234 = [x2[i]*x3[i]*x4[i] for i in range(N)]

        x1234 = [x1[i]*x2[i]*x3[i]*x4[i] for i in range(N)]

        for i in range(N + 1):
            self.MainTable.set(i + 1, 0, i + 1)
        self.x_table = [x0, x1, x2, x3, x4, x12, x13, x14, x23, x24, x34, x11, x22, x33, x44]
        self.x_table2 = [x0, x1, x2, x3, x4, x12, x13, x14, x23, x24, x34, x11c, x22c, x33c, x44c, x123, x124, x134, x234, x1234]
        
        self.set_x_values()

        y = self._modelling()

        b = []
        for i in range(1):
            b.append(self._count_b(self.x_table2[i], y))
        for i in range(1, factors_amount + 1):
            b.append(self._count_b_complex(self.x_table2[i], y, N + self.alpha ** 2 * 2))
        for i in range(factors_amount + 1, 6 + factors_amount + 1):
            b.append(self._count_b_complex(self.x_table2[i], y, N0))
        for i in range(factors_amount + 1 + 6, factors_amount + 1 + 10):
            b.append(self._count_b_complex(self.x_table[i], y, self.alpha ** 4 * 2))
        for i in range(factors_amount + 1 + 10, 14 + factors_amount + 2):
            b.append(self._count_b_complex(self.x_table2[i], y, N0))

        b[0] -= self.S * sum(b[11:15])

        print(f"###### B: {b}")

        self.MainTable.set_column(16, y)
        self.b = b

        y_nl = self._calc_polynomial(self.x_table2, b, len(b))
        print(f"real: {y}, nl: {y_nl}")
        y_nl_per = [abs(y[i] - y_nl[i]) for i in range(len(y))]

        self.MainTable.set_column(17, y_nl)
        self.MainTable.set_column(18, y_nl_per)
        self.MainTable.set_row(N + 1, ['-'] * 19, 1)

        x_indexes = [
            "0", "1", "2", "3", "4",
            "1x2", "1x3", "1x4", "2x3", "2x4", "3x4",
            "1^2", "2^2", "3^2", "4^2",
            "1x2x3", "1x2x4", "1x3x4", "2x3x4",
            "1x2x3x4"
        ]

        not_lin_str = "y = {:.5g}".format(b[0])
        for i in range (1, 5):
            if i % 4 == 0:
                not_lin_str += '\n'
            if i >= 3:
                not_lin_str += " - " + str('{:.5g}'.format(abs(b[i]))) + " * x" + x_indexes[i]
            else:
                not_lin_str += " + " + str('{:.5g}'.format(abs(b[i]))) + " * x" + x_indexes[i]
        # not_lin_str += " - " + str('{:.5g}'.format(abs(b[4]))) + " * x" + x_indexes[4]
        
        for i in range (5, 11):
            if i % 4 == 0:
                not_lin_str += '\n'
            if (b[i] > 0):
                not_lin_str += " + " + str('{:.5g}'.format(b[i])) + " * x" + x_indexes[i]
            else:
                not_lin_str += " - " + str('{:.5g}'.format(math.fabs(b[i]))) + " * x" + x_indexes[i]
        
        for i in range(11, 15):
            if i % 4 == 0:
                not_lin_str += '\n'
            if i >= 13:
                not_lin_str += " - " + str('{:.5g}'.format(abs(b[i]))) + " * x" + x_indexes[i]
            else:
                not_lin_str += " + " + str('{:.5g}'.format(abs(b[i]))) + " * x" + x_indexes[i]

        for i in range (15, len(b)):
            if i % 4 == 0:
                not_lin_str += '\n'
            if (b[i] > 0):
                not_lin_str += " + " + str('{:.5g}'.format(b[i])) + " * x" + x_indexes[i]
            else:
                not_lin_str += " - " + str('{:.5g}'.format(math.fabs(b[i]))) + " * x" + x_indexes[i]

        print(not_lin_str)

        self.not_lin_formula.set(not_lin_str)

    def _count_b(self, x, y): 
        sum = 0
        for i in range(len(x)):
            sum += x[i] * y[i]
        sq_sum = 0
        for i in range(len(x)):
            sq_sum += x[i]* x[i]
        return sum / sq_sum

    def _count_b_complex(self, x, y, delim):
        sum = 0
        for i in range(len(x)):
            sum += x[i] * y[i]
        return sum / delim

    def _calc_polynomial(self, x_table, b, l):
        y_lin = []
        for i in range(len(x_table[0])):
            # x = x_table[i] 
            y = 0
            for j in range(l):
                # print(f"CELL [{j}][{i}]", x_table[j][i], b[j])
                y += x_table[j][i] * b[j]
            y_lin.append(y)
        return y_lin
