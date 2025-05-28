import re
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from ttkthemes import ThemedTk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt

KEYWORDS = {"int", "float", "char", "double", "if", "else", "while", "for", "return", "void", "main"}

def check_syntax(code):
    errors = []
    if code.count('{') != code.count('}'):
        errors.append("Unbalanced curly braces.")
    if code.count('(') != code.count(')'):
        errors.append("Unbalanced parentheses.")
    if code.count('"') % 2 != 0:
        errors.append("Unbalanced double quotes.")
    if code.count("'") % 2 != 0:
        errors.append("Unbalanced single quotes.")

    lines = code.splitlines()
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped and not stripped.endswith(';') and re.match(r"^(int|float|char|double|return|[a-zA-Z_][a-zA-Z0-9_]*)", stripped):
            if not (stripped.endswith('}') or stripped.endswith('{') or stripped.startswith('//') or stripped.startswith('#') or '(' in stripped):
                errors.append(f"Line {i+1}: Missing semicolon")
    return errors

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("C Files", "*.c"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, 'r') as file:
            code = file.read()
            code_area.delete(1.0, tk.END)
            code_area.insert(tk.END, code)
            apply_syntax_highlighting()

def analyze_syntax():
    code = code_area.get(1.0, tk.END)
    result_area.config(state='normal')
    result_area.delete(1.0, tk.END)
    errors = check_syntax(code)
    if errors:
        for error in errors:
            result_area.insert(tk.END, f"❌ {error}\n")
        status_bar.config(text=f"{len(errors)} error(s) found")
    else:
        result_area.insert(tk.END, "✅ No syntax errors found.\n")
        status_bar.config(text="Syntax analysis complete. No errors found.")
    result_area.config(state='disabled')

def apply_syntax_highlighting():
    code_area.tag_remove("keyword", "1.0", tk.END)
    for keyword in KEYWORDS:
        start = "1.0"
        while True:
            start = code_area.search(rf'\y{keyword}\y', start, stopindex=tk.END, regexp=True)
            if not start:
                break
            end = f"{start}+{len(keyword)}c"
            code_area.tag_add("keyword", start, end)
            start = end
    code_area.tag_config("keyword", foreground="blue")

def clear_all():
    code_area.delete(1.0, tk.END)
    result_area.config(state='normal')
    result_area.delete(1.0, tk.END)
    result_area.config(state='disabled')
    status_bar.config(text="Editor cleared.")

def toggle_theme():
    global is_dark
    is_dark = not is_dark
    bg = "#1e1e1e" if is_dark else "white"
    fg = "#dcdcdc" if is_dark else "black"
    code_area.config(bg=bg, fg=fg, insertbackground=fg)
    result_area.config(bg=bg, fg=fg)
    status_bar.config(bg="#444" if is_dark else "#eaeaea", fg=fg)
    theme_btn.config(text="☀️ Light Mode" if is_dark else "🌙 Dark Mode")

def generate_parse_tree():
    code = code_area.get(1.0, tk.END)
    lines = [line.strip() for line in code.splitlines() if line.strip()]

    G = nx.DiGraph()
    root = "Program"
    G.add_node(root)

    for i, line in enumerate(lines):
        if line.endswith(";"):
            line = line[:-1].strip()

        if re.match(r"^(int|float|char|double)\s+\w+$", line):  # Declaration
            decl_node = f"Declaration_{i+1}"
            G.add_edge(root, decl_node)

            parts = line.split()
            G.add_edge(decl_node, f"Type: {parts[0]}")
            G.add_edge(decl_node, f"Variable: {parts[1]}")

        elif "=" in line:  # Assignment
            assign_node = f"Assignment_{i+1}"
            G.add_edge(root, assign_node)

            var, expr = [x.strip() for x in line.split("=", 1)]
            G.add_edge(assign_node, f"Variable: {var}")
            G.add_edge(assign_node, f"Expression: {expr}")

        elif re.match(r"^(if|while|for)\s*\(.*\)", line):  # Control structures
            ctrl_type = line.split("(")[0].strip()
            ctrl_node = f"{ctrl_type.capitalize()}_{i+1}"
            G.add_edge(root, ctrl_node)

            condition = re.search(r"\((.*)\)", line)
            if condition:
                G.add_edge(ctrl_node, f"Condition: {condition.group(1)}")

        else:  # Generic statement
            stmt_node = f"Statement_{i+1}: {line}"
            G.add_edge(root, stmt_node)

    plt.figure(figsize=(14, 9))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_color="lightyellow", edge_color="gray",
            node_size=2500, font_size=10, font_weight="bold", arrows=True)
    plt.title("C Code Parse Tree", fontsize=14)
    plt.show()

# GUI Setup
app = ThemedTk(theme="arc")
app.title("C Syntax Analyzer with Parse Tree")
app.geometry("1000x700")

style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 10), padding=6)
style.configure("TLabel", font=("Segoe UI", 10))

frame = ttk.Frame(app, padding=10)
frame.pack(fill=tk.BOTH, expand=True)

# Code Input
ttk.Label(frame, text="Enter or Load C Code:").pack(anchor=tk.W)
code_area = ScrolledText(frame, height=18, font=("Consolas", 12), undo=True)
code_area.pack(fill=tk.BOTH, expand=True, pady=5)

# Buttons
button_frame = ttk.Frame(frame)
button_frame.pack(fill=tk.X, pady=8)

ttk.Button(button_frame, text="📂 Load File", command=load_file).pack(side=tk.LEFT, padx=5)
ttk.Button(button_frame, text="🔍 Analyze Syntax", command=analyze_syntax).pack(side=tk.LEFT, padx=5)
ttk.Button(button_frame, text="🌳 Generate Parse Tree", command=generate_parse_tree).pack(side=tk.LEFT, padx=5)
ttk.Button(button_frame, text="🧹 Clear All", command=clear_all).pack(side=tk.LEFT, padx=5)

is_dark = False
theme_btn = ttk.Button(button_frame, text="🌙 Dark Mode", command=toggle_theme)
theme_btn.pack(side=tk.RIGHT)

# Result Output
ttk.Label(frame, text="Syntax Analysis Results:").pack(anchor=tk.W, pady=(10, 0))
result_area = ScrolledText(frame, height=10, font=("Consolas", 11), state='disabled', foreground='darkred')
result_area.pack(fill=tk.BOTH, expand=True)

# Status bar
status_bar = tk.Label(app, text="Ready", anchor=tk.W, relief=tk.SUNKEN, font=("Segoe UI", 9))
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

app.mainloop()
