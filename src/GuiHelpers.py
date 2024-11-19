import tkinter as tk

# global variables
root = None
output_text = None

def initialize_gui(application_root):
    global root, output_text
    root = application_root
    # create a default output text
    output_text = tk.Text(root, wrap="word", height=20, width=60)
    output_text.pack(padx=10, pady=10, expand=True, fill="both")
    output_text.configure(state="disabled")  # Make it read-only initially

def dual_print(message, tag="stdout", parent=None):
    global root, output_text

    print(message)  # print to the terminal

    # if parent is provided, create a local Text widget
    if parent:
        local_text = tk.Text(parent, wrap="word", height=10, width=40)
        local_text.pack(padx=10, pady=10, expand=True, fill="both")
        local_text.insert("end", message + "\n", tag)
        local_text.see("end")  
        return

    # print to the global Text widget
    if root is None or output_text is None:
        raise RuntimeError("GUI not initialized. Call initialize_gui(root) first.")

    output_text.configure(state="normal")  
    output_text.insert("end", message + "\n", tag)
    output_text.configure(state="disabled") 
    output_text.see("end") 

    # GUI update GUI immediately
    root.update_idletasks()