import tkinter as tk

def on_button_click():
    label.config(text="Hello, World!")

root = tk.Tk()
root.title("Simple GUI")

label = tk.Label(root, text="Click the button")
label.pack(pady=10)

button = tk.Button(root, text="Click Me", command=on_button_click)
button.pack(pady=5)

root.mainloop()