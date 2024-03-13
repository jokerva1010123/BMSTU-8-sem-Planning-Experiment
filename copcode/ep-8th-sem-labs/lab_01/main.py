from tkinter import *

import input
import utils

root = Tk()

varList = {
    "freq1": StringVar(),
    "freq2": StringVar(),
    "basefreq": StringVar(),
    "standdev": StringVar(),
    "standdev_exp": StringVar(),
    "N": StringVar(),
    "start": StringVar(),
    "end": StringVar(),
    "N_exp": StringVar(),
    "exp_amount": StringVar()
}


def work_view(Event):
    utils.view(
        start=float(varList["start"].get()),
        end=float(varList["end"].get()),
        N=float(varList["N_exp"].get()),
        freq=float(varList["freq2"].get()),
        standdev=float(varList["standdev_exp"].get()),
        exp_amount=int(varList["exp_amount"].get())
    )


def expirement_list(root):
    items = [
        input.Item(text="От:", var=varList["start"], value=0.01),
        input.Item(text="До:", var=varList["end"], value=1.0),
        input.Item(text="Интенсивность поступления заявок (равномерный):",
                   var=varList["freq1"], value=10),
        input.Item(text="Интенсивность обслуживания заявок (Вейбулла):",
                   var=varList["freq2"], value=1.0),
        input.Item(text="СКО поступления:", var=varList["standdev_exp"], value=1.0),
        input.Item(text="Число заявок:", var=varList["N_exp"], value=1000),
        input.Item(text="Число экспериментов:", var=varList["exp_amount"], value=100)
    ]

    i_list = input.InputList(master=root, items=items)
    i_list.grid(column=1)

    btn2 = Button(root, text="Старт")
    btn2.configure(font=18)
    btn2.bind("<Button-1>", work_view)
    btn2.grid(column=1, padx=10, pady=10)


if __name__ == '__main__':
    root.title("Планирование эксперимента, ЛР1")
    root.geometry('600x300')
    f_view = Frame(root)
    expirement_list(f_view)
    f_view.pack()
    root.mainloop()
