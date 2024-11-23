import os
import tkinter as tk
from tkinter import filedialog
from App.ApplicationLayerFunctions import TransferFile
from LogSetup import SetupLogger
import logging
logger = SetupLogger("[SendTest]", logging.DEBUG)  
# TODO move prints to work with logger

selected_file_path = None 

def Send(sender_frame, output_text): 
    global selected_file_path  
    logger.info(f"Preparing to send file: {selected_file_path}")
    # open a file dialog to select a file to send
    def open_file_dialog():

        global selected_file_path
        file_path = filedialog.askopenfilename(
            title="Select a File to Send",
            filetypes=(("All Files", "*.*"), ("Text Files", "*.txt"), ("PDF Files", "*.pdf")),
        )
        if file_path:
            selected_file_path = file_path
            print(f"[SendTest.py] File selected: {file_path}")
        else:
            print("[SendTest.py] No file selected.")

    # send the selected file
    def send_file():
        if not selected_file_path:
            print("[SendTest.py] No file selected.")
            return

        try:
            print(f"[SendTest.py] Preparing to send file: {selected_file_path}")
            TransferFile(selected_file_path)
            print(f"[SendTest.py] File sent successfully. Sent file: {selected_file_path}")
        except Exception as e:
            print(f"[SendTest.py] Error sending file: {e}")

    tk.Button(
        sender_frame,
        text="Select File To Send",
        command=open_file_dialog,
        bg="lightgreen",
        font=("Arial", 14, "bold")
    ).pack(pady=20)

    tk.Button(
        sender_frame,
        text="Send",
        command=send_file,
        bg="orange",
        font=("Arial", 14, "bold")
    ).pack(pady=20)

