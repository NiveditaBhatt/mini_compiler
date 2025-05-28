import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import subprocess
import os
import time

class ModernCCompilerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🛠️ Mini C Compiler & Runner")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        self.dark_mode = False

        self.file_path = ""
        self.setup_ui()
        self.set_light_mode()

    def setup_ui(self):
        # --- Header Frame ---
        header = tk.Frame(self.root, height=60)
        header.pack(fill=tk.X, pady=(0, 5))
        self.title_label = tk.Label(header, text="Mini C Compiler", font=("Helvetica", 20, "bold"))
        self.title_label.pack(pady=10)

        # --- Button Frame ---
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        self.load_btn = tk.Button(button_frame, text="📂 Load C File", font=("Arial", 11), width=15, command=self.load_file)
        self.load_btn.grid(row=0, column=0, padx=10)

        self.run_btn = tk.Button(button_frame, text="▶ Run & Test", font=("Arial", 11), width=15, command=self.run_code)
        self.run_btn.grid(row=0, column=1, padx=10)

        self.toggle_btn = tk.Button(button_frame, text="🌙 Dark Mode", font=("Arial", 11), width=15, command=self.toggle_mode)
        self.toggle_btn.grid(row=0, column=2, padx=10)

        # --- Code Editor Section ---
        code_label = tk.Label(self.root, text="C Code Editor", font=("Arial", 12, "bold"))
        code_label.pack(anchor="w", padx=15)

        self.code_editor = scrolledtext.ScrolledText(self.root, width=100, height=15, font=("Courier New", 11), wrap=tk.WORD, relief=tk.GROOVE, borderwidth=2)
        self.code_editor.pack(padx=15, pady=5)

        # --- Output Label ---
        output_label = tk.Label(self.root, text="Execution Output", font=("Arial", 12, "bold"))
        output_label.pack(anchor="w", padx=15)

        self.output_display = scrolledtext.ScrolledText(self.root, width=100, height=10, font=("Courier New", 11), wrap=tk.WORD, relief=tk.GROOVE, borderwidth=2)
        self.output_display.pack(padx=15, pady=5)

    def load_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("C Files", "*.c")])
        if self.file_path:
            with open(self.file_path, 'r') as file:
                code = file.read()
            self.code_editor.delete(1.0, tk.END)
            self.code_editor.insert(tk.END, code)

    def run_code(self):
        if not self.file_path:
            messagebox.showerror("Error", "Please load a C file first.")
            return

        exe_path = self.file_path.replace(".c", ".exe")
        compile_cmd = ["gcc", self.file_path, "-o", exe_path]

        try:
            start_time = time.time()
            compile_proc = subprocess.run(compile_cmd, capture_output=True, text=True)
            compile_time = time.time() - start_time

            self.output_display.delete(1.0, tk.END)

            if compile_proc.returncode != 0:
                self.output_display.insert(tk.END, f"🔴 Compilation Error:\n{compile_proc.stderr}")
                return

            start_time = time.time()
            run_proc = subprocess.run([exe_path], capture_output=True, text=True, timeout=5)
            execution_time = time.time() - start_time

            output = run_proc.stdout or "✅ Code executed with no output."
            self.output_display.insert(tk.END, f"{output}\n\n⏱️ Compile Time: {compile_time:.2f}s | Run Time: {execution_time:.2f}s")

        except subprocess.TimeoutExpired:
            self.output_display.insert(tk.END, "⏳ Execution Timed Out.")
        except Exception as e:
            self.output_display.insert(tk.END, f"⚠️ Error during execution:\n{str(e)}")

    def toggle_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.set_dark_mode()
            self.toggle_btn.config(text="☀ Light Mode")
        else:
            self.set_light_mode()
            self.toggle_btn.config(text="🌙 Dark Mode")

    def set_dark_mode(self):
        self.root.config(bg="#121212")
        self.title_label.config(bg="#121212", fg="#FAFAFA")
        self.code_editor.config(bg="#1E1E1E", fg="#D4D4D4", insertbackground="white")
        self.output_display.config(bg="#1E1E1E", fg="#D4D4D4", insertbackground="white")
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(bg="#121212", fg="white")

    def set_light_mode(self):
        self.root.config(bg="#FFFFFF")
        self.title_label.config(bg="#FFFFFF", fg="#000000")
        self.code_editor.config(bg="#F8F8F8", fg="#000000", insertbackground="black")
        self.output_display.config(bg="#F8F8F8", fg="#000000", insertbackground="black")
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(bg="#FFFFFF", fg="black")

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernCCompilerGUI(root)
    root.mainloop()
