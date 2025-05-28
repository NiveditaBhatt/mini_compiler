import tkinter as tk
from tkinter import filedialog, messagebox
import re

def optimize_code(code):
    lines = code.splitlines()
    optimized_lines = []

    for line in lines:
        stripped = line.strip()

        # Remove self assignments like x = x;
        if re.match(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*\1\s*;', stripped):
            continue

        # Constant folding for int declaration: int x = 2 + 3;
        const_decl = re.match(r'^\s*int\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*([0-9+\-*/\s]+);$', stripped)
        if const_decl:
            var, expr = const_decl.group(1), const_decl.group(2)
            try:
                value = eval(expr)
                optimized_lines.append(f"int {var} = {value};")
                continue
            except:
                pass

        # Constant folding for assignment: x = 2 + 3;
        const_assign = re.match(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*([0-9+\-*/\s]+);$', stripped)
        if const_assign:
            var, expr = const_assign.group(1), const_assign.group(2)
            try:
                value = eval(expr)
                optimized_lines.append(f"{var} = {value};")
                continue
            except:
                pass

        # Algebraic simplifications
        simplified = stripped

        # x = y + 0 or x = 0 + y → x = y;
        simplified = re.sub(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\+\s*0\s*;', r'\1 = \2;', simplified)
        simplified = re.sub(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*0\s*\+\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*;', r'\1 = \2;', simplified)

        # x = y - 0 → x = y;
        simplified = re.sub(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*-\s*0\s*;', r'\1 = \2;', simplified)

        # x = y * 1 or x = 1 * y → x = y;
        simplified = re.sub(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\*\s*1\s*;', r'\1 = \2;', simplified)
        simplified = re.sub(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*1\s*\*\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*;', r'\1 = \2;', simplified)

        # x = y * 0 or x = 0 * y → x = 0;
        simplified = re.sub(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\*\s*0\s*;', r'\1 = 0;', simplified)
        simplified = re.sub(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*0\s*\*\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*;', r'\1 = 0;', simplified)

        optimized_lines.append(simplified)

    return '\n'.join(optimized_lines)


# GUI Codes
class CodeOptimizerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Mini Compiler - Code Optimizer")
        master.geometry("900x600")

        tk.Label(master, text="Mini Compiler - Code Optimizer", font=("Helvetica", 16, "bold")).pack(pady=10)

        tk.Label(master, text="Enter C Code to Optimize:").pack(anchor="w", padx=10)
        self.input_text = tk.Text(master, height=15, width=100, font=("Consolas", 12))
        self.input_text.pack(padx=10, pady=5)

        button_frame = tk.Frame(master)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Optimize Code", command=self.optimize_code).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Load Code from File", command=self.load_file).grid(row=0, column=1, padx=10)
        tk.Button(button_frame, text="Save Optimized Code", command=self.save_file).grid(row=0, column=2, padx=10)

        tk.Label(master, text="Optimized Code:").pack(anchor="w", padx=10)
        self.output_text = tk.Text(master, height=15, width=100, font=("Consolas", 12), bg="#f0f0f0")
        self.output_text.pack(padx=10, pady=5)

    def optimize_code(self):
        code = self.input_text.get("1.0", tk.END)
        optimized = optimize_code(code)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, optimized)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("C files", "*.c"), ("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "r") as f:
                code = f.read()
            self.input_text.delete("1.0", tk.END)
            self.input_text.insert(tk.END, code)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".c",
                                                 filetypes=[("C files", "*.c"), ("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w") as f:
                f.write(self.output_text.get("1.0", tk.END))
            messagebox.showinfo("Saved", "Optimized code saved successfully!")

# Run GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = CodeOptimizerGUI(root)
    root.mainloop()
