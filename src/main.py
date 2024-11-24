import tkinter as tk
from PIL import Image, ImageTk
from RecvTest import Recv
from SendTest import Send
from LogSetup import SetupLogger
import logging
from GuiHelpers import GuiHandler

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

# display the main menu
def show_main_menu():
    global current_frame

    # clear the current frame
    if current_frame is not None:
        current_frame.destroy()

    clear_output()

    # create main menu frame
    current_frame = tk.Frame(root, bg="white", padx=10, pady=10)
    current_frame.pack(expand=True, fill="both")

    sender_frame = tk.Frame(current_frame, bg="white", padx=10, pady=10)
    sender_frame.pack(side=tk.LEFT, expand=True)

    receiver_frame = tk.Frame(current_frame, bg="white", padx=10, pady=10)
    receiver_frame.pack(side=tk.RIGHT, expand=True)

    # load images
    sender_image = load_image("./src/sendLogo.png", (150, 150))
    receiver_image = load_image("./src/receiveLogo.png", (150, 150))

    # add sender image and text
    sender_label = tk.Label(sender_frame, image=sender_image, bg="white")
    sender_label.image = sender_image
    sender_label.pack()
    sender_label.bind("<Button-1>", lambda e: show_sender_view())
    sender_text = tk.Label(sender_frame, text="Sender", font=("Arial", 16, "bold"), bg="lightgray")
    sender_text.pack()

    # add receiver image and text
    receiver_label = tk.Label(receiver_frame, image=receiver_image, bg="white")
    receiver_label.image = receiver_image
    receiver_label.pack()
    receiver_label.bind("<Button-1>", lambda e: show_receiver_view())
    receiver_text = tk.Label(receiver_frame, text="Receiver", font=("Arial", 16, "bold"), bg="lightgray")
    receiver_text.pack()

# switch to the receiver view
def show_receiver_view():
    global current_frame
    logger.info("Switching to Receiver")

    if current_frame is not None:
        current_frame.destroy()

    current_frame = tk.Frame(root, bg="white", padx=10, pady=10)
    current_frame.pack(expand=True, fill="both")

    back_button = tk.Button(
        current_frame, 
        text="<-- Back", 
        command=show_main_menu,
        bg="orange",
        font=("Arial", 14, "bold")
    ).pack(pady=20)

    Recv(current_frame, output_text)

# switch to the sender view
def show_sender_view():
    global current_frame
    logger.info("Switching to Sender")

    if current_frame is not None:
        current_frame.destroy()

    current_frame = tk.Frame(root, bg="white", padx=10, pady=10)
    current_frame.pack(expand=True, fill="both")

    back_button = tk.Button(
        current_frame, 
        text="<-- Back", 
        command=show_main_menu,
        bg="orange",
        font=("Arial", 14, "bold")
    ).pack(pady=20)


    Send(current_frame, output_text) 


# initialize Tkinter window
root = tk.Tk()
root.title("File Transfer GUI")
root.geometry("900x600")

current_frame = None
output_text = tk.Text(root, state="disabled", height=15)
output_text.pack(side=tk.BOTTOM, fill=tk.X)

logging.getLogger().addHandler(GuiHandler(output_text))
logging.getLogger().setLevel(logging.INFO)
show_main_menu()
root.mainloop()
