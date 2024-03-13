
from operator import imod
from tkinter import * 
from tkinter import messagebox
import Input as i
from functions import *
from Constants import *
root = Tk()


varList = {
    "lambda": StringVar(),
    "mu": StringVar(),
    "k": StringVar(), 
    "N": StringVar(), 
    "start": StringVar(), 
    "end": StringVar(),
    "N_exp": StringVar(), 
    "start1": StringVar(), 
    "end1": StringVar(),
    "N_exp1": StringVar(), 

}

def work_proc(Event):

    result = modelling(
        clients_number=float(varList["N"].get())+1000,
        clients_proccessed=float(varList["N"].get()),
        lambda_coming=float(varList["lambda"].get()),
        lambda_obr=float(varList["mu"].get())
    )

    workload = float(varList["lambda"].get())/float(varList["mu"].get())

    messagebox.showinfo(title="Результаты", 
            message="Загрузка системы(расчетная): {:.4f}\nВремя работы:{:.4f} \nСреднее время ожидания: {:.4f}"
                        .format(workload, result['time'],result['wait_time_middle']))

def work_view(Event):
    view(
        start=float(varList["start"].get()), 
        end=float(varList["end"].get()), 
        N=float(varList["N_exp"].get())
    )

def work_a(Event):
    view1(
        start=float(varList["start1"].get()), 
        end=float(varList["end1"].get()), 
        N=float(varList["N_exp1"].get())
    )


def one_model_list(root):
    items = [
        i.Item(text="Интенсивность поступления заявок:", var=varList["lambda"], value=10),
        i.Item(text="Интенсивность обслуживания заявок:", var=varList["mu"], value=15),
        i.Item(text="Число заявок:", var=varList["N"], value=1000),
    ]
    i_list = i.InputList(master=root, items=items)
    i_list.grid(column=1)

    btn = Button(root, text="Запуск")
    btn.bind("<Button-1>", work_proc)       
    btn.configure(font=FONT)
    btn.grid(column=1, padx=10, pady=10)                          


def expirement_list(root): 
    items = [
        i.Item(text="От:", var=varList["start"], value=0.01), 
        i.Item(text="До:", var=varList["end"], value=1.0), 
        i.Item(text="Число заявок:", var=varList["N_exp"], value=1000)
    ]

    i_list = i.InputList(master=root, items=items)
    i_list.grid(column=1)

    btn2 = Button(root, text="Запуск")
    btn2.configure(font=FONT)
    btn2.bind("<Button-1>", work_view)       
    btn2.grid(column=1, padx=10, pady=10)  

def a(root):
    items = [
        i.Item(text="От:", var=varList["start1"], value=0.1), 
        i.Item(text="До:", var=varList["end1"], value=1.0), 
        i.Item(text="Число заявок:", var=varList["N_exp1"], value=1000)
    ]

    i_list = i.InputList(master=root, items=items)
    i_list.grid(column=2)

    btn2 = Button(root, text="Запуск")
    btn2.configure(font=FONT)
    btn2.bind("<Button-1>", work_a)       
    btn2.grid(column=2, padx=10, pady=10)  


if __name__ == '__main__':
    root.title("Планирования эксперимента лабораторная работа 1")
    root.geometry('600x400')
    root.configure(background=MAIN_COLOR)
    f_proc = Frame(root)
    f_view = Frame(root)
    f_a = Frame(root)

    one_model_list(f_proc)
    expirement_list(f_view)
    a(f_a)

    f_proc.configure(background=MAIN_COLOR)
    f_view.configure(background=MAIN_COLOR)
    f_a.configure(background=MAIN_COLOR)

    f_proc.pack()
    f_view.pack()
    f_a.pack()

    root.mainloop()
    
