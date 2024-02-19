import tkinter as tk

class Table(tk.Frame): 
    def __init__(self, master, rows, columns): 
        super().__init__(master)
        self.array = []
        self.rows = rows
        self.columns = columns
        for i in range(rows):
            self.array.append([])
            for j in range(columns):
                self.array[i].append(tk.Entry(self, width=10))
                self.array[i][j].grid(row=i, column=j)

    def set(self, i, j, val): 
        if (i >= self.rows) or (j >= self.columns):
            return
        self.array[i][j].delete(0, tk.END)
        try:
            float(val)
            val = str('{:10.3g}'.format(val))
        except ValueError:
            pass
        self.array[i][j].insert(0, str(val))

    def set_row(self, index, row, start=0):
        for i in range(start, self.columns):
            if (len(row) == i-start):
                break
            self.array[index][i].delete(0, tk.END)
            val = row[i-start]
            try:
                float(val)
                val = str('{:10.3g}'.format(val))
            except ValueError:
                pass
            self.array[index][i].insert(0, str(val))
    
    def set_column(self, index, column, start=1):
        for i in range(start, self.rows): 
            if (len(column) == i-start):
                break
            val = column[i-start]
            try:
                float(val)
                val = str('{:10.3g}'.format(val))
            except ValueError:
                pass
            self.array[i][index].delete(0, tk.END)
            self.array[i][index].insert(0, str(val))
        
        
