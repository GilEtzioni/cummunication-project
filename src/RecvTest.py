import os
import tkinter as tk
from tkinter import filedialog
from App.ApplicationLayerFunctions import ReceiveAndSaveFile
from GuiHelpers import custom_print

selected_folder = None

def Recv(receiver_frame, output_text): 
    global selected_folder

    # open a folder dialog to select a folder for saving files
    def open_folder_dialog():
        global selected_folder
        folder_path = filedialog.askdirectory(title="Select a Folder to Save Files")
        if folder_path:
            selected_folder = folder_path
            print(f"[RecvTest.py] Folder selected: {os.path.abspath(selected_folder)}")
        else:
            print("[RecvTest.py] No folder selected.")

    # start receiving and saving data
    def receive_data():
        if not selected_folder:
            print("[RecvTest.py] Please select a folder before receiving data.")
            return

        try:
            print(f"[RecvTest.py] Starting data reception to folder: {selected_folder}")
            ReceiveAndSaveFile(selected_folder)
            print(f"[RecvTest.py] File saved successfully to {selected_folder}")
        except Exception as e:
            print(f"[RecvTest.py] Error during file reception: {e}")

    tk.Button(
        receiver_frame,
        text="Select Folder to Save Files",
        command=open_folder_dialog,
        bg="lightblue",
        font=("Arial", 14, "bold")
    ).pack(pady=20)

    tk.Button(
        receiver_frame,
        text="Start Listening",
        command=receive_data,
        bg="lightgreen",
        font=("Arial", 14, "bold")
    ).pack(pady=20)
