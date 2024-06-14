import tkinter as tk


class Item:
    def __init__(self, text, var, value=0):
        self.text = text
        self.var = var
        self.value = value


class InputList(tk.Frame):
    def __init__(self, master, items=(), bg="#FFFFFF", fg="#000000", title=None):
        super().__init__(master)
        # self.configure(bg=bg)

        i = 0
        if title is not None:
            t = tk.Label(self, text=title)
            t.grid(row=i, column=0, columnspan=2, padx=5, pady=5)
            i += 1
        for item in items: 
            label = tk.Label(self, text=item.text, bg=bg, fg=fg)
            label.grid(row=i, column=0, sticky="e")

            entry = tk.Entry(self, width=10, textvariable=item.var, bg=bg, fg=fg)
            entry.grid(row=i, column=1)
            entry.insert(0, str(item.value))

            i += 1
