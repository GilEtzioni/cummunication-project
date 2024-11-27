import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from App.ApplicationLayerFunctions import ReceiveAndSaveFile
from AudioTransport.AudioConfig import Config  
import os
from LogSetup import SetupLogger
from AudioTransport.PhysicalLayer.tools.GraphRecv import create_graph, change_graph
import logging
import threading
import ttkbootstrap as ttk
from ttkbootstrap.constants import INFO, SUCCESS
from Style import create_ui

logger = SetupLogger("[RecvTest.py]", logging.DEBUG)
selected_folder = None


def Recv(receiver_frame, config:Config):
    global selected_folder

    graph_holder = {}
    graph_holder['graph_label'] = create_graph(receiver_frame)  # create graph --> maybe i will change the logic

    # open a folder dialog --> select a folder for saving files
    def open_folder_dialog():
        global selected_folder
        folder_path = filedialog.askdirectory(title="Select a Folder to Save Files")
        if folder_path:
            selected_folder = folder_path
            logger.info(f"Folder selected: {os.path.abspath(selected_folder)}")
        else:
            logger.info("No folder selected.")

    # start receiving data
    def receive_data():
        if not selected_folder:
            logger.info("Please select a folder before receiving data.")
            return

        try:
            thread = threading.Thread(target=ReceiveAndSaveFile, args=(selected_folder,config,))
            thread.daemon = True
            thread.start()

            graph_holder['graph_label'].destroy()
            graph_holder['graph_label'] = change_graph(receiver_frame)
        except Exception as e:
            logger.error(f"Error during file reception: {e}")

    # use UI
    create_ui(
        receiver_frame,
        first_button_action=open_folder_dialog,
        second_button_action=receive_data,
        first_butt_name="Select Folder to Save Files",
        second_butt_name="Start Listening",
        slider_name1="Block Size",
        slider_name2="Calc Interval",
        slider_name3="?????"
    )
