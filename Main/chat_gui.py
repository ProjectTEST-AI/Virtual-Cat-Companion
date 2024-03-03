import tkinter as tk
from tkinter import scrolledtext
from threading import Thread
from virtual_cat_companion import ask_virtual_cat_companion  # Import from the AI logic file

def communicate_with_ai(user_input, output_area):
    response = ask_virtual_cat_companion(user_input)
    output_area.config(state=tk.NORMAL)
    output_area.insert(tk.END, "You: " + user_input + "\n")
    output_area.insert(tk.END, "Virtual Cat Companion: " + response + "\n\n")
    output_area.config(state=tk.DISABLED)
    output_area.see(tk.END)

def send_input(input_entry, output_area):
    user_input = input_entry.get()
    if user_input.strip() != "":
        input_entry.delete(0, tk.END)
        Thread(target=communicate_with_ai, args=(user_input, output_area)).start()

def setup_gui():
    root = tk.Tk()
    root.title("Virtual Cat Companion Chat")

    frame = tk.Frame(root)
    frame.pack(padx=20, pady=20)

    output_area = scrolledtext.ScrolledText(frame, state='disabled', height=20, width=70)
    output_area.pack()

    input_entry = tk.Entry(frame, width=60)
    input_entry.pack(side=tk.LEFT, pady=(5, 0))

    send_button = tk.Button(frame, text="Send", command=lambda: send_input(input_entry, output_area))
    send_button.pack(side=tk.RIGHT, padx=(5, 0), pady=(5, 0))

    root.mainloop()

if __name__ == "__main__":
    setup_gui()