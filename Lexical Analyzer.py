# Maddox McDaniel
# Concepts of Programming Languages
# Semester project
# April 15, 2025

import re
import tkinter as tk
from tkinter import scrolledtext
import numpy as np


class Analyzer:
    def __init__(self, input_box, output_box):
        self.input_box = input_box
        self.output_box = output_box

    def lexeme_identifier(self):
        code = self.input_box.get("1.0", tk.END)
        pypattern = r"\d+\.\d+|\d+|\".*?\"|\'.*?\'|\w+|==|[-+*/=(){}\[\]:,;]"

        lexemes_with_lines = []
        lines = code.split('\n')
        for i, line in enumerate(lines, start=1):
            matches = re.findall(pypattern, line)
            for lex in matches:
                lexemes_with_lines.append((i, lex))
        return lexemes_with_lines

    def analyze(self):
        lexemes = self.lexeme_identifier()
        keywords = {"def", "print", "println", "class", "int", "float", "public", "static", "void", "main"}
        operators = {"+", "-", "*", "/", "=", "=="}
        separators = {"(", ")", "{", "}", "]", "[", ",", ":", ";"}

        output_lines = ["Tokens:"]
        error_lines = []
        to_save = []


        for line_num, lexeme in lexemes:
            errors = False
            if errors:
                output_lines.append(f"There was an error on Line {line_num}: Invalid token '{lexeme}'")
            else:

                if lexeme in keywords:
                    token_type = "KEYWORD"
                elif lexeme in operators:
                    token_type = "OPERATOR"
                elif lexeme in separators:
                    token_type = "SEPARATOR"
                elif re.fullmatch(r"\d+", lexeme):
                    token_type = "INT_LITERAL"
                elif re.fullmatch(r"\d+\.\d+", lexeme):
                    token_type = "FLOAT_LITERAL"
                elif re.fullmatch(r"\".*?\"|\'.*?\'", lexeme):
                    token_type = "STRING_LITERAL"
                elif re.fullmatch(r"[a-zA-Z_]\w*", lexeme):
                    token_type = "IDENTIFIER"
                else:
                    token_type = "UNKNOWN"
                    error_lines.append(f"Line {line_num}: Invalid token '{lexeme}'")

                output_lines.append(f"{lexeme}  →  {token_type} (Line {line_num})")
                to_save.append([lexeme,token_type,line_num])

        array = np.array(to_save,dtype=object)
        np.save('Analysis',array)
        np.savetxt('Analysis_txt', array, fmt="%s", delimiter=" ")
        # Display all output + errors
        final_output = "\n".join(output_lines)
        if error_lines:
            final_output += "\n\nErrors:\n" + "\n".join(error_lines)

        self.output_box.config(state='normal')
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, final_output)
        self.output_box.config(state='disabled')


# GUI setup
window = tk.Tk()
window.title("Lexical Analyzer")
window.geometry("1000x700")

tk.Label(window, text="Enter your code below:").pack()

# Frame for text boxes
f = tk.Frame(window)
f.pack(pady=10)

# Input and output text boxes inside the frame
code_input = scrolledtext.ScrolledText(f, width=50, height=30 )
code_input.pack(side='left', padx=5)

code_output = scrolledtext.ScrolledText(f, width=50, height=30)
code_output.pack(side='left', padx=5)
code_output.config(state='disabled')

# Create analyzer object with references to input/output
an = Analyzer(code_input, code_output)

# Analyze button
analyze_btn = tk.Button(window, text="Analyze", command=an.analyze)
analyze_btn.pack(side='bottom')

window.mainloop()
