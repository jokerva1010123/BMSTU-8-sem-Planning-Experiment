import tkinter as tk
from tkinter import *

import input
import pfe

root = Tk()
experiment = pfe.PfeFrame(root)

varList = {
    "lambda": StringVar(),
    "mu": StringVar(),
    "lambda_disp": StringVar(),
    "k": StringVar(),
    "N": StringVar(),
    "start": StringVar(),
    "end": StringVar(),
    "N_exp": StringVar(),
    "lambda_min": StringVar(),
    "lambda_max": StringVar(),
    "mu_min": StringVar(),
    "mu_max": StringVar(),
    "lambda_disp_min": StringVar(),
    "lambda_disp_max": StringVar(),
}


def work_pfe(Event):
    try:
        lambda_min = float(varList["lambda_min"].get())
        lambda_max = float(varList["lambda_max"].get())
        mu_min = float(varList["mu_min"].get())
        mu_max = float(varList["mu_max"].get())
        lambda_disp_min = float(varList["lambda_disp_min"].get())
        lambda_disp_max = float(varList["lambda_disp_max"].get())
        count = float(varList["N"].get())
        experiment.run(
            lambda_min=lambda_min,
            lambda_max=lambda_max,
            mu_max=mu_max,
            mu_min=mu_min,
            count=count,
            lambda_disp_min=lambda_disp_min,
            lambda_disp_max=lambda_disp_max
        )
        add_button.config(state='normal')
    except ValueError:
        tk.messagebox.showerror(title="error", message="Ошибка ввода параметров!")


def work_one(Event):
    lam = float(varList["lambda"].get())
    mu = float(varList["mu"].get())
    lambda_disp = float(varList["lambda_disp"].get())
    experiment.count_one(lam=lam, mu=mu, disp=lambda_disp)


def pfe_inputs(root):
    frame_inputs = Frame(root)
    items_1 = [
        input.Item(text="Lambda_min:", var=varList["lambda_min"], value=1),
        input.Item(text="Labmda_max:", var=varList["lambda_max"], value=10),
    ]
    items_2 = [
        input.Item(text="Mu_min:", var=varList["mu_min"], value=20),
        input.Item(text="Mu_max:", var=varList["mu_max"], value=100),
    ]
    items_3 = [
        input.Item(text="lambda_disp_min:", var=varList["lambda_disp_min"], value=0.01),
        input.Item(text="lambda_disp_max:", var=varList["lambda_disp_max"], value=0.1),
    ]
    i_list_1 = input.InputList(master=frame_inputs, items=items_1)
    i_list_2 = input.InputList(master=frame_inputs, items=items_2)
    i_list_3 = input.InputList(master=frame_inputs, items=items_3)

    i_list_1.pack(side=LEFT, padx=10, pady=10)
    i_list_2.pack(side=LEFT,  padx=10, pady=10)
    i_list_3.pack(side=LEFT,  padx=10, pady=10)

    frame_inputs.grid(column=1)

    items_4 = [
        input.Item(text="Число заявок:", var=varList["N"], value=1000),
    ]

    i_list_4 = input.InputList(master=root, items=items_4)
    i_list_4.grid(column=1,  padx=10, pady=10)

    btn = Button(root, text="Старт")
    btn.bind("<Button-1>", work_pfe)

    btn.grid(column=1, padx=10, pady=10)


def draw_new_point(root):
    items = [
        input.Item(text="Интенсивность поступления заявок:", var=varList["lambda"], value=10),
        input.Item(text="Дисперсия поступления заявок", var=varList["lambda_disp"], value=0.05),
        input.Item(text="Интенсивность обслуживания заявок:", var=varList["mu"], value=30),
    ]
    i_list = input.InputList(master=root, items=items)
    i_list.grid(column=1)

    btn = Button(root, text="Рассчитать", state=DISABLED)
    btn.bind("<Button-1>", work_one)
    btn.grid(column=1, padx=10, pady=10)
    btn.config(state="disabled")
    return btn


if __name__ == '__main__':
    f_pfe = Frame(root)
    pfe_inputs(f_pfe)
    add_button = draw_new_point(f_pfe)
    f_pfe.pack()

    experiment.pack()

    root.mainloop()
