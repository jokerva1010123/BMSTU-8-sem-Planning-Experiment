from tkinter import *
import tkinter as tk
from tkinter.ttk import Separator, Style

import gui.input as i
from gui.frame import FrameFFE


BG = "#FFFFFF"
FG = "#000000"

root = Tk()
root.title("ExpPlanning lab_02")
ffe_results_frame = FrameFFE(root)

var_list = {
    "lambda": StringVar(),
    "mu": StringVar(),
    "mu_disp": StringVar(),
    "k": StringVar(),
    "N": StringVar(),
    "start": StringVar(),
    "end": StringVar(),
    "N_exp": StringVar(),
    "lambda_min": StringVar(),
    "lambda_max": StringVar(),
    "mu_min": StringVar(),
    "mu_max": StringVar(),
    "mu_disp_min": StringVar(),
    "mu_disp_max": StringVar(),
}


def work_ffe(_Event):
    try:
        lambda_min = float(var_list["lambda_min"].get())
        lambda_max = float(var_list["lambda_max"].get())
        mu_min = float(var_list["mu_min"].get())
        mu_max = float(var_list["mu_max"].get())
        mu_disp_min = float(var_list["mu_disp_min"].get())
        mu_disp_max = float(var_list["mu_disp_max"].get())
        count = float(var_list["N"].get())
        ffe_results_frame.run_ffe(
            lambda_min=lambda_min,
            lambda_max=lambda_max,
            mu_max=mu_max,
            mu_min=mu_min,
            count=count,
            disp_min=mu_disp_min,
            disp_max=mu_disp_max
        )

        btn_add_exp.config(state='normal')
    except ValueError:
        tk.messagebox.showerror(title="error", message="Ошибка ввода параметров!")


def work_single_exp(_Event):
    lam = float(var_list["lambda"].get())
    mu = float(var_list["mu"].get())
    mu_disp = float(var_list["mu_disp"].get())
    ffe_results_frame.count_one(lam=lam, mu=mu, disp=mu_disp)


def add_ffe_inputs(root):
    frame_inputs = Frame(root)
    item_n_requests = ( 
        i.Item(text="Число заявок:", var=var_list["N"], value=1000),
    )
    ilist_nreq = i.InputList(master=root, items=item_n_requests)
    ilist_nreq.grid(column=1,  padx=10, pady=10)

    items = [(
            i.Item(text="Инт. генерации (min):", var=var_list["lambda_min"], value=1),
            i.Item(text="Инт. генерации (max):", var=var_list["lambda_max"], value=3),
        ), (
            i.Item(text="Инт. обслуживания (min):", var=var_list["mu_min"], value=5),
            i.Item(text="Инт. обслуживания (max):", var=var_list["mu_max"], value=10),
        ), (
            i.Item(text="Дисперсия обслуживания (min):", var=var_list["mu_disp_min"], value=0.01),
            i.Item(text="Дисперсия обслуживания (max):", var=var_list["mu_disp_max"], value=0.1),
        ),
    ]

    ilists = [i.InputList(master=frame_inputs, items=item) for item in items]
    list(map(lambda x: x.pack(side=LEFT, padx=10, pady=10), ilists))
    frame_inputs.grid(column=1)

    btn = Button(root, text="Запустить")
    btn.configure(bg=BG, fg=FG, activebackground=FG, activeforeground=BG)
    btn.bind("<Button-1>", work_ffe)
    btn.grid(column=1, padx=10, pady=10)


def add_new_exp(root):
    items = [
        i.Item(text="Интенсивность поступления заявок:", var=var_list["lambda"], value=2),
        i.Item(text="Интенсивность обслуживания заявок:", var=var_list["mu"], value=7.5),
        i.Item(text="Дисперсия обслуживания заявок", var=var_list["mu_disp"], value=0.055),
    ]
    ilist = i.InputList(master=root, items=items)
    ilist.grid(column=1)

    btn = Button(root, text="Рассчитать", state=DISABLED)
    btn.configure(bg=BG, fg=FG, activebackground=FG, activeforeground=BG)
    btn.bind("<Button-1>", work_single_exp)
    btn.grid(column=1, padx=10, pady=10)
    btn.config(state="disabled")

    return btn


if __name__ == '__main__':
    ffe_inputs_frame = Frame(root)
    btn_add_exp = add_new_exp(ffe_inputs_frame)

    sep = Separator(ffe_inputs_frame, orient='horizontal')
    sep.place(x=0, y=120, relwidth=1)
    sty = Style(ffe_inputs_frame)
    sty.configure("TSeparator", background="red")

    add_ffe_inputs(ffe_inputs_frame)
    ffe_inputs_frame.pack()

    ffe_results_frame.pack()

    root.mainloop()
