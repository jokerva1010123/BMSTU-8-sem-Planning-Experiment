import tkinter as tk
from Table import Table
from functions import *
import math

class DfeFrame(tk.Frame): 
    def __init__(self, master): 
        super().__init__(master)

        label = tk.Label(self,text="ДФЭ") 
        label.grid(row=0)

        self.MainTable = Table(master=self, rows=10, columns=17)
        self.MainTable.grid(column=0, row=1, padx=5, pady=5)

        self.MainTable.set_row(
            0, 
            ['№',"x0", "x1", "x2", "x3", "x4", 
             "x12","x13","x14", "x23", "x24", "x34",  
            "Y", "Yл", "Yчн", "|Y - Yл|", "|Y - Yчн|"]
            )


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
            self.MainTable.set_column(i+1, self.x_table[i])

    def modelling(self): 
        y = []
        i_lam = (self.lambda_max -self.lambda_min)/2
        lam0 = (self.lambda_max + self.lambda_min)/2
        i_mu = (self.mu_max -self.mu_min)/2
        mu0 = (self.mu_max + self.mu_min)/2
        
        i_lam2 = (self.lambda2_max -self.lambda2_min)/2
        lam02 = (self.lambda2_max + self.lambda2_min)/2
        i_mu2 = (self.mu2_max -self.mu2_min)/2
        mu02 = (self.mu2_max + self.mu2_min)/2
        for i in range(len(self.x_table[0])):
            result = modelling(
                clients_number=self.count+1000,
                clients_proccessed=self.count,
                lambda_coming= self.x_table[1][i] * i_lam + lam0,
                lambda_obr=self.x_table[2][i]* i_mu + mu0, 
                lambda_coming2=self.x_table[3][i] * i_lam2 + lam02,
                lambda_obr2=self.x_table[2][i]* i_mu2 + mu02, 
            )

            y.append(result['wait_time_middle'])
        return y

    def count_one(self, lam, mu, lam2=None, mu2=None):
        if lam < self.lambda_min or lam > self.lambda_max or mu < self.mu_min or mu > self.mu_max: 
            tk.messagebox.showinfo(title="error", message="Точка не входит в промежуток варьирования!")
            return 

        result = modelling(
                clients_number=self.count+1000,
                clients_proccessed=self.count,
                lambda_coming=lam,
                lambda_obr=mu,
                lambda_coming2=lam2 or lam, 
                lambda_obr2=mu2 or mu,
            )

        print(result)
        i_lam = (self.lambda_max -self.lambda_min)/2
        lam0 = (self.lambda_max + self.lambda_min)/2
        i_mu = (self.mu_max -self.mu_min)/2
        mu0 = (self.mu_max + self.mu_min)/2
        
        i_lam2 = (self.lambda2_max -self.lambda2_min)/2
        lam02 = (self.lambda2_max + self.lambda2_min)/2
        i_mu2 = (self.mu2_max -self.mu2_min)/2
        mu02 = (self.mu2_max + self.mu2_min)/2

        x0 = 1

        x1 = (lam - lam0)/i_lam
        x2 = (mu - mu0)/i_mu
        x3 = (lam2  - lam02)/i_lam2
        x4 = (mu2 - mu02)/ i_mu2
        x12 = x1 * x2
        x13 = x1 * x3
        x14 = x1 * x4
        x23 = x2 * x3
        x24 = x2 * x4
        x34 = x3 * x4 
        x123 = x1*x2*x3
        x124 = x1*x2*x4
        x134 = x1*x4*x3
        x234 = x2*x3*x4
        x1234 = x1*x2*x3*x4

        line = ( [x0] + [x1] + [x2] + [x3] + [x4] 
                + [x12] + [x13] + [x14] + [x23] + [x24] + [x34] )

        line2 = ( [x0] + [x1] + [x2] + [x3] + [x4] 
                + [x12] + [x13] + [x14] + [x23] + [x24] + [x34] 
                + [x123]+[x124]+[x134] +[x234]+[x1234])
        y = result['wait_time_middle']

        s = 0
        l = 5
        for j in range(l): 
            s += line[j] * self.b[j]
        y_lin = s

        s = 0
        l = len(self.b_nl)
        for j in range(l): 
            s += line2[j] * self.b_nl[j]
        y_nl = s

        y_lin_per = abs(y - y_lin)
        y_nl_per = abs(y - y_nl)

        line += [y] + [y_lin] + [y_nl] + [y_lin_per] + [y_nl_per]

        self.MainTable.set_row(9, line, 1)

    def run(self, lambda_min, lambda_max, mu_min, mu_max, count, lambda2_min, lambda2_max, mu2_min, mu2_max):
        self.lambda_max = lambda_max
        self.lambda_min = lambda_min
        self.mu_max = mu_max
        self.mu_min = mu_min
        self.lambda2_max = lambda2_max
        self.lambda2_min = lambda2_min
        self.mu2_max = mu2_max
        self.mu2_min = mu2_min
        self.count = count
        lin_count = 4
        exp_count = 8
        # считаем иксы
        x0 = [1 for i in range(exp_count)]
        x1 = [1 if i%2==1 else -1 for i in range(exp_count)]
        x2 = [-1 if i%4 < 2 else 1 for i in range(exp_count)]
        x3 = [-1 if i%8 < 4 else 1  for i in range(exp_count)]
        x4 = [x1[i]*x2[i]*x3[i] for i in range(len(x1))] 
        x12 = [x1[i]*x2[i] for i in range(len(x1))]
        x13 = [x1[i]*x3[i] for i in range(len(x1))]
        x14 = [x1[i]*x4[i] for i in range(len(x1))]
        x23 = [x2[i]*x3[i] for i in range(len(x2))]
        x24 = [x2[i]*x4[i] for i in range(len(x2))]
        x34 = [x3[i]*x4[i] for i in range(len(x2))]
        x123 = [x1[i]*x2[i]*x3[i] for i in range(len(x1))]
        x124 = [x1[i]*x2[i]*x4[i] for i in range(len(x1))]
        x134 = [x1[i]*x3[i]*x4[i] for i in range(len(x1))]
        x234 = [x2[i]*x3[i]*x4[i] for i in range(len(x2))]
        x1234 = [x1[i]*x2[i]*x3[i]*x4[i] for i in range(len(x2))]

        # отображаем иксы
        for i in range(exp_count + 1):
            self.MainTable.set(i+1, 0, i+1)
        self.x_table = [x0] + [x1] + [x2] + [x3] +[x4]+ [x12] + [x13] + [x14] + [x23] + [x24] + [x34]
        self.x_table2 =( [x0] + [x1] + [x2] + [x3] + [x4] 
                        + [x12] + [x13] + [x14] + [x23] + [x24] + [x34] 
                        + [x123] + [x124] + [x134] + [x234] + [x1234] )
        self.set_x_values()


        # Считаем игреки
        y = self.modelling()

        # Считаем b
        b = []
        for i in range(exp_count):
            b.append(self.count_b(self.x_table[i], y))
        
        print(b)
        

        # Отображаем игреки и b
        self.MainTable.set_column(12, y)
        self.b = b

        b_nl = [b/2 for b  in self.b] +  [b[i]/2 for i in range(len(b)-1, -1, -1)]
        print(b_nl)
        self.b_nl = b_nl

        # Считаем линейную и частично не линейную модели
        y_lin = self.count_lin(self.x_table2, b, lin_count+1)
        y_nl = self.count_lin(self.x_table2, b_nl, len(b_nl))
        
        y_lin_per = [abs(y[i] - y_lin[i]) for i in range(len(y))]
        y_nl_per = [abs(y[i] - y_nl[i]) for i in range(len(y))]

        # Отрисовываем
        self.MainTable.set_column( 13, y_lin)
        self.MainTable.set_column(14, y_nl)
        self.MainTable.set_column(15, y_lin_per)
        self.MainTable.set_column(16, y_nl_per)
        self.MainTable.set_row(9, ['','','','','','',
                                    '','','','','','',''], 1)


        lin_str = "y = " + str('{:.5g}'.format(b[0]))
        for i in range (1, 5): 
            if (b[i] > 0):
                lin_str += " + " + str('{:.5g}'.format(b[i])) + " * x" + str(i)
            else: 
                lin_str += " - " + str('{:.5g}'.format(math.fabs(b[i]))) + " * x" + str(i)
        
        print(lin_str)
        x_indexes = ["0", "1", "2", "3", "4", 
             "12","13","14", "23", "24", "34", 
             "123","124","134", "234", "1234",]
        not_lin_str = "y = " + str('{:.5g}'.format(b[0]))
        for i in range (1, len(b_nl)):
            if i == round(len(b_nl)/2):
                not_lin_str += '\n' 
            if (b_nl[i] > 0):
                not_lin_str += " + " + str('{:.5g}'.format(b_nl[i])) + " * x" + x_indexes[i]
            else: 
                not_lin_str += " - " + str('{:.5g}'.format(math.fabs(b_nl[i]))) + " * x" + x_indexes[i]
        # print(not_lin_str)

        self.lin_formula.set(lin_str)
        self.not_lin_formula.set(not_lin_str)
        
            

    def count_b(self, x, y): 
        sum = 0
        for i in range(len(y)):
            sum += x[i]*y[i]
        return sum/len(x)


    def count_lin(self, x_table, b, l):
        y_lin = []
        for i in range(len(x_table[0])):
            x = x_table[i] 
            y = 0
            for j in range(l): 
                y += x_table[j][i]*b[j]
            y_lin.append(y)
        return y_lin 