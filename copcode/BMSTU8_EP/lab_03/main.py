
from tkinter import *
from tkinter import ttk
import tkinter as tk
import Input as i
from Table import Table
from functions import *
from PfeFrame import *
from DfeFrame import *
root = Tk()
nb = ttk.Notebook(root)
experiment = PfeFrame(nb)
dfe_experiment = DfeFrame(nb)
root.configure(background="white")


varList = {
    "lambda": StringVar(),
    "lambda2": StringVar(),
    "mu": StringVar(),
    "mu2": StringVar(),
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
    "mu2_min": StringVar(),
    "mu2_max": StringVar(),
}

def work_pfe(Event):
    try:
        lambda_min = float(varList["lambda_min"].get())
        lambda_max = float(varList["lambda_max"].get())
        mu_min = float(varList["mu_min"].get())
        mu_max = float(varList["mu_max"].get())
        lambda2_min = float(varList["lambda2_min"].get())
        lambda2_max = float(varList["lambda2_max"].get())
        mu2_min = float(varList["mu2_min"].get())
        mu2_max = float(varList["mu2_max"].get())
        count = float(varList["N"].get())
        experiment.run(
            lambda_min=lambda_min,
            lambda_max=lambda_max,
            mu_max=mu_max,
            mu_min=mu_min, 
            lambda2_min=lambda2_min,
            lambda2_max=lambda2_max,
            mu2_max=mu2_max,
            mu2_min=mu2_min, 
            count=count, 
        )      
        dfe_experiment.run(
            lambda_min=lambda_min,
            lambda_max=lambda_max,
            mu_max=mu_max,
            mu_min=mu_min, 
            lambda2_min=lambda2_min,
            lambda2_max=lambda2_max,
            mu2_max=mu2_max,
            mu2_min=mu2_min, 
            count=count, 
        )        
        add_button.config(state='normal')

    
    except ValueError:
        tk.messagebox.showinfo(title="error", message="Ошибка ввода параметров!")


def work_one(Event): 
    lam = float(varList["lambda"].get())
    lam2 = float(varList["lambda2"].get())
    mu = float(varList["mu"].get())
    mu2 = float(varList["mu2"].get())
    experiment.count_one(lam=lam, mu=mu, lam2=lam2, mu2=mu2)
    dfe_experiment.count_one(lam=lam, mu=mu,lam2=lam2, mu2=mu2)


def pfe_inputs(root):
    t = tk.Label(root, text="Эксперимент", background="white")
    t.grid(column=1)
    frame_inputs = Frame(root)
    items_1 = [
        i.Item(text="Минимум:", var=varList["lambda_min"], value=10), 
        i.Item(text="Максимум:", var=varList["lambda_max"], value=30), 
    ]
    items_2 = [
        i.Item(text="Минимум:", var=varList["lambda2_min"], value=10), 
        i.Item(text="Максимум:", var=varList["lambda2_max"], value=30), 
    ]
    items_3 = [
        i.Item(text="Минимум:", var=varList["mu_min"], value=95), 
        i.Item(text="Максимум:", var=varList["mu_max"], value=105), 
    ]
    items_4 = [
        i.Item(text="Минимум:", var=varList["mu2_min"], value=95), 
        i.Item(text="Максимум:", var=varList["mu2_max"], value=105), 
    ]
    i_list_1 = i.InputList(master=frame_inputs, items=items_1, title="Интенсивность поступления заявок 1")
    i_list_2 = i.InputList(master=frame_inputs, items=items_2, title="Интенсивность поступления заявок 2")
    i_list_3 = i.InputList(master=frame_inputs, items=items_3, title="Интенсивность обработки заявок 1")
    i_list_4 = i.InputList(master=frame_inputs, items=items_4, title="Интенсивность обработки заявок 2")

    i_list_1.pack(side=LEFT, padx=10)
    i_list_2.pack(side=LEFT,  padx=10)
    i_list_3.pack(side=LEFT,  padx=10)
    i_list_4.pack(side=LEFT,  padx=10)

    frame_inputs.grid(column=1)

    items_4 = [
        i.Item(text="Число заявок:", var=varList["N"], value=5000), 
    ]

    i_list_5 = i.InputList(master=root, items=items_4)
    i_list_5.grid(column=1,  padx=10)

    btn = Button(root, text="Запуск", background="white")
    btn.bind("<Button-1>", work_pfe)
      
    btn.grid(column=1, padx=10, pady=10) 

def draw_new_point(root):
    items = [
        i.Item(text="Интенсивность поступления заявок 1:", var=varList["lambda"], value=15),
        i.Item(text="Интенсивность поступления заявок 2:", var=varList["lambda2"], value=15),
        i.Item(text="Интенсивность обслуживания заявок 1:", var=varList["mu"], value=100),
        i.Item(text="Интенсивность обслуживания заявок 2:", var=varList["mu2"], value=100),
    ]
    i_list = i.InputList(master=root, items=items, title="Добавление точки факторного пространства")
    i_list.grid(column=1)

    btn = Button(root, text="Добавить", state=DISABLED, background="white")
    btn.bind("<Button-1>", work_one)       
    btn.grid(column=1, padx=10, pady=10)
    btn.config(state="disabled")
    return btn

def work_view(Event):
    view(
        start=float(varList["start"].get()), 
        end=float(varList["end"].get()), 
        N=float(varList["N_exp"].get())
    )

def expirement_list(root): 
    items = [
        i.Item(text="От:", var=varList["start"], value=0.01), 
        i.Item(text="До:", var=varList["end"], value=1.1), 
        i.Item(text="Число заявок:", var=varList["N_exp"], value=1000)
    ]

    i_list = i.InputList(master=root, items=items)
    i_list.grid(column=1)

    btn2 = Button(root, text="Запуск")
    btn2.bind("<Button-1>", work_view)       
    btn2.grid(column=1, padx=10, pady=10) 

if __name__ == '__main__':
    f_view = Frame(root, highlightbackground="white", highlightthickness=1)

    # expirement_list(f_view)

    f_view.grid(row=0, column=3,  padx=10, pady=10)
  

    f_pfe = Frame(root, highlightbackground="white", highlightthickness=1)
    f_one = Frame(root, highlightbackground="white", highlightthickness=1)
    pfe_inputs(f_pfe)
    add_button = draw_new_point(f_one)
    f_pfe.grid(row=0, column=0)
    f_one.grid(row=0, column=1)
    nb.grid(row=1, columnspan=2)

    # experiment.grid(row=1, column=0, columnspan=2,   padx=5, pady=5)
    # dfe_experiment.grid(row=2, column=0, columnspan=2,   padx=5, pady=5)

    nb.add(experiment, text='ПФЭ') 
    nb.add(dfe_experiment, text='ДФЭ')
    root.mainloop()
    

    