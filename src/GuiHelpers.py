import tkinter as tk

def custom_print(*args, **kwargs):
    """Redirect print statements to both the terminal and the output_text widget."""
    
    # Print to the terminal (console)
    print(*args)
    
    # Get output_text from kwargs to insert into the Text widget in the GUI
    output_text = kwargs.get('output_text')  # Get output_text from kwargs
    if output_text:
        output_text.configure(state="normal")
        output_text.insert(tk.END, " ".join(map(str, args)) + "\n")  # Insert the message into the Text widget
        output_text.configure(state="disabled")  # Disable editing the Text widget
        output_text.yview(tk.END)  # Scroll to the bottom of the Text widget
