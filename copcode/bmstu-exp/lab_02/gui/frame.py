import tkinter as tk
from tkinter import messagebox

from experiment.exp import modelling

from .table import Table


class FrameFFE(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.MainTable = Table(master=self, rows=9, columns=14)
        self.MainTable.pack(padx=10, pady=10)
        self.AdditionalTable = Table(master=self, rows=1, columns=14)
        self.AdditionalTable.pack(padx=10, pady=0)

        self.BTable = Table(master=self, rows=2, columns=8)
        self.BTable.pack(padx=10, pady=10)

        col_names = [
            "№", "x0", "x1", "x2", "x3", "x1x2", "x1x3", "x2x3", "x1x2x3",
            "y", "ŷ_lin", "ŷ_pnl", "|y - ŷ_lin|", "|y - ŷ_pnl|"
        ]
        for i, name in enumerate(col_names):
            self.MainTable.set(0, i, name)

        regression_col_names = ["b0", "b1", "b2", "b3", "b12", "b13", "b23", "b123"]
        for i, name in enumerate(regression_col_names):
            self.BTable.set(0, i, name)

    def set_x_values(self):
        for i in range(len(self.x_table)):
            self.MainTable.set_column(i + 1, self.x_table[i])

    def _modelling(self):
        y = []
        for i in range(len(self.x_table[0])):
            result = modelling(
                clients_number=self.count,
                mean1=(1 / self.lambda_min if self.x_table[1][i] == -1 else 1 / self.lambda_max),
                mean2=(1 / self.mu_min if self.x_table[2][i] == -1 else 1 / self.mu_max),
                standdev=(self.mu_disp_min if self.x_table[3][i] == -1 else self.mu_disp_max),
            )
            y.append(result['avg_wait_time'])
        return y

    def count_one(self, lam, mu, disp):
        if (lam < self.lambda_min) or (lam > self.lambda_max) or (mu < self.mu_min) or (mu > self.mu_max):
            messagebox.showerror(title="error", message="Точка не входит в промежуток варьирования!")
            return

        result = modelling(
                clients_number=self.count,
                mean1=(1 / lam),
                mean2=(1 / mu),
                standdev=disp
            )

        x0 = 1
        i_lam = (self.lambda_max - self.lambda_min) / 2
        lam0 = (self.lambda_max + self.lambda_min) / 2
        x1 = (lam - lam0) / i_lam
        i_mu = (self.mu_max - self.mu_min) / 2
        mu0 = (self.mu_max + self.mu_min) / 2

        x2 = (mu - mu0) / i_mu
        i_disp = (self.mu_disp_max - self.mu_disp_min) / 2
        disp0 = (self.mu_disp_max + self.mu_disp_min) / 2

        x3 = (disp - disp0) / i_disp
        x12 = x1 * x2
        x13 = x1 * x3
        x23 = x2 * x3
        x123 = x1*x2*x3

        line = [x0, x1, x2, x3, x12, x13, x23, x123]
        y = result['avg_wait_time']

        y_lin = 0
        for j in range(3):
            y_lin += line[j] * self.b[j]

        y_nl = 0
        for j in range(len(line)):
            y_nl += line[j] * self.b[j]

        y_lin_per = abs(y - y_lin)
        y_nl_per = abs(y - y_nl)

        line += [y, y_lin, y_nl, y_lin_per, y_nl_per]

        self.AdditionalTable.set_row(0, line, 1)

    def run_ffe(self, lambda_min, lambda_max, mu_min, mu_max, disp_min, disp_max, count):
        self.lambda_max = lambda_max
        self.lambda_min = lambda_min
        self.mu_max = mu_max
        self.mu_min = mu_min
        self.mu_disp_min = disp_min
        self.mu_disp_max = disp_max
        self.count = count
        exp_count = 8

        x0 = [1 for i in range(exp_count)]
        x1 = [-1 if i % 2 == 0 else 1 for i in range(exp_count)]
        x2 = [-1 if i % 4 < 2 else 1 for i in range(exp_count)]
        x3 = [-1 if i % 8 < 4 else 1 for i in range(exp_count)]
        x12 = [x1[i] * x2[i] for i in range(len(x1))]
        x13 = [x1[i] * x3[i] for i in range(len(x1))]
        x23 = [x2[i] * x3[i] for i in range(len(x2))]
        x123 = [x1[i] * x2[i] * x3[i] for i in range(len(x1))]

        self.x_table = [x0, x1, x2, x3, x12, x13, x23, x123]
        self.set_x_values()
        print(self.x_table)

        y = self._modelling()
        for i in range(9):
            self.MainTable.set(i + 1, 0, i + 1)

        b = []
        for x in [x0, x1, x2, x3, x12, x13, x23, x123]:
            b.append(self._count_b(x, y))
        print(b)

        self.MainTable.set_column(9, y)
        self.BTable.set_row(1, b)
        self.b = b

        y_lin = self._calc_polynomial(self.x_table, b, 4)
        y_nl = self._calc_polynomial(self.x_table, b, len(b))

        y_lin_per = [abs(y[i] - y_lin[i]) for i in range(len(y))]
        y_nl_per = [abs(y[i] - y_nl[i]) for i in range(len(y))]

        self.MainTable.set_column(10, y_lin)
        self.MainTable.set_column(11, y_nl)
        self.MainTable.set_column(12, y_lin_per)
        self.MainTable.set_column(13, y_nl_per)
        self.AdditionalTable.set_row(0, ['-'] * 13, 1)

    def _count_b(self, x, y): 
        sum = 0
        for i in range(len(x)):
            sum += x[i] * y[i]
        return sum / len(x)

    def _calc_polynomial(self, x_table, b, l):
        y_lin = []
        for i in range(len(x_table)):
            # x = x_table[i] 
            y = 0
            for j in range(l): 
                y += x_table[j][i] * b[j]
            y_lin.append(y)
        return y_lin
