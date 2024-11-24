import os
import tkinter as tk
from tkinter import filedialog
from App.ApplicationLayerFunctions import ReceiveAndSaveFile
from LogSetup import SetupLogger
from AudioTransport.PhysicalLayer.tools.GraphRecv import create_graph, change_graph
import logging

logger = SetupLogger("[RecvTest.py]", logging.DEBUG)  
selected_folder = None

def Recv(receiver_frame, output_text): 
    global selected_folder

    graph_holder = {} # use a dictionary to hold the graph label reference
    graph_holder['graph_label'] = create_graph(receiver_frame) # create graph

    # open a folder dialog to select a folder for saving files
    def open_folder_dialog():
        global selected_folder
        folder_path = filedialog.askdirectory(title="Select a Folder to Save Files")
        if folder_path:
            selected_folder = folder_path
            logger.info(f"[RecvTest.py] Folder selected: {os.path.abspath(selected_folder)}")
        else:
            logger.info("[RecvTest.py] No folder selected.")

    # start receiving and saving data
    def receive_data():
        if not selected_folder:
            logger.info("[RecvTest.py] Please select a folder before receiving data.")
            return

        try:
            logger.info(f"[RecvTest.py] Starting data reception to folder: {selected_folder}")

            """
            ReceiveAndSaveFile(selected_folder)
            """

            # update the graph
            logger.debug("[RecvTest.py] Updating the graph...")
            graph_holder['graph_label'].destroy()                       # remove the old graph
            graph_holder['graph_label'] = change_graph(receiver_frame)  # display the new graph
            logger.info(f"[RecvTest.py] File saved successfully to {selected_folder}")
        except Exception as e:
            logger.error(f"[RecvTest.py] Error during file reception: {e}")

    # folder selection button
    tk.Button(
        receiver_frame,
        text="Select Folder to Save Files",
        command=open_folder_dialog,
        bg="lightblue",
        font=("Arial", 14, "bold")
    ).pack(pady=20)

    # start listening button
    tk.Button(
        receiver_frame,
        text="Start Listening",
        command=receive_data,
        bg="lightgreen",
        font=("Arial", 14, "bold")
    ).pack(pady=20)
