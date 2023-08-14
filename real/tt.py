import tkinter as tk

def on_button_click():
    input_text = entry.get()
    label.config(text=f"Hello, {input_text}!")

# Create the main window
root = tk.Tk()
root.title("Simple UI")

# Create a label
label = tk.Label(root, text="Enter your name:")
label.pack()

# Create an entry field
entry = tk.Entry(root)
entry.pack()

# Create a button
button = tk.Button(root, text="Greet", command=on_button_click)
button.pack()

# Run the main event loop
root.mainloop()
