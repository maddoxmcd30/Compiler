# Maddox McDaniel
# Concepts of Programming Languages
# Semester project

import re
import tkinter as tk
from tkinter import scrolledtext, messagebox


class Analyzer:
    def __init__(self, input_box, output_box):
        self.input_box = input_box
        self.output_box = output_box

    def py_anal(self):
        code = self.input_box.get("1.0", tk.END)
        pypattern = r"\w+"
        tokens = re.findall(pypattern, code)

        # Update output box
        self.output_box.config(state='normal')
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, "Tokens:\n" + "\n".join(tokens))
        self.output_box.config(state='disabled')


# GUI setup
window = tk.Tk()
window.title("Lexical Analyzer")
window.geometry("1000x400")

tk.Label(window, text="Enter your code below:").pack()

# Frame for text boxes
f = tk.Frame(window)
f.pack(pady=10)

# Input and output text boxes inside the frame
code_input = scrolledtext.ScrolledText(f, width=50, height=15)
code_input.pack(side='left', padx=5)

code_output = scrolledtext.ScrolledText(f, width=50, height=15)
code_output.pack(side='left', padx=5)
code_output.config(state='disabled')

# Create analyzer object with references to input/output
an = Analyzer(code_input, code_output)

# Analyze button
analyze_btn = tk.Button(window, text="Analyze", command=an.py_anal)
analyze_btn.pack(side='bottom')

window.mainloop()
