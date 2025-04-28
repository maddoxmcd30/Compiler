import re
import tkinter as tk
from tkinter import scrolledtext

class Analyzer:
    def __init__(self, code_string):
        self.code_string = code_string

    def lexeme_identifier(self):
        pypattern = r"\d+\.\d+|\d+|\".*?\"|\'.*?\'|\w+|<=|>=|==|!=|[-+*/=(){}\[\]:,;<>]"
        lexemes_with_lines = []
        lines = self.code_string.split('\n')
        for i, line in enumerate(lines, start=1):
            indent = len(line) - len(line.lstrip(' '))  # Number of leading spaces
            matches = re.findall(pypattern, line)
            for lex in matches:
                lexemes_with_lines.append((i, indent, lex))  # Save line number, indent, and lexeme
        return lexemes_with_lines

    def analyze(self):
        lexemes = self.lexeme_identifier()

        keywords = {"def", "print", "println", "class", "int", "float", "public", "static", "void", "main", "if", "elif", "else"}
        operators = {"+", "-", "*", "/", "="}
        comparators = {"<", ">", "<=", ">=", "==", "!="}
        separators = {"(", ")", "{", "}", "]", "[", ",", ":", ";"}

        tokens = []

        for line_num, indent, lexeme in lexemes:
            if lexeme in keywords:
                token_type = "KEYWORD"
            elif lexeme in comparators:
                token_type = "COMPARATOR"
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

            tokens.append((lexeme, token_type, line_num, indent))

        return tokens

class Parser:
    def __init__(self, input_box, output_box):
        self.input_box = input_box
        self.output_box = output_box

    def output(self, message):
        self.output_box.config(state='normal')
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, message)
        self.output_box.config(state='disabled')


    def parse(self):
        an = Analyzer(self.input_box.get("1.0", tk.END))
        tokens = an.analyze()

        if not tokens:
            self.output("No code to parse.")
            return

        i = 0
        while i < len(tokens):
            lexeme, token_type, line_num, indent = tokens[i]

            if lexeme == "if" or lexeme == "elif" or lexeme == "else":
                if_block = []
                start_indent = indent
                comparison = False
                # Expect ":" at the end of the condition
                while i < len(tokens):
                    if tokens[i][0] == ":":
                        i += 1
                        break
                    if tokens[i][2] != line_num:
                        self.output(f"Line {line_num}: Expected ':' at end of {lexeme} statement")
                        return
                    if tokens[i][1] == "COMPARATOR" or lexeme == "else":
                        comparison = True
                    i += 1
                if not comparison:
                    self.output(f"Line {line_num}: Expected comparative expression")
                    return
                # Now expect an indented block
                if i >= len(tokens):
                    self.output(f"Line {line_num}: Expected indented block after ':'")
                    return

                next_indent = tokens[i][3]
                if next_indent <= start_indent:
                    self.output(f"Line {tokens[i][2]}: Expected increased indentation after ':'")
                    return

                # Parse the indented block
                while i < len(tokens):
                    current_lexeme, current_type, current_line, current_indent = tokens[i]

                    if current_indent < next_indent:
                        # Block ended
                        break
                    if current_indent != next_indent:
                        self.output(f"Line {current_line}: Inconsistent indentation inside block")
                        return
                    if_block.append((current_lexeme, current_type, current_line))
                    i += 1

            else:
                # Handle simple expressions like x = 3 + 4
                if token_type == "IDENTIFIER":
                    if i + 1 < len(tokens) and tokens[i + 1][0] == "=":
                        # Assignment found
                        i += 2
                        while i < len(tokens) and tokens[i][2] == line_num:
                            i += 1
                    else:
                        self.output(f"Line {line_num}: Expected '=' after identifier")
                        return
                else:
                    i += 1

        self.output("Parsing Successful: No syntax errors detected!")

# GUI setup
window = tk.Tk()
window.title("Lexical Analyzer and Parser")
window.geometry("1000x700")

tk.Label(window, text="Enter your code below:").pack()

# Frame for text boxes
f = tk.Frame(window)
f.pack(pady=10)

# Input and output text boxes inside the frame
code_input = scrolledtext.ScrolledText(f, width=50, height=30)
code_input.pack(side='left', padx=5)

code_output = scrolledtext.ScrolledText(f, width=50, height=30)
code_output.pack(side='left', padx=5)
code_output.config(state='disabled')

# Create analyzer object with references to input/output
pr = Parser(code_input, code_output)

# Analyze button
analyze_btn = tk.Button(window, text="Analyze", command=pr.parse)
analyze_btn.pack(side='bottom')

window.mainloop()
