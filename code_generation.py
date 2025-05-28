import tkinter as tk
from tkinter import filedialog, scrolledtext
from pycparser import c_parser, c_ast


# ====== Symbol Table Extraction ======
def parse_c_file(file_path):
    with open(file_path, 'r') as file:
        c_code = file.read()

    # Remove #include lines (pycparser cannot handle real headers)
    c_code = '\n'.join(line for line in c_code.splitlines() if not line.strip().startswith('#'))

    parser = c_parser.CParser()
    try:
        ast = parser.parse(c_code)
    except Exception as e:
        return f"Error parsing C code:\n{e}"

    symbol_table = {}

    class SymbolVisitor(c_ast.NodeVisitor):
        def __init__(self):
            self.counter = 1

        def visit_Decl(self, node):
            var_name = node.name
            var_type = self._get_type(node.type)
            var_size = '4 bytes'
            var_dimension = '1'

            if isinstance(node.type, c_ast.ArrayDecl):
                if isinstance(node.type.dim, c_ast.Constant):
                    var_dimension = node.type.dim.value
                    var_size = f"{int(var_dimension) * 4} bytes"

            var_address = f"memory[{self.counter}]"
            self.counter += 1

            symbol_table[var_name] = {
                'type': var_type,
                'size': var_size,
                'dimension': var_dimension,
                'address': var_address
            }

        def _get_type(self, node):
            if isinstance(node, c_ast.TypeDecl):
                return self._get_type(node.type)
            elif isinstance(node, c_ast.IdentifierType):
                return ' '.join(node.names)
            elif isinstance(node, c_ast.PtrDecl):
                return f"pointer to {self._get_type(node.type)}"
            elif isinstance(node, c_ast.ArrayDecl):
                return f"array of {self._get_type(node.type)}"
            return "unknown"

    visitor = SymbolVisitor()
    visitor.visit(ast)
    return symbol_table


# ====== TAC to Target Code Generator ======
def generate_code(tac_code):
    target_code = []
    for line in tac_code:
        if '=' not in line:
            continue

        parts = line.split('=')
        dest = parts[0].strip()
        expr = parts[1].strip()

        if '+' in expr:
            op1, op2 = map(str.strip, expr.split('+'))
            target_code.append(f"LOAD {op1}")
            target_code.append(f"ADD {op2}")
        elif '-' in expr:
            op1, op2 = map(str.strip, expr.split('-'))
            target_code.append(f"LOAD {op1}")
            target_code.append(f"SUB {op2}")
        elif '*' in expr:
            op1, op2 = map(str.strip, expr.split('*'))
            target_code.append(f"LOAD {op1}")
            target_code.append(f"MUL {op2}")
        elif '/' in expr:
            op1, op2 = map(str.strip, expr.split('/'))
            target_code.append(f"LOAD {op1}")
            target_code.append(f"DIV {op2}")
        else:
            target_code.append(f"MOVE {expr}")

        target_code.append(f"STORE {dest}")
    return target_code


# ====== GUI Class ======
class TACCodeGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("C Symbol Table and TAC Generator")
        self.dark_mode = False
        self.tac_code = []

        self.create_widgets()
        self.set_light_mode()

    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10, anchor="w")

        self.select_button = tk.Button(self.frame, text="Load C File", bg="#4CAF50", fg="white",
                                       font=("Arial", 11, "bold"), command=self.load_file)
        self.select_button.grid(row=0, column=0, padx=5, pady=5)

        self.analyze_button = tk.Button(self.frame, text="Generate Target Code", bg="#2196F3", fg="white",
                                        font=("Arial", 11, "bold"), command=self.generate_target_code)
        self.analyze_button.grid(row=0, column=1, padx=5, pady=5)

        self.mode_button = tk.Button(self.frame, text="Dark Mode", bg="#f44336", fg="white",
                                     font=("Arial", 11, "bold"), command=self.toggle_mode)
        self.mode_button.grid(row=0, column=2, padx=5, pady=5)

        self.output_text = scrolledtext.ScrolledText(self.root, width=70, height=10, font=("Consolas", 11))
        self.output_text.pack(padx=10, pady=10)

        self.symbol_table_frame = tk.Frame(self.root)
        self.symbol_table_frame.pack(padx=10, pady=10)

        self.symbol_table_label = tk.Label(self.symbol_table_frame, text="Symbol Table", font=("Arial", 12, "bold"))
        self.symbol_table_label.grid(row=0, column=0, padx=5, pady=5)

        self.symbol_table_text = scrolledtext.ScrolledText(self.symbol_table_frame, width=70, height=6,
                                                           font=("Consolas", 11))
        self.symbol_table_text.grid(row=1, column=0, padx=5, pady=5)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("C Files", "*.c")])
        if file_path:
            result = parse_c_file(file_path)
            if isinstance(result, str):  # Error string
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(tk.END, result)
                return
            symbol_table = result
            self.update_symbol_table(symbol_table)

            self.tac_code = self.generate_sample_tac_code()
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "TAC Code:\n")
            for line in self.tac_code:
                self.output_text.insert(tk.END, line + "\n")

    def generate_sample_tac_code(self):
        return [
            "t1 = a + b",
            "t2 = t1 * c",
            "t3 = t2 - d"
        ]

    def update_symbol_table(self, symbol_table):
        header = "Name\tType\tSize\tDimension\tAddress\n"
        content = ''
        for name, details in symbol_table.items():
            content += f"{name}\t{details['type']}\t{details['size']}\t{details['dimension']}\t{details['address']}\n"

        self.symbol_table_text.delete(1.0, tk.END)
        self.symbol_table_text.insert(tk.END, header + content)

    def generate_target_code(self):
        if not self.tac_code:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "No TAC code available. Please load a file first.")
            return

        target_code = generate_code(self.tac_code)

        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Target Code:\n")
        for instr in target_code:
            self.output_text.insert(tk.END, instr + "\n")

    def toggle_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.set_dark_mode()
            self.mode_button.config(text="Light Mode")
        else:
            self.set_light_mode()
            self.mode_button.config(text="Dark Mode")

    def set_dark_mode(self):
        self.root.config(bg="#121212")
        self.frame.config(bg="#121212")
        self.output_text.config(bg="#1E1E1E", fg="#FFFFFF", insertbackground="white")
        self.symbol_table_text.config(bg="#1E1E1E", fg="white", insertbackground="white")
        self.symbol_table_label.config(bg="#121212", fg="white")

    def set_light_mode(self):
        self.root.config(bg="#FFFFFF")
        self.frame.config(bg="#FFFFFF")
        self.output_text.config(bg="#F0F0F0", fg="#000000", insertbackground="black")
        self.symbol_table_text.config(bg="#F0F0F0", fg="black", insertbackground="black")
        self.symbol_table_label.config(bg="#FFFFFF", fg="black")


# ====== Run the GUI ======
if __name__ == "__main__":
    root = tk.Tk()
    app = TACCodeGeneratorApp(root)
    root.mainloop()
