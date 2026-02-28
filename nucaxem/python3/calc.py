import tkinter as tk
from tkinter import ttk
import math

class Calculator:
    def __init__(self):
        self.win = tk.Tk()
        self.win.title("Scientific Calculator")
        self.win.resizable(0, 0)
        self.win.geometry("400x550")
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.win)
        self.tab_std = ttk.Frame(self.notebook)
        self.tab_sci = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_std, text="Standard")
        self.notebook.add(self.tab_sci, text="Scientific")
        self.notebook.pack(expand=1, fill="both")

        # Display entry (shared)
        self.entry = tk.Entry(self.win, font=('Arial', 18), bd=10, relief=tk.RIDGE, justify='right')
        self.entry.insert(0, "0")
        self.entry.pack(fill="x")

        # State variables
        self.expression = ""
        self.memory = 0.0
        self.deg_mode = True  # True = degrees, False = radians

        # Layout buttons on each tab
        self.create_standard_buttons()
        self.create_scientific_buttons()

    def append(self, text):
        if self.entry.get() == "0" and text not in (".", "+", "-", "*", "/"):
            self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, text)

    def clear_all(self):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, "0")
        self.expression = ""

    def clear_entry(self):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, "0")

    def backspace(self):
        txt = self.entry.get()
        if len(txt) > 1:
            new = txt[:-1]
        else:
            new = "0"
        self.entry.delete(0, tk.END)
        self.entry.insert(0, new)

    def toggle_sign(self):
        txt = self.entry.get()
        if txt.startswith('-'):
            self.entry.delete(0)
        else:
            if txt != "0":
                self.entry.insert(0, '-')

    def set_memory(self):
        try:
            self.memory = float(self.entry.get().replace(',', '.'))
        except:
            pass

    def recall_memory(self):
        val = str(self.memory).replace('.', ',')
        self.entry.delete(0, tk.END)
        self.entry.insert(0, val)

    def clear_memory(self):
        self.memory = 0.0

    def evaluate(self):
        expr = self.entry.get().replace(',', '.')
        try:
            # Replace 'EE' or 'EXP' if needed
            expr = expr.replace('EE', 'e').replace('EXP', 'e')
            result = eval(expr)
            result_str = str(result)
            # Format output with comma
            if '.' in result_str:
                result_str = result_str.rstrip('0').rstrip('.')
            self.entry.delete(0, tk.END)
            self.entry.insert(0, result_str.replace('.', ','))
        except Exception:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, "Error")

    def insert_math_function(self, func):
        txt = self.entry.get().replace(',', '.')
        try:
            value = float(txt)
            if func == 'sqrt':
                res = math.sqrt(value)
            elif func == 'percent':
                res = value / 100.0
            elif func == 'reciprocal':
                res = 1.0 / value
            # Trig
            elif func == 'sin':
                angle = math.radians(value) if self.deg_mode else value
                res = math.sin(angle)
            elif func == 'cos':
                angle = math.radians(value) if self.deg_mode else value
                res = math.cos(angle)
            elif func == 'tan':
                angle = math.radians(value) if self.deg_mode else value
                res = math.tan(angle)
            elif func == 'asin':
                res = math.degrees(math.asin(value)) if self.deg_mode else math.asin(value)
            elif func == 'acos':
                res = math.degrees(math.acos(value)) if self.deg_mode else math.acos(value)
            elif func == 'atan':
                res = math.degrees(math.atan(value)) if self.deg_mode else math.atan(value)
            # Logarithms
            elif func == 'log10':
                res = math.log10(value)
            elif func == 'ln':
                res = math.log(value)
            # Exponentials
            elif func == 'exp':
                res = math.exp(value)
            # Square
            elif func == 'square':
                res = value * value
            else:
                return
            res_str = str(res)
            if '.' in res_str:
                res_str = res_str.rstrip('0').rstrip('.')
            self.entry.delete(0, tk.END)
            self.entry.insert(0, res_str.replace('.', ','))
        except Exception:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, "Error")

    def toggle_mode(self):
        self.deg_mode = not self.deg_mode

    def create_button(self, parent, text, row, col, cmd, width=5):
        btn = tk.Button(parent, text=text, width=width, height=2, font=('Arial', 14), command=cmd)
        btn.grid(row=row, column=col, padx=2, pady=2)

    def create_standard_buttons(self):
        frame = ttk.Frame(self.tab_std)
        frame.pack()
        # First row: MC, MR, MS, Backspace
        self.create_button(frame, "MC", 0, 0, self.clear_memory)
        self.create_button(frame, "MR", 0, 1, self.recall_memory)
        self.create_button(frame, "MS", 0, 2, self.set_memory)
        self.create_button(frame, "⌫", 0, 3, self.backspace)
        # Second row: 7,8,9, / 
        self.create_button(frame, "7", 1, 0, lambda: self.append("7"))
        self.create_button(frame, "8", 1, 1, lambda: self.append("8"))
        self.create_button(frame, "9", 1, 2, lambda: self.append("9"))
        self.create_button(frame, "÷", 1, 3, lambda: self.append("/"))
        # Third row: 4,5,6, * 
        self.create_button(frame, "4", 2, 0, lambda: self.append("4"))
        self.create_button(frame, "5", 2, 1, lambda: self.append("5"))
        self.create_button(frame, "6", 2, 2, lambda: self.append("6"))
        self.create_button(frame, "×", 2, 3, lambda: self.append("*"))
        # Fourth: 1,2,3, - 
        self.create_button(frame, "1", 3, 0, lambda: self.append("1"))
        self.create_button(frame, "2", 3, 1, lambda: self.append("2"))
        self.create_button(frame, "3", 3, 2, lambda: self.append("3"))
        self.create_button(frame, "−", 3, 3, lambda: self.append("-"))
        # Fifth: 0, ., =, +
        self.create_button(frame, "0", 4, 0, lambda: self.append("0"))
        self.create_button(frame, ",", 4, 1, lambda: self.append("."))
        self.create_button(frame, "=", 4, 2, self.evaluate, width=11)
        self.create_button(frame, "+", 4, 3, lambda: self.append("+"))
        # Sixth row: CE, C, ±, % (clear entry/all clear etc.)
        self.create_button(frame, "CE", 5, 0, self.clear_entry)
        self.create_button(frame, "C", 5, 1, self.clear_all)
        self.create_button(frame, "±", 5, 2, self.toggle_sign)
        self.create_button(frame, "%", 5, 3, lambda: self.insert_math_function('percent'))

    def create_scientific_buttons(self):
        frame = ttk.Frame(self.tab_sci)
        frame.pack()
        funcs = [
            ("√", 0, 0, lambda: self.insert_math_function('sqrt')),
            ("x²", 0, 1, lambda: self.insert_math_function('square')),
            ("1/x", 0, 2, lambda: self.insert_math_function('reciprocal')),
            ("xʸ", 0, 3, lambda: self.append("**")),
            ("(", 0, 4, lambda: self.append("(")),
            (")", 0, 5, lambda: self.append(")")),
            ("10ˣ", 1, 0, lambda: self.append("10**")),
            ("EXP", 1, 1, lambda: self.append("e")),  # uses e-notation
            ("π", 1, 2, lambda: self.append(str(math.pi))),
            ("e", 1, 3, lambda: self.append(str(math.e))),
            ("sin", 1, 4, lambda: self.insert_math_function('sin')),
            ("cos", 1, 5, lambda: self.insert_math_function('cos')),
            ("tan", 2, 0, lambda: self.insert_math_function('tan')),
            ("asin", 2, 1, lambda: self.insert_math_function('asin')),
            ("acos", 2, 2, lambda: self.insert_math_function('acos')),
            ("atan", 2, 3, lambda: self.insert_math_function('atan')),
            ("ln", 2, 4, lambda: self.insert_math_function('ln')),
            ("log₁₀", 2, 5, lambda: self.insert_math_function('log10')),
            ("eˣ", 3, 0, lambda: self.insert_math_function('exp')),
            ("DRG", 3, 1, self.toggle_mode),
        ]
        for (text, r, c, cmd) in funcs:
            self.create_button(frame, text, r, c, cmd)

    def run(self):
        self.win.mainloop()

# Run the calculator
if __name__ == "__main__":
    calc = Calculator()
    calc.run()
