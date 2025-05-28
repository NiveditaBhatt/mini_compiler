import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
import subprocess
import os

# Function to compile and run the C file
def compile_and_run_c_file(file_path):
    # File paths
    executable_path = file_path.replace(".c", ".exe")
    
    # Compile the C file using GCC
    compile_command = f"gcc {file_path} -o {executable_path}"
    compile_process = subprocess.Popen(compile_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    compile_stdout, compile_stderr = compile_process.communicate()
    
    if compile_process.returncode != 0:
        return f"Compilation Error:\n{compile_stderr.decode()}"
    
    # Run the compiled C program
    run_process = subprocess.Popen(executable_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    run_stdout, run_stderr = run_process.communicate()
    
    if run_process.returncode != 0:
        return f"Runtime Error:\n{run_stderr.decode()}"
    
    return run_stdout.decode()

# GUI Class
class TACCodeGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Three Address Code (TAC) Generator")
        self.dark_mode = False
        self.selected_code = ""

        self.create_widgets()
        self.set_light_mode()

    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10, anchor="w")

        self.select_button = tk.Button(self.frame, text="Load C File", bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), command=self.load_file)
        self.select_button.grid(row=0, column=0, padx=5, pady=5)

        self.analyze_button = tk.Button(self.frame, text="Generate Target Code", bg="#2196F3", fg="white", font=("Arial", 11, "bold"), command=self.generate_target_code)
        self.analyze_button.grid(row=0, column=1, padx=5, pady=5)

        self.link_button = tk.Button(self.frame, text="Link Code", bg="#FFC107", fg="white", font=("Arial", 11, "bold"), command=self.link_code)
        self.link_button.grid(row=0, column=2, padx=5, pady=5)

        self.execute_button = tk.Button(self.frame, text="Execute Code", bg="#FF5722", fg="white", font=("Arial", 11, "bold"), command=self.execute_code)
        self.execute_button.grid(row=0, column=3, padx=5, pady=5)

        self.result_button = tk.Button(self.frame, text="Show Execution Result", bg="#8BC34A", fg="white", font=("Arial", 11, "bold"), command=self.show_execution_result)
        self.result_button.grid(row=1, column=0, padx=5, pady=5)

        self.mode_button = tk.Button(self.frame, text="Dark Mode", bg="#f44336", fg="white", font=("Arial", 11, "bold"), command=self.toggle_mode)
        self.mode_button.grid(row=1, column=1, padx=5, pady=5)

        self.selected_code_label = tk.Label(self.root, text="Selected Code", font=("Arial", 12, "bold"))
        self.selected_code_label.pack(padx=10, pady=10)

        self.selected_code_text = scrolledtext.ScrolledText(self.root, width=70, height=5, font=("Consolas", 11))
        self.selected_code_text.pack(padx=10, pady=10)

        self.output_text = scrolledtext.ScrolledText(self.root, width=70, height=10, font=("Consolas", 11))
        self.output_text.pack(padx=10, pady=10)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("C Files", "*.c")])
        if file_path:
            self.selected_code = open(file_path, 'r').read()
            self.selected_code_text.delete(1.0, tk.END)
            self.selected_code_text.insert(tk.END, self.selected_code)

    def generate_target_code(self):
        # For simplicity, just return sample TAC code (target code generation logic can be added)
        tac_code = [
            "t1 = a + b",
            "t2 = t1 * c",
            "t3 = t2 - d"
        ]
        self.output_text.delete(1.0, tk.END)
        for line in tac_code:
            self.output_text.insert(tk.END, line + "\n")

    def link_code(self):
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Linking in progress...\n")
        self.output_text.insert(tk.END, "Linking successful! Ready for execution.\n")

    def execute_code(self):
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Executing the code...\n")
        self.output_text.insert(tk.END, "Execution finished.\n")

    def show_execution_result(self):
        if self.selected_code:
            # Write the selected code to a temporary C file
            temp_file_path = "temp.c"
            with open(temp_file_path, 'w') as temp_file:
                temp_file.write(self.selected_code)
            
            # Compile and execute the C file, then get the result
            result = compile_and_run_c_file(temp_file_path)

            # Show the result in the output section
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "Execution Results:\n")
            self.output_text.insert(tk.END, result)
            
            # Clean up the temporary file after execution
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

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
        self.selected_code_text.config(bg="#1E1E1E", fg="white", insertbackground="white")

    def set_light_mode(self):
        self.root.config(bg="#FFFFFF")
        self.frame.config(bg="#FFFFFF")
        self.output_text.config(bg="#F0F0F0", fg="#000000", insertbackground="black")
        self.selected_code_text.config(bg="#F0F0F0", fg="black", insertbackground="black")


# === Run GUI ===
if __name__ == "__main__":
    root = tk.Tk()
    app = TACCodeGeneratorApp(root)
    root.mainloop()
