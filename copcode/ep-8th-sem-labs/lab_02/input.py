import tkinter as tk


class Item:
    def __init__(self, text, var, value=0):
        self.text = text
        self.var = var
        self.value = value


class InputList(tk.Frame):
    def __init__(self, master, items=[]):
        super().__init__(master)
        i = 0
        for item in items:
            label = tk.Label(self, text=item.text)
            label.grid(row=i, column=0, sticky="e")
            label.configure(font=18)
            entry = tk.Entry(self, width=10, textvariable=item.var)
            entry.configure(font=18)
            entry.grid(row=i, column=1)
            entry.insert(0, str(item.value))
            i += 1
