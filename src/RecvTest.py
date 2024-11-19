import os
import tkinter as tk
from tkinter import filedialog
from GuiHelpers import dual_print
import threading
from src.App.ApplicationLayerFunctions import ReceiveAndSaveFile

# global variable
selected_folder = None

def Recv(receiver_frame):
    global selected_folder

    def open_folder_dialog():
        """Open a folder dialog to select a folder for saving files."""
        global selected_folder
        try:
            folder_path = filedialog.askdirectory(
                title="Select a Folder to Save Files"
            )
            if folder_path:
                selected_folder = folder_path
                print(f"[RecvTest.py] Folder selected: {os.path.abspath(selected_folder)}")
            else:
                print("[RecvTest.py] No folder selected.")
        except Exception as e:
            print(f"[RecvTest.py] Error during folder selection: {e}")

    def receive_data():
        """Start receiving and saving data."""
        if not selected_folder:
            print("[RecvTest.py] Please select a folder before receiving data.")
            print(receiver_frame, "[RecvTest.py] Please select a folder before receiving data.")
            return

        def threaded_receive():
            try:
                ReceiveAndSaveFile(selected_folder)
            except Exception as e:
                print(f"[RecvTest.py] Error during file reception: {e}")
                print(receiver_frame, f"Error: {e}")

        # separate thread
        threading.Thread(target=threaded_receive, daemon=True).start()

    # Button 1
    folder_select_button = tk.Button(
        receiver_frame,
        text="Select Folder to Save Files",
        command=open_folder_dialog,
        bg="lightblue",
        font=("Arial", 14, "bold"),
    )
    folder_select_button.pack(pady=20)

    # Button 2
    receive_button = tk.Button(
        receiver_frame,
        text="Start Listening",
        command=receive_data,
        bg="lightgreen",
        font=("Arial", 14, "bold"),
    )
    receive_button.pack(pady=20)
