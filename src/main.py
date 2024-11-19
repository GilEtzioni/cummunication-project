import tkinter as tk
from PIL import Image, ImageTk
from src.GuiHelpers import dual_print, initialize_gui
from src.RecvTest import Recv
from src.SendTest import Send

# load the sender and receiver pictures
def load_image(path, size):
    image = Image.open(path)
    image = image.resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(image)

# clear the output text box
def clear_output():
    global output_text
    output_text.configure(state="normal")  # Enable editing
    output_text.delete("1.0", tk.END)  # Clear all text
    output_text.configure(state="disabled")  # Make it read-only again

# function to display the main menu
def show_main_menu():
    global current_frame

    # clear the current frame
    if current_frame is not None:
        current_frame.destroy()

    # clear the output text box
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
    sender_label.pack()
    sender_label.bind("<Button-1>", lambda e: show_sender_view())  # Bind click to sender view
    sender_text = tk.Label(sender_frame, text="Sender", font=("Arial", 16, "bold"), bg="lightgray")
    sender_text.pack()

    # add receiver image and text
    receiver_label = tk.Label(receiver_frame, image=receiver_image, bg="white")
    receiver_label.image = receiver_image  # Keep a reference
    receiver_label.pack()
    receiver_label.bind("<Button-1>", lambda e: show_receiver_view())  # Bind click to receiver view
    receiver_text = tk.Label(receiver_frame, text="Receiver", font=("Arial", 16, "bold"), bg="lightgray")
    receiver_text.pack()

# switch to the receiver view
def show_receiver_view():
    global current_frame
    dual_print("[main.py] Switching to Receiver")

    # clear the current frame
    if current_frame is not None:
        current_frame.destroy()

    # create receiver view frame
    current_frame = tk.Frame(root, bg="white", padx=10, pady=10)
    current_frame.pack(expand=True, fill="both")

    # add a single back button for navigation
    back_button = tk.Button(current_frame, text="<-- Back", command=show_main_menu)
    back_button.pack(pady=10)

    # call the Recv function to add additional GUI elements
    Recv(current_frame)


# switch to the sender view
def show_sender_view():
    global current_frame
    dual_print("[main.py] Switching to Sender")

    # clear the current frame
    if current_frame is not None:
        current_frame.destroy()

    # create sender view frame
    current_frame = tk.Frame(root, bg="white", padx=10, pady=10)
    current_frame.pack(expand=True, fill="both")

    # add a single back button for navigation
    back_button = tk.Button(current_frame, text="<-- Back", command=show_main_menu)
    back_button.pack(pady=10)

    # call the Send function to add additional GUI elements
    Send(current_frame)

# initialize Tkinter window
root = tk.Tk()
initialize_gui(root)  

current_frame = None  
output_text = root.nametowidget(".!text")

# start the main menu
show_main_menu()
root.mainloop()