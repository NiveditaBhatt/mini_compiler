import tkinter as tk 
import subprocess
import sys
import os

print("Current Working Directory:", os.getcwd())

def run_script(script_name):
    if os.path.exists(script_name):
        subprocess.Popen([sys.executable, script_name])
    else:
        print(f"Error: {script_name} not found!")

root = tk.Tk()
root.title("Mini C Compiler - Launcher")
root.geometry("420x520")
root.configure(bg="#2b2b2b")

tk.Label(
    root,
    text="Mini C Compiler - Module Launcher",
    font=("Arial", 15, "bold"),
    fg="white",
    bg="#2b2b2b"
).pack(pady=15)

buttons = [
    ("Lexical Analysis", r"C:\Users\nived\OneDrive\Desktop\my-mini-compiler-nived\lexical_gui.py"),
    ("Syntax Analysis", r"C:\Users\nived\OneDrive\Desktop\my-mini-compiler-nived\syntax_gui.py"),
    ("Semantic Analysis", r"C:\Users\nived\OneDrive\Desktop\my-mini-compiler-nived\sementic.py"),  
    ("Optimization", r"C:\Users\nived\OneDrive\Desktop\my-mini-compiler-nived\optimization.py"),
    ("Code Generation", r"C:\Users\nived\OneDrive\Desktop\my-mini-compiler-nived\code_generation.py"),
    ("Error Handling", r"C:\Users\nived\OneDrive\Desktop\my-mini-compiler-nived\error_handling.py"),
    ("Link & Execute", r"C:\Users\nived\OneDrive\Desktop\my-mini-compiler-nived\linking_and_executing.py"),
    ("Testing & Debugging", r"C:\Users\nived\OneDrive\Desktop\my-mini-compiler-nived\testing_and_debugging.py"),
]

for label, script in buttons:
    tk.Button(
        root,
        text=label,
        width=35,
        height=2,
        bg="#3399FF",       # lighter_blue color
        fg="white",
        font=("Arial", 10, "bold"),
        command=lambda s=script: run_script(s)
    ).pack(pady=6)

tk.Button(
    root,
    text="Exit Launcher",
    width=35,
    height=2,
    bg="#f44336",
    fg="white",
    font=("Arial", 10, "bold"),
    command=root.destroy
).pack(pady=15)

root.mainloop()
