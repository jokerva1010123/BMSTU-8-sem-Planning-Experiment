from tkinter import *
import tkinter as tk
from tkinter import ttk

import gui.input as i
from gui.frame import FrameFFE


BG = "#FFFFFF"
FG = "#000000"

root = Tk()
root.title("ExpPlanning lab_04")
ffe_results_frame = FrameFFE(root)


var_list = {
    "lambda": StringVar(),
    "lambda2": StringVar(),
    "mu": StringVar(),
    "mu_disp": StringVar(),
    "k": StringVar(),
    "N": StringVar(),
    "start": StringVar(),
    "end": StringVar(),
    "N_exp": StringVar(),
    "lambda_min": StringVar(),
    "lambda_max": StringVar(),
    "lambda2_min": StringVar(),
    "lambda2_max": StringVar(),
    "mu_min": StringVar(),
    "mu_max": StringVar(),
    "mu_disp_min": StringVar(),
    "mu_disp_max": StringVar(),
}


def work_ffe(_Event):
    # try:
    lambda_min = float(var_list["lambda_min"].get())
    lambda_max = float(var_list["lambda_max"].get())
    lambda2_min = float(var_list["lambda2_min"].get())
    lambda2_max = float(var_list["lambda2_max"].get())
    mu_min = float(var_list["mu_min"].get())
    mu_max = float(var_list["mu_max"].get())
    mu_disp_min = float(var_list["mu_disp_min"].get())
    mu_disp_max = float(var_list["mu_disp_max"].get())
    count = float(var_list["N"].get())
    ffe_results_frame.run_ffe(
        lambda_min=lambda_min,
        lambda_max=lambda_max,
        lambda2_min=lambda2_min,
        lambda2_max=lambda2_max,
        mu_max=mu_max,
        mu_min=mu_min,
        count=count,
        disp_min=mu_disp_min,
        disp_max=mu_disp_max
    )

    btn_add_exp.config(state='normal')
    # except ValueError:
    #     tk.messagebox.showerror(title="error", message="Ошибка ввода параметров!")


def work_single_exp(_Event):
    lam = float(var_list["lambda"].get())
    lam2 = float(var_list["lambda2"].get())
    mu = float(var_list["mu"].get())
    mu_disp = float(var_list["mu_disp"].get())
    ffe_results_frame.count_one(lam=lam, lam2=lam2, mu=mu, disp=mu_disp)


def add_ffe_inputs(root):
    t = tk.Label(root, text="Эксперимент")
    t.grid(column=1)
    frame_inputs = Frame(root)

    items_0 = [
        i.Item(text="Число заявок:", var=var_list["N"], value=1000),
    ]
    ilist_0 = i.InputList(master=root, items=items_0)

    items = [
        [
            i.Item(text="Минимум:", var=var_list["lambda_min"], value=1),
            i.Item(text="Максимум:", var=var_list["lambda_max"], value=3),
        ], [
            i.Item(text="Минимум:", var=var_list["lambda2_min"], value=1),
            i.Item(text="Максимум:", var=var_list["lambda2_max"], value=3),
        ], [
            i.Item(text="Минимум:", var=var_list["mu_min"], value=5),
            i.Item(text="Максимум:", var=var_list["mu_max"], value=10),
        ], [
            i.Item(text="Минимум:", var=var_list["mu_disp_min"], value=0.7),
            i.Item(text="Максимум:", var=var_list["mu_disp_max"], value=0.9),
        ]
    ]

    ilist = [
        i.InputList(master=frame_inputs, items=items[0], title="Интенсивность поступления 1"),
        i.InputList(master=frame_inputs, items=items[1], title="Интенсивность поступления 2"),
        i.InputList(master=frame_inputs, items=items[2], title="Интенсивность обработки"),
        i.InputList(master=frame_inputs, items=items[3], title="Разброс генератора"),
    ]
    list(map(lambda x: x.pack(side=LEFT, padx=5), ilist))

    btn = Button(root, text="Запуск")
    btn.bind("<Button-1>", work_ffe)

    ilist_0.grid(column=1, padx=5)
    frame_inputs.grid(column=1)
    btn.grid(column=1, padx=5, pady=5)


def add_new_exp(root):
    items = [
        i.Item(text="Интенсивность поступления заявок №1:", var=var_list["lambda"], value=2),
        i.Item(text="Интенсивность поступления заявок №2:", var=var_list["lambda2"], value=2),
        i.Item(text="Интенсивность обслуживания заявок:", var=var_list["mu"], value=7.5),
        i.Item(text="Дисперсия обслуживания заявок", var=var_list["mu_disp"], value=0.8),
    ]
    ilist = i.InputList(master=root, items=items, title="Добавление точки факторного пространства")
    ilist.grid(column=1)

    btn = Button(root, text="Добавить точку", state=DISABLED)
    btn.configure(bg=BG, fg=FG, activebackground=FG, activeforeground=BG)
    btn.bind("<Button-1>", work_single_exp)
    btn.grid(column=1, padx=10, pady=10)
    btn.config(state="disabled")

    return btn


if __name__ == '__main__':
    f_ffe = Frame(root, highlightbackground="grey", highlightthickness=1)
    f_one = Frame(root, highlightbackground="grey", highlightthickness=1)

    add_ffe_inputs(f_ffe)
    btn_add_exp = add_new_exp(f_one)

    sep = ttk.Separator(root, orient='horizontal')
    sep.place(x=0, y=175, relwidth=1)
    sty = ttk.Style(root)
    sty.configure("TSeparator", background="red")

    f_ffe.grid(row=0, column=0)
    f_one.grid(row=0, column=1)

    ffe_results_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    root.mainloop()
