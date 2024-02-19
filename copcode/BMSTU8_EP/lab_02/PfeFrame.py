import tkinter as tk
from Table import Table
from constants import *
from functions import *

class PfeFrame(tk.Frame): 
    def __init__(self, master): 
        super().__init__(master)

        self.MainTable = Table(master=self, rows=6, columns=10)
        self.MainTable.pack(padx=10, pady=10)
        self.BTable = Table(master=self, rows=2, columns=4)
        self.BTable.pack(padx=10, pady=10)

        self.MainTable.set_row(0, ['№',"x0", "x1", "x2", "x12", "Y", "Yл", "Yчн", "|Y - Yл|", "|Y - Yчн|"])

        self.BTable.set( 0, 0, "b0")
        self.BTable.set( 0, 1, "b1")
        self.BTable.set( 0, 2, "b2")
        self.BTable.set( 0, 3, "b12")
        

    def set_x_values(self): 
        for i in range(len(self.x_table)):
            self.MainTable.set_column(i+1, self.x_table[i])

    def modelling(self): 
        y = []
        for i in range(len(self.x_table[0])):
            result = modelling(
                clients_number=self.count+1000,
                clients_proccessed=self.count,
                lambda_coming=self.lambda_min if self.x_table[1][i] == -1 else self.lambda_max,
                lambda_obr=self.mu_min if self.x_table[2][i] == -1 else self.mu_max, 
            )

            y.append(result['wait_time_middle'])
        return y

    def count_one(self, lam, mu):
        if lam < self.lambda_min or lam > self.lambda_max or mu < self.mu_min or mu > self.mu_max: 
            tk.messagebox.showinfo(title="error", message="Точка не входит в промежуток варьирования!")
            return 


        result = modelling(
                clients_number=self.count+1000,
                clients_proccessed=self.count,
                lambda_coming=lam,
                lambda_obr=mu
            )

        x0 = 1 
        I_j_lambda = (self.lambda_max - self.lambda_min)/2
        X_i_average_lambda = (self.lambda_max + self.lambda_min)/2
        x1 = (lam - X_i_average_lambda)/I_j_lambda
        
        I_j_mu = (self.mu_max -self.mu_min)/2
        X_i_average_mu = (self.mu_max + self.mu_min)/2
        x2 = (mu - X_i_average_mu)/I_j_mu
        x12 = x1 * x2

        line = [x0] + [x1] + [x2] + [x12]
        y = result['wait_time_middle']

        s = 0
        l = 3
        for j in range(l): 
            s += line[j] * self.b[j]
        y_lin = s

        s = 0
        l = len(line)
        for j in range(l): 
            s += line[j] * self.b[j]
        y_nl = s

        y_lin_per = abs(y - y_lin)
        y_nl_per = abs(y - y_nl)

        line += [y] + [y_lin] + [y_nl] + [y_lin_per] + [y_nl_per]

        self.MainTable.set_row(5, line, 1)

    def run(self, lambda_min, lambda_max, mu_min, mu_max, count):
        self.lambda_max = lambda_max
        self.lambda_min = lambda_min
        self.mu_max = mu_max
        self.mu_min = mu_min
        self.count = count
        exp_count = 4

        # считаем иксы
        x0 = [1 for i in range(exp_count)]
        x1 = [1 if i%2==1 else -1 for i in range(exp_count)]
        x2 = [-1 if i%4 < 2 else 1 for i in range(exp_count)]
        x12 = [x1[i]*x2[i] for i in range(len(x1))]

        # отображаем иксы
        self.x_table = [x0] + [x1] + [x2] + [x12]
        self.set_x_values()

        # print(self.x_table)

        # Считаем ys
        y = self.modelling()

        # Записываем нумерацию (0 столбец (№))
        for i in range(9):
            self.MainTable.set(i+1, 0, i+1)

        # Считаем b
        b0 = self.count_b(x0, y)
        b1 = self.count_b(x1, y)
        b2 = self.count_b(x2, y)
        b12 = self.count_b(x12, y)

        b = [b0] + [b1] + [b2] + [b12]
        print(b)
        

        # Отображаем игреки и b
        self.MainTable.set_column(5, y)
        self.BTable.set_row(1, b)
        self.b = b

        # Считаем линейную и частично не линейную модели 
        y_lin = self.count_lin(self.x_table, b, 3) # (Искомая функция y=b0*x0+b1*x1+b2*x2)
        y_nl = self.count_lin(self.x_table, b, len(b)) # (Искомая функция y=b0*x0+b1*x1+b2*x2+b12*x12)
        
        y_lin_per = [abs(y[i] - y_lin[i]) for i in range(len(y))]
        y_nl_per = [abs(y[i] - y_nl[i]) for i in range(len(y))]

        print(y)
        print(y_lin)
        print(y_lin_per)
        print(y_lin_per)

        # Отрисовываем
        self.MainTable.set_column(6, y_lin)
        self.MainTable.set_column(7, y_nl)
        self.MainTable.set_column(8, y_lin_per)
        self.MainTable.set_column(9, y_nl_per)
        self.MainTable.set_row(5, ['','','','','','',
                                    '','','','','','',''], 1)

    def count_b(self, x, y): 
        sum = 0
        for i in range(len(x)):
            sum += x[i]*y[i]
        return sum/len(x)

    def count_lin(self, x_table, b, l):
        y_lin = []
        for i in range(len(x_table)):
            x = x_table[i] 
            y = 0
            for j in range(l): 
                y += x_table[j][i]*b[j]
            y_lin.append(y)
        return y_lin 


            