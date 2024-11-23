import tkinter as tk
from PIL import Image, ImageTk
from RecvTest import Recv
from SendTest import Send
from GuiHelpers import custom_print

def load_image(path, size):
    """Load and resize an image."""
    image = Image.open(path)
    image = image.resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(image)

def clear_output():
    """Clear the output text box."""
    global output_text
    output_text.configure(state="normal")
    output_text.delete("1.0", tk.END)
    output_text.configure(state="disabled")

def show_main_menu():
    """Display the main menu."""
    global current_frame

    # Clear the current frame
    if current_frame is not None:
        current_frame.destroy()

    clear_output()

    # Create main menu frame
    current_frame = tk.Frame(root, bg="white", padx=10, pady=10)
    current_frame.pack(expand=True, fill="both")

    sender_frame = tk.Frame(current_frame, bg="white", padx=10, pady=10)
    sender_frame.pack(side=tk.LEFT, expand=True)

    receiver_frame = tk.Frame(current_frame, bg="white", padx=10, pady=10)
    receiver_frame.pack(side=tk.RIGHT, expand=True)

    # Load images
    sender_image = load_image("./src/sendLogo.png", (150, 150))
    receiver_image = load_image("./src/receiveLogo.png", (150, 150))

    # Add sender image and text
    sender_label = tk.Label(sender_frame, image=sender_image, bg="white")
    sender_label.image = sender_image
    sender_label.pack()
    sender_label.bind("<Button-1>", lambda e: show_sender_view())
    sender_text = tk.Label(sender_frame, text="Sender", font=("Arial", 16, "bold"), bg="lightgray")
    sender_text.pack()

    # Add receiver image and text
    receiver_label = tk.Label(receiver_frame, image=receiver_image, bg="white")
    receiver_label.image = receiver_image
    receiver_label.pack()
    receiver_label.bind("<Button-1>", lambda e: show_receiver_view())
    receiver_text = tk.Label(receiver_frame, text="Receiver", font=("Arial", 16, "bold"), bg="lightgray")
    receiver_text.pack()

def show_receiver_view():
    """Switch to the receiver view."""
    global current_frame
    custom_print("[main.py] Switching to Receiver", output_text=output_text)

    if current_frame is not None:
        current_frame.destroy()

    current_frame = tk.Frame(root, bg="white", padx=10, pady=10)
    current_frame.pack(expand=True, fill="both")

    back_button = tk.Button(current_frame, text="<-- Back", command=show_main_menu)
    back_button.pack(pady=10)

    Recv(current_frame, output_text) 

def show_sender_view():
    """Switch to the sender view."""
    global current_frame
    custom_print("[main.py] Switching to Sender", output_text=output_text)

    if current_frame is not None:
        current_frame.destroy()

    current_frame = tk.Frame(root, bg="white", padx=10, pady=10)
    current_frame.pack(expand=True, fill="both")

    back_button = tk.Button(current_frame, text="<-- Back", command=show_main_menu)
    back_button.pack(pady=10)

    Send(current_frame, output_text) 

# Initialize Tkinter window
root = tk.Tk()
root.title("File Transfer GUI")
root.geometry("600x400")

current_frame = None
output_text = tk.Text(root, state="disabled", height=5)
output_text.pack(side=tk.BOTTOM, fill=tk.X)

show_main_menu()
root.mainloop()
