import os
import tkinter as tk
from tkinter import filedialog
from App.ApplicationLayerFunctions import TransferFile
from LogSetup import SetupLogger
import logging
from AudioTransport.PhysicalLayer.tools.GraphSend import create_graph, change_graph

logger = SetupLogger("[SendTest]", logging.DEBUG)  
# TODO move prints to work with logger

selected_file_path = None 

def Send(sender_frame, output_text): 
    global selected_file_path  

    graph_holder = {} # use a dictionary to hold the graph label reference
    graph_holder['graph_label'] = create_graph(sender_frame) # create graph

    logger.debug(f"Preparing to send file: {selected_file_path}")
    # open a file dialog to select a file to send
    def open_file_dialog():

        global selected_file_path
        file_path = filedialog.askopenfilename(
            title="Select a File to Send",
            filetypes=(("All Files", "*.*"), ("Text Files", "*.txt"), ("PDF Files", "*.pdf")),
        )
        if file_path:
            selected_file_path = file_path
            logger.info(f"[SendTest.py] File selected: {file_path}")
        else:
            logger.info("[SendTest.py] No file selected.")

    # send the selected file
    def send_file():
        if not selected_file_path:
            logger.info("[SendTest.py] No file selected.")
            return

        try:
            logger.debug(f"[SendTest.py] Preparing to send file: {selected_file_path}")
            TransferFile(selected_file_path)
            logger.info(f"[SendTest.py] File sent successfully. Sent file: {selected_file_path}")

            # update the graph
            logger.debug("[RecvTest.py] Updating the graph...")
            graph_holder['graph_label'].destroy()                       # remove the old graph
            graph_holder['graph_label'] = change_graph(sender_frame)  # display the new graph
        except Exception as e:
            logger.error(f"[SendTest.py] Error sending file: {e}")

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