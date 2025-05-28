import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import re
import csv

# Token specification
KEYWORDS = {
    "auto", "break", "case", "char", "const", "continue", "default", "do", "double",
    "else", "enum", "extern", "float", "for", "goto", "if", "int", "long", "register",
    "return", "short", "signed", "sizeof", "static", "struct", "switch", "typedef",
    "union", "unsigned", "void", "volatile", "while"
}

TOKEN_SPEC = [
    ('COMMENT', r'//.*?$|/\*.*?\*/'),
    ('STRING', r'"(?:\\.|[^"\\])*"'),
    ('CHAR', r"'(?:\\.|[^'\\])'"),
    ('NUMBER', r'\b\d+(\.\d+)?\b'),
    ('IDENTIFIER', r'\b[A-Za-z_]\w*\b'),
    ('OPERATOR', r'[+\-*/%=!<>]=?|&&|\|\|'),
    ('DELIMITER', r'[;,\[\](){}]'),
    ('SKIP', r'[ \t\n]+'),
    ('MISMATCH', r'.'),
]

TOK_REGEX = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPEC)
TOKEN_RE = re.compile(TOK_REGEX, re.DOTALL | re.MULTILINE)

def analyze_code(code):
    tokens = []
    for match in TOKEN_RE.finditer(code):
        kind = match.lastgroup
        value = match.group()
        if kind == 'SKIP':
            continue
        elif kind == 'IDENTIFIER' and value in KEYWORDS:
            kind = 'KEYWORD'
        elif kind == 'MISMATCH':
            kind = 'UNKNOWN'
        tokens.append((kind, value))
    return tokens

class LexicalAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Lexical Analyzer - Mini C Compiler")
        self.root.geometry("1000x700")
        self.dark_mode = False

        self.setup_gui()
        self.set_light_mode()

    def setup_gui(self):
        # File controls
        file_frame = tk.Frame(self.root)
        file_frame.pack(pady=10)

        tk.Button(file_frame, text="Load C File", command=self.load_file, bg="green", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(file_frame, text="Analyze Code", command=self.run_analysis, bg="blue", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(file_frame, text="Export Tokens", command=self.export_tokens, bg="purple", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(file_frame, text="Toggle Theme", command=self.toggle_theme, bg="gray", fg="white").pack(side=tk.LEFT, padx=10)

        # Code display
        self.code_display = scrolledtext.ScrolledText(self.root, height=15, width=120, font=("Consolas", 12))
        self.code_display.pack(pady=10)

        # Token result display
        self.token_list = tk.Listbox(self.root, height=20, width=120, font=("Courier", 11))
        self.token_list.pack(pady=10)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("C Files", "*.c"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'r') as f:
                code = f.read()
            self.code_display.delete("1.0", tk.END)
            self.code_display.insert(tk.END, code)

    def run_analysis(self):
        code = self.code_display.get("1.0", tk.END)
        tokens = analyze_code(code)
        self.token_list.delete(0, tk.END)
        for tok_type, tok_value in tokens:
            self.token_list.insert(tk.END, f"{tok_type:<15} | {tok_value}")
        messagebox.showinfo("Lexical Analysis Complete", f"{len(tokens)} tokens identified.")

    def export_tokens(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filepath:
            with open(filepath, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Token Type", "Token Value"])
                for i in range(self.token_list.size()):
                    line = self.token_list.get(i)
                    tok_type, tok_value = line.split('|', 1)
                    writer.writerow([tok_type.strip(), tok_value.strip()])
            messagebox.showinfo("Export Successful", f"Tokens saved to: {filepath}")

    def toggle_theme(self):
        if self.dark_mode:
            self.set_light_mode()
        else:
            self.set_dark_mode()

    def set_light_mode(self):
        self.dark_mode = False
        bg_color = "white"
        fg_color = "black"
        self.code_display.config(bg=bg_color, fg=fg_color, insertbackground=fg_color)
        self.token_list.config(bg=bg_color, fg=fg_color)

    def set_dark_mode(self):
        self.dark_mode = True
        bg_color = "#1e1e1e"
        fg_color = "white"
        self.code_display.config(bg=bg_color, fg=fg_color, insertbackground=fg_color)
        self.token_list.config(bg=bg_color, fg=fg_color)

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = LexicalAnalyzerGUI(root)
    root.mainloop()
