import tkinter as tk
from Table import Table
from functions import *
import math

class PfeFrame(tk.Frame): 
    def __init__(self, master): 
        super().__init__(master)

        # label = tk.Label(self,text="ОЦКП")
        # label.grid(column=0)

        self.MainTable = Table(master=self, rows=27, columns=19)

        self.MainTable.set_row(
            0, 
            ['№',"x0", "x1", "x2", "x3", "x4", 
             "x12","x13","x14", "x23", "x24", "x34", 
            'x1^2-a', 'x2^2-a', 'x3^2-a', 'x4^2-a', 
            "Y", "Yн", "|Y - Yн|"]
            )

        self.formula_frame = tk.Frame(
            master=self, 
            highlightbackground="lightgrey", 
            highlightthickness=1)

        self.lin_formula = tk.StringVar()
        self.not_lin_formula = tk.StringVar()
        self.a_string = tk.StringVar()
        self.alpha_string = tk.StringVar()
        a_label = tk.Label(  self.formula_frame, text="Постоянная S: ")
        a_label.grid(row=0, column=0, sticky="e")
        a_formula_label = tk.Label(self.formula_frame, textvariable=self.a_string)
        a_formula_label.grid(row=0, column=1, sticky="w")

        alpha_label = tk.Label(  self.formula_frame, text="Звездное плечо (a): ")
        alpha_label.grid(row=1, column=0, sticky="e")
        alpha_formula_label = tk.Label(self.formula_frame, textvariable=self.alpha_string)
        alpha_formula_label.grid(row=1, column=1, sticky="w")

        not_lin_label = tk.Label(self.formula_frame, text="Нелинейная модель: ")
        not_lin_label.grid(row=2, column=0, sticky="e")
        not_lin_formula_label = tk.Label(self.formula_frame, textvariable=self.not_lin_formula)
        not_lin_formula_label.grid(row=2, column=1, sticky="w")

        self.formula_frame.grid(column=0, row=1)
        self.MainTable.grid(column=0, row=2, padx=10, pady=10)


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
                lambda_obr2=self.x_table[4][i]* i_mu2 + mu02, 
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
                lambda_coming2=lam2, 
                lambda_obr2=mu2,
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
        x5 = x1*x1 - self.a 
        x6 = x2*x2 - self.a 
        x7 = x3*x3 - self.a
        x8 = x4*x4 - self.a 

        line = ( [x0] + [x1] + [x2] + [x3] + [x4] 
                + [x12] + [x13] + [x14] + [x23] + [x24] + [x34] 
                # + [x123]+[x124]+[x134] +[x234]+[x1234]
                + [x5] + [x6] + [x7] + [x8] )
        line2 = ( [x0] + [x1] + [x2] + [x3] + [x4] 
                + [x12] + [x13] + [x14] + [x23] + [x24] + [x34] 
                + [x123]+[x124]+[x134] +[x234]+[x1234]
                + [x5] + [x6] + [x7] + [x8] )
        y = result['wait_time_middle']

        s = 0
        l = len(line2)
        for j in range(l): 
            s += line2[j] * self.b[j]
        y_nl = s

        y_nl_per = abs(y - y_nl)

        line += [y] + [y_nl] + [y_nl_per]

        self.MainTable.set_row(26, line, 1)

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
        N0 = 2**(lin_count)
        N = N0 + 2 * lin_count + 1
        self.a = a = math.sqrt( N0 / N) # = 8/15 = 0.73
        self.alpha = alpha = math.sqrt(1/2 * (math.sqrt( N * N0 ) - N0 )) # = 1.215

        # считаем иксы
        x0 = [1 for i in range(N)] 
        x1 = [1 if i%2==1 else -1 for i in range(N0)] + [+alpha] + [-alpha] + [0, 0, 0, 0, 0, 0] + [0]
        x2 = [-1 if i%4 < 2 else 1 for i in range(N0)] + [0, 0, alpha, -alpha, 0,  0, 0, 0] + [0]
        x3 = [-1 if i%8 < 4 else 1 for i in range(N0)] + [0, 0, 0, 0, alpha, -alpha, 0, 0] + [0]
        x4 = [-1 if i%16 < 8 else 1 for i in range(N0)] + [0, 0, 0, 0, 0, 0, alpha, -alpha] + [0]
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

        x5 = [x1[i]*x1[i] - a for i  in range(N)] 
        x6 = [x2[i]*x2[i] - a for i  in range(N)] 
        x7 = [x3[i]*x3[i] - a for i  in range(N)]
        x8 = [x4[i]*x4[i] - a for i  in range(N)]

        # отображаем иксы
        for i in range(N+1):
            self.MainTable.set(i+1, 0, i+1)
        self.x_table = [x0] + [x1] + [x2] + [x3] +[x4]+ [x12] + [x13] + [x14] + [x23] + [x24] + [x34] + [x5] +[x6] + [x7] + [x8]
        self.x_table2 =( [x0] + [x1] + [x2] + [x3] + [x4] + [x12] + [x13] + [x14] + [x23] + [x24] + [x34] + 
                        [x123]+[x124]+[x134] +[x234]+[x1234]+ [x5] +[x6] + [x7] + [x8] )
        self.set_x_values()

        # print(self.x_table)

        # Считаем игреки
        y = self.modelling()

        # Считаем b
        b = []
        for i in range(len(self.x_table2)):
            b.append(self.count_b(self.x_table2[i], y))
        # print(b)

        b0_strih = b[0]
        for i in range(lin_count):
            b0_strih -= a * b[N0 + i]

        

        # Отображаем игреки и b
        self.MainTable.set_column(16, y)
        self.b = b

        # Считаем линейную и частично не линейную модели
        y_nl = self.count_lin(self.x_table2, b, len(self.x_table2))
        
        y_nl_per = [abs(y[i] - y_nl[i]) for i in range(len(y))]

        # Отрисовываем
        self.MainTable.set_column(17, y_nl)
        self.MainTable.set_column(18, y_nl_per)
        self.MainTable.set_row(26, ['','','','','','',
                                    '','','','','','',''], 1)

        b[0] = b0_strih
        x_indexes = ["0", "1", "2", "3", "4", 
             "12","13","14", "23", "24", "34", 
             "123","124","134", "234", "1234",
            '1^2', '2^2', '3^2', '4^2',]
        not_lin_str = "y = " + str('{:.5g}'.format(b[0]))

        # Курову важно, чтобы коэф. перед обработчиками были отрицательные, а при генераторе положительные
        inx_negative = [2, 4, 17, 19]
        inx_positive = [1, 3, 16, 18]
        for i in range (1, len(b)): 
            if i == round(len(b)/2):
                not_lin_str += '\n'
            
            if (i in inx_negative):
                not_lin_str += " - " + str('{:.4f}'.format(math.fabs(b[i]))) + " * x" + x_indexes[i]
                continue
            if (i in inx_positive):
                not_lin_str += " + " + str('{:.4f}'.format(math.fabs(b[i]))) + " * x" + x_indexes[i]
                continue

            if (b[i] > 0):
                not_lin_str += " + " + str('{:.4f}'.format(b[i])) + " * x" + x_indexes[i]
            else: 
                not_lin_str += " - " + str('{:.4f}'.format(math.fabs(b[i]))) + " * x" + x_indexes[i]
        # print(not_lin_str)

        self.not_lin_formula.set(not_lin_str)
        self.a_string.set(str( '{:.5g}'.format(a)))
        self.alpha_string.set(str('{:.5g}'.format(alpha)))
        
            

    def count_b(self, x, y): 
        sum = 0
        for i in range(len(x)):
            sum += x[i]*y[i]
        sq_sum = 0 
        for i in range(len(x)):
            sq_sum += x[i]*x[i]
        return sum/sq_sum

    def count_lin(self, x_table, b, l):
        y_lin = []
        for i in range(len(x_table[0])):
            y = 0
            for j in range(l): 
                y += x_table[j][i]*b[j]
            y_lin.append(y)
        return y_lin 