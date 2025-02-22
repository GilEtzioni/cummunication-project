import tkinter as tk
import argparse
from tkinter import ttk
from PIL import Image, ImageTk
from RecvTest import Recv
from SendTest import Send
from LogSetup import  SetupLogger
from AudioTransport.AudioConfig import Config  
import logging
from GuiHelpers import GuiHandler
import ttkbootstrap as ttk
from ttkbootstrap.constants import INFO

logger = SetupLogger("[main.py]", logging.DEBUG)

# load and resize an image
def load_image(path, size):
    image = Image.open(path)
    image = image.resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(image)

# clear the output text box
def clear_output():
    global output_text
    output_text.configure(state="normal")
    output_text.delete("1.0", tk.END)
    output_text.configure(state="disabled")

def apply_css_styles():
    style = ttk.Style()
    style.configure(
        "Blue.TButton",
        background="#87CEEB",  # blue color
        foreground="white",
        font=("Arial", 14, "bold"),
        padding=10,
        relief="flat",  # no border
        borderwidth=0,  # no border
    )
    style.map("Blue.TButton",
              background=[("active", "#B0E0E6")])  # slightly lighter blue when active

# display the main menu
def show_main_menu():
    # logger.info("Please choose sender / receiver")
    global current_frame

    # clear the current frame
    if current_frame is not None:
        current_frame.destroy()

    clear_output()

    # create main menu frame
    current_frame = ttk.Frame(root, padding=10)
    current_frame.pack(expand=True, fill="both")

    sender_frame = ttk.Frame(current_frame, padding=10)
    sender_frame.pack(side=tk.LEFT, expand=True)

    receiver_frame = ttk.Frame(current_frame, padding=10)
    receiver_frame.pack(side=tk.RIGHT, expand=True)

    # load images
    sender_image = load_image("./src/sendLogo.png", (150, 150))
    receiver_image = load_image("./src/receiveLogo.png", (150, 150))
    # back_image = load_image("./src/BackButton.png", (20, 20))

    # add sender image and text
    sender_label = tk.Label(sender_frame, image=sender_image, bg="white", borderwidth=0)
    sender_label.image = sender_image
    sender_label.pack()
    sender_label.bind("<Button-1>", lambda e: show_sender_view())
    sender_text = tk.Label(sender_frame, text="Sender", font=("Arial", 16, "bold"), bg="white")
    sender_text.pack()

    # add receiver image and text
    receiver_label = tk.Label(receiver_frame, image=receiver_image, bg="white", borderwidth=0)
    receiver_label.image = receiver_image
    receiver_label.pack()
    receiver_label.bind("<Button-1>", lambda e: show_receiver_view())
    receiver_text = tk.Label(receiver_frame, text="Receiver", font=("Arial", 16, "bold"), bg="white")
    receiver_text.pack()


# switch to the receiver view
def show_receiver_view():
    global current_frame
    logger.info("Switching to Receiver")

    if current_frame is not None:
        current_frame.destroy()

    current_frame = ttk.Frame(root, padding=10)
    current_frame.pack(expand=True, fill="both")

    back_button = ttk.Button(
        current_frame,
        text="<-- Back",
        command=show_main_menu,
        style="Blue.TButton"
    )
    back_button.pack(pady=10, anchor="w", side="top")

    Recv(current_frame, Config(),args.path) 

# switch to the sender view
def show_sender_view():
    global current_frame
    logger.info("Switching to Sender")

    if current_frame is not None:
        current_frame.destroy()

    current_frame = ttk.Frame(root, padding=10)
    current_frame.pack(expand=True, fill="both")

    back_button = ttk.Button(
        current_frame, 
        text="<-- Back", 
        command=show_main_menu,
        style="Blue.TButton"
    )
    back_button.pack(pady=10, anchor="w", side="top")

    Send(current_frame, Config(),args.path)


# initialize Tkinter window
root = tk.Tk()
root.title("File Transfer GUI")
root.geometry("800x770")

apply_css_styles()

current_frame = None

output_text = tk.Text(root, state="disabled", height=20, bg="lightgrey", bd=2, relief="solid")
output_text.pack(side=tk.BOTTOM, fill=tk.X)
root.update_idletasks()  # force GUI layout update

logging.getLogger().addHandler(GuiHandler(output_text))
logging.getLogger().setLevel(logging.INFO)
# Parse command-line arguments
parser = argparse.ArgumentParser(description="File Transfer GUI")
parser.add_argument('--sender', action='store_true', help="Run as sender")
parser.add_argument('--receiver', action='store_true', help="Run as receiver")
parser.add_argument('--path', type=str, help="Path to the file to send or folder to save received files")
args = parser.parse_args()
if args.sender and args.receiver:
    logger.error("Please choose either sender or receiver")
    exit(1)

if args.receiver:
    show_receiver_view()
elif args.sender:
    show_sender_view()
else:
    show_main_menu()
root.mainloop()