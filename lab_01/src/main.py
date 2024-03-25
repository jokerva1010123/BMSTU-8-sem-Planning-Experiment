from tkinter import *

import input
import utils

root = Tk()

varList = {
    "N_exp": StringVar(),
    "exp_amount": StringVar()
}


def work_view(Event):
    utils.view(
        start=0.01,
        end=1.0,
        N=float(varList["N_exp"].get()),
        freq_gen=10.0,
        dev_gen=2.0,
        freq_proc=5.0,
        dev_proc=2.0,
        exp_amount=int(varList["exp_amount"].get())
    )


def expirement_list(root):
    items = [
        input.Item(text="Число заявок:", var=varList["N_exp"], value=500),
        input.Item(text="Число экспериментов:", var=varList["exp_amount"], value=50)
    ]

    i_list = input.InputList(master=root, items=items)
    i_list.grid(column=1)

    btn2 = Button(root, text="Старт")
    btn2.configure(font=18)
    btn2.bind("<Button-1>", work_view)
    btn2.grid(column=1, padx=10, pady=10)


if __name__ == '__main__':
    root.title("Lab 1")
    root.geometry('600x300')
    f_view = Frame(root)
    expirement_list(f_view)
    f_view.pack()
    root.mainloop()