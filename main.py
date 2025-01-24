import pyautogui
import pyperclip
import time
import tkinter as tk
from tkinter import messagebox
import os
import signal

def paste_text(x, y, text, send_x, send_y, wait_time):
    """
    Pastes the text at the specified x, y coordinates and clicks the send button located at send_x, send_y.
    """
    pyautogui.click(x, y)
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.click(send_x, send_y)
    time.sleep(wait_time)

def run_program():
    """
    Executes the program based on the user-provided parameters.
    """
    global input_x, input_y, send_x, send_y

    try:
        wait_time = int(wait_var.get())
        iterations = int(iterations_var.get())
        start_numbers = {
            'sentence1': int(start_number1_var.get()) if increment1_enabled.get() else None,
            'sentence2': int(start_number2_var.get()) if increment2_enabled.get() else None,
            'sentence3': int(start_number3_var.get()) if increment3_enabled.get() else None,
            'sentence4': int(start_number4_var.get()) if increment4_enabled.get() else None
        }
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers for iterations, wait time, and starting numbers.")
        return

    # Collect sentences and validate activation checkboxes
    sentences = []
    if sentence1_enabled.get():
        sentences.append(('sentence1', sentence1_var.get()))
    if sentence2_enabled.get():
        sentences.append(('sentence2', sentence2_var.get()))
    if sentence3_enabled.get():
        sentences.append(('sentence3', sentence3_var.get()))
    if sentence4_enabled.get():
        sentences.append(('sentence4', sentence4_var.get()))

    if not sentences:
        messagebox.showerror("Error", "Please activate and provide at least one sentence.")
        return

    # Perform the automated pasting
    for i in range(iterations):
        for key, sentence in sentences:
            if start_numbers[key] is not None:
                text = sentence + str(start_numbers[key])
                paste_text(input_x, input_y, text, send_x, send_y, wait_time)
                start_numbers[key] += 1
            else:
                paste_text(input_x, input_y, sentence, send_x, send_y, wait_time)

def set_paste_position():
    """
    Captures the position for pasting text.
    """
    time.sleep(2)  # Wait for 2 seconds to position the mouse
    x, y = pyautogui.position()
    paste_pos_var.set(f"X: {x}, Y: {y}")
    global input_x, input_y
    input_x, input_y = x, y

def set_send_position():
    """
    Captures the position for clicking the send button.
    """
    time.sleep(2)  # Wait for 2 seconds to position the mouse
    x, y = pyautogui.position()
    send_pos_var.set(f"X: {x}, Y: {y}")
    global send_x, send_y
    send_x, send_y = x, y

def toggle_sentence(checkbox_var, text_entry, increment_checkbox, increment_entry):
    """
    Enables or disables the text box and incrementation options for a sentence based on the checkbox state.
    """
    if checkbox_var.get():
        text_entry.config(state="normal")
        increment_checkbox.config(state="normal")
        increment_entry.config(state="normal")
    else:
        text_entry.delete(0, tk.END)
        text_entry.config(state="disabled")
        increment_checkbox.deselect()
        increment_checkbox.config(state="disabled")
        increment_entry.delete(0, tk.END)
        increment_entry.config(state="disabled")

def kill_process():
    """
    Terminates the program immediately.
    """
    os.kill(os.getpid(), signal.SIGTERM)

# Initialize Tkinter
root = tk.Tk()
root.title("Text Pasting Automation")

# Variables
iterations_var = tk.StringVar(value="1")
wait_var = tk.StringVar(value="1")
paste_pos_var = tk.StringVar(value="Not Set")
send_pos_var = tk.StringVar(value="Not Set")
sentence1_var = tk.StringVar()
sentence1_enabled = tk.BooleanVar(value=False)
increment1_enabled = tk.BooleanVar(value=False)
start_number1_var = tk.StringVar(value="1")
sentence2_var = tk.StringVar()
sentence2_enabled = tk.BooleanVar(value=False)
increment2_enabled = tk.BooleanVar(value=False)
start_number2_var = tk.StringVar(value="1")
sentence3_var = tk.StringVar()
sentence3_enabled = tk.BooleanVar(value=False)
increment3_enabled = tk.BooleanVar(value=False)
start_number3_var = tk.StringVar(value="1")
sentence4_var = tk.StringVar()
sentence4_enabled = tk.BooleanVar(value=False)
increment4_enabled = tk.BooleanVar(value=False)
start_number4_var = tk.StringVar(value="1")

# Iterations
tk.Label(root, text="Number of Iterations:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
tk.Entry(root, textvariable=iterations_var, width=10).grid(row=0, column=1, sticky="w", padx=10, pady=5)

# Wait Time
tk.Label(root, text="Wait Time (sec):").grid(row=1, column=0, sticky="w", padx=10, pady=5)
tk.Entry(root, textvariable=wait_var, width=10).grid(row=1, column=1, sticky="w", padx=10, pady=5)

# Paste Position
tk.Label(root, text="Paste Position (click and position cursor in 2 sec):").grid(row=2, column=0, sticky="w", padx=10, pady=5)
tk.Label(root, textvariable=paste_pos_var).grid(row=2, column=1, sticky="w", padx=10, pady=5)
tk.Button(root, text="Set Position", command=set_paste_position).grid(row=2, column=2, padx=10, pady=5)

# Send Position
tk.Label(root, text="Send Position (click and position cursor in 2 sec):").grid(row=3, column=0, sticky="w", padx=10, pady=5)
tk.Label(root, textvariable=send_pos_var).grid(row=3, column=1, sticky="w", padx=10, pady=5)
tk.Button(root, text="Set Position", command=set_send_position).grid(row=3, column=2, padx=10, pady=5)

# Sentence 1
tk.Checkbutton(root, text="Include Sentence 1", variable=sentence1_enabled, command=lambda: toggle_sentence(sentence1_enabled, sentence1_entry, increment1_checkbox, start_number1_entry)).grid(row=4, column=0, sticky="w", padx=10, pady=5)
sentence1_entry = tk.Entry(root, textvariable=sentence1_var, width=40, state="disabled")
sentence1_entry.grid(row=4, column=1, padx=10, pady=5)
increment1_checkbox = tk.Checkbutton(root, text="Increment", variable=increment1_enabled, state="disabled")
increment1_checkbox.grid(row=4, column=2, sticky="w", padx=10, pady=5)
start_number1_entry = tk.Entry(root, textvariable=start_number1_var, width=10, state="disabled")
start_number1_entry.grid(row=4, column=3, padx=10, pady=5)

# Sentence 2
tk.Checkbutton(root, text="Include Sentence 2", variable=sentence2_enabled, command=lambda: toggle_sentence(sentence2_enabled, sentence2_entry, increment2_checkbox, start_number2_entry)).grid(row=5, column=0, sticky="w", padx=10, pady=5)
sentence2_entry = tk.Entry(root, textvariable=sentence2_var, width=40, state="disabled")
sentence2_entry.grid(row=5, column=1, padx=10, pady=5)
increment2_checkbox = tk.Checkbutton(root, text="Increment", variable=increment2_enabled, state="disabled")
increment2_checkbox.grid(row=5, column=2, sticky="w", padx=10, pady=5)
start_number2_entry = tk.Entry(root, textvariable=start_number2_var, width=10, state="disabled")
start_number2_entry.grid(row=5, column=3, padx=10, pady=5)

# Sentence 3
tk.Checkbutton(root, text="Include Sentence 3", variable=sentence3_enabled, command=lambda: toggle_sentence(sentence3_enabled, sentence3_entry, increment3_checkbox, start_number3_entry)).grid(row=6, column=0, sticky="w", padx=10, pady=5)
sentence3_entry = tk.Entry(root, textvariable=sentence3_var, width=40, state="disabled")
sentence3_entry.grid(row=6, column=1, padx=10, pady=5)
increment3_checkbox = tk.Checkbutton(root, text="Increment", variable=increment3_enabled, state="disabled")
increment3_checkbox.grid(row=6, column=2, sticky="w", padx=10, pady=5)
start_number3_entry = tk.Entry(root, textvariable=start_number3_var, width=10, state="disabled")
start_number3_entry.grid(row=6, column=3, padx=10, pady=5)

# Sentence 4
tk.Checkbutton(root, text="Include Sentence 4", variable=sentence4_enabled, command=lambda: toggle_sentence(sentence4_enabled, sentence4_entry, increment4_checkbox, start_number4_entry)).grid(row=7, column=0, sticky="w", padx=10, pady=5)
sentence4_entry = tk.Entry(root, textvariable=sentence4_var, width=40, state="disabled")
sentence4_entry.grid(row=7, column=1, padx=10, pady=5)
increment4_checkbox = tk.Checkbutton(root, text="Increment", variable=increment4_enabled, state="disabled")
increment4_checkbox.grid(row=7, column=2, sticky="w", padx=10, pady=5)
start_number4_entry = tk.Entry(root, textvariable=start_number4_var, width=10, state="disabled")
start_number4_entry.grid(row=7, column=3, padx=10, pady=5)

# Run Button
tk.Button(root, text="Run", command=run_program, bg="green", fg="white").grid(row=8, column=0, columnspan=2, pady=20)

# Kill Process Button
tk.Button(root, text="Kill Process", command=kill_process, bg="red", fg="white").grid(row=8, column=2, columnspan=2, pady=20)

# Start Tkinter Loop
root.mainloop()
