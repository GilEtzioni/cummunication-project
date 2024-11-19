import os
import tkinter as tk
from tkinter import filedialog
from GuiHelpers import dual_print
from src.App.ApplicationLayerFunctions import TransferFile

# global variables
file_select_button = None
selected_file = None  
selected_file_path = None 


def Send(sender_frame):
    global file_select_button, selected_file, selected_file_path

    def open_file_dialog():
        global selected_file, selected_file_path
        try:
            file_path = filedialog.askopenfilename(
                title="Select a File to Send",
                filetypes=(("All Files", "*.*"), ("Text Files", "*.txt"), ("PDF Files", "*.pdf")),
            )
            if not file_path:
                print("[SendTest.py] No file selected.")
                return

            selected_file = os.path.basename(file_path)
            selected_file_path = file_path
            print(f"[SendTest.py] File selected: {selected_file}")
        except Exception as e:
            print(f"[SendTest.py] Error during file selection: {e}")

    def send_file():
        global selected_file, selected_file_path

        print(f"selected_file: {selected_file}")               # example.txt
        print(f"selected_file_path: {selected_file_path}")     # /Users/giletzioni/Desktop/example.txt

        if not selected_file:
            print("[SendTest.py] No file selected.")
        else:
            try:
                file_extension = os.path.splitext(selected_file)[1].lower()  
                print(f"[SendTest.py] File extension: {file_extension}")

                # send the file to ./Transports
                TransferFile(selected_file_path) 
                print(f"[SendTest.py] File sent successfully. Sent file: {selected_file}")
            except Exception as e:
                print(f"[SendTest.py] Error sending file: {e}")

    # Button 1
    file_select_button = tk.Button(
        sender_frame,
        text="Select File To Send",
        command=open_file_dialog,
        bg="lightgreen",
        font=("Arial", 14, "bold"),
    )
    file_select_button.pack(pady=20)

    # Button 2
    send_button = tk.Button(
        sender_frame,
        text="Send",
        command=send_file,
        bg="orange",
        font=("Arial", 14, "bold"),
    )
    send_button.pack(pady=20)