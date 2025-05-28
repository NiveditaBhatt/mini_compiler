import tkinter as tk
from tkinter import scrolledtext, filedialog
import re

class SemanticAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Compiler - Semantic Analyzer")
        self.is_dark_mode = False

        # Define color themes correctly
        self.colors = {
            "light": {
                "bg": "#ffffff",
                "fg": "#000000",
                "button_bg": "#3399FF",
                "button_fg": "#ffffff",
                "text_bg": "#f0f0f0",
                "text_fg": "#000000"
            },
            "dark": {
                "bg": "#2e2e2e",
                "fg": "#ffffff",
                "button_bg": "#3399FF",
                "button_fg": "#ffffff",
                "text_bg": "#1E1E1E",
                "text_fg": "#ffffff"
            }
        }

        self.build_gui()
        self.apply_theme("light")

    def build_gui(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # File load button
        self.file_btn = tk.Button(self.main_frame, text="Load C File", command=self.load_file)
        self.file_btn.pack(fill=tk.X, pady=(0, 5))
        self.add_hover_effect(self.file_btn)

        # Input label and text
        self.code_label = tk.Label(self.main_frame, text="Enter C-like Code:")
        self.code_label.pack(anchor="w")
        self.code_input = scrolledtext.ScrolledText(self.main_frame, height=12, wrap=tk.WORD, font=("Consolas", 11))
        self.code_input.pack(fill=tk.BOTH, expand=True)

        # Analyze button
        self.analyze_btn = tk.Button(self.main_frame, text="Analyze Semantics", command=self.analyze)
        self.analyze_btn.pack(fill=tk.X, pady=(10, 5))
        self.add_hover_effect(self.analyze_btn)

        # Output label and text
        self.output_label = tk.Label(self.main_frame, text="Output:")
        self.output_label.pack(anchor="w", pady=(10, 0))
        self.output_box = scrolledtext.ScrolledText(self.main_frame, height=8, wrap=tk.WORD, font=("Consolas", 10), state=tk.DISABLED)
        self.output_box.pack(fill=tk.BOTH, expand=True)

        # Mode toggle button
        self.toggle_btn = tk.Button(self.main_frame, text="Switch to Dark Mode", command=self.toggle_mode)
        self.toggle_btn.pack(fill=tk.X, pady=(10, 0))
        self.add_hover_effect(self.toggle_btn)

    def apply_theme(self, mode):
        theme = self.colors[mode]
        self.root.configure(bg=theme["bg"])
        self.main_frame.configure(bg=theme["bg"])

        # Update button colors
        for btn in [self.file_btn, self.analyze_btn, self.toggle_btn]:
            btn.configure(bg=theme["button_bg"], fg=theme["button_fg"], activebackground="#5ab1ff")

        # Update labels and text widgets
        self.code_label.configure(bg=theme["bg"], fg=theme["fg"])
        self.output_label.configure(bg=theme["bg"], fg=theme["fg"])

        self.code_input.configure(bg=theme["text_bg"], fg=theme["text_fg"], insertbackground=theme["fg"])
        self.output_box.configure(bg=theme["text_bg"], fg=theme["text_fg"], insertbackground=theme["fg"])

    def toggle_mode(self):
        self.is_dark_mode = not self.is_dark_mode
        mode = "dark" if self.is_dark_mode else "light"
        self.toggle_btn.configure(text="Switch to Light Mode" if self.is_dark_mode else "Switch to Dark Mode")
        self.apply_theme(mode)

    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Select C File",
            filetypes=[("C Files", "*.c;*.h"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                self.code_input.delete("1.0", tk.END)
                self.code_input.insert(tk.END, content)
                self.output_box.config(state=tk.NORMAL)
                self.output_box.delete("1.0", tk.END)
                self.output_box.insert(tk.END, f"Loaded file: {file_path}\n")
                self.output_box.config(state=tk.DISABLED)
            except Exception as e:
                self.show_error(f"Error loading file: {e}")

    def show_error(self, message):
        self.output_box.config(state=tk.NORMAL)
        self.output_box.insert(tk.END, f"❌ {message}\n")
        self.output_box.config(state=tk.DISABLED)

    def analyze(self):
        code = self.code_input.get("1.0", tk.END)
        lines = code.strip().split('\n')
        declared_vars = {}
        errors = []

        for i, line in enumerate(lines, 1):
            # Remove inline comments
            line = re.sub(r'//.*', '', line).strip()
            if not line:
                continue

            # Variable declaration (int, float, char) with optional initialization
            match_decl = re.match(r'^(int|float|char)\s+(\w+)\s*=?\s*(.*);', line)
            if match_decl:
                var_type, var_name, value = match_decl.groups()
                if var_name in declared_vars:
                    errors.append(f"[Line {i}] Variable '{var_name}' already declared.")
                else:
                    declared_vars[var_name] = var_type
                    # Simple type check: int cannot be assigned string
                    if value:
                        if var_type == "int" and re.search(r'["\']', value):
                            errors.append(f"[Line {i}] Type mismatch: cannot assign string to int '{var_name}'.")
                continue

            # Variable assignment: var = value;
            match_assign = re.match(r'^(\w+)\s*=\s*(.*);', line)
            if match_assign:
                var_name, value = match_assign.groups()
                if var_name not in declared_vars:
                    errors.append(f"[Line {i}] Variable '{var_name}' used without declaration.")
                else:
                    if declared_vars[var_name] == "int" and re.search(r'["\']', value):
                        errors.append(f"[Line {i}] Type mismatch: assigning string to int '{var_name}'.")

        # Show results in output box
        self.output_box.config(state=tk.NORMAL)
        self.output_box.delete("1.0", tk.END)
        if errors:
            self.output_box.insert(tk.END, "❌ Semantic Errors Found:\n" + "\n".join(errors))
        else:
            self.output_box.insert(tk.END, "✅ No semantic errors found.")
        self.output_box.config(state=tk.DISABLED)

    def add_hover_effect(self, widget):
        def on_enter(e):
            widget['bg'] = "#5ab1ff"  # lighter blue on hover
        def on_leave(e):
            current_mode = "dark" if self.is_dark_mode else "light"
            widget['bg'] = self.colors[current_mode]['button_bg']
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)


if __name__ == "__main__":
    root = tk.Tk()
    app = SemanticAnalyzerGUI(root)
    root.geometry("800x600")
    root.mainloop()
