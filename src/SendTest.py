import os
import tkinter as tk
from tkinter import filedialog
from App.ApplicationLayerFunctions import TransferFile
from LogSetup import SetupLogger
import logging
from AudioTransport.PhysicalLayer.tools.GraphSend import create_graph, change_graph
import threading
import ttkbootstrap as ttk
from ttkbootstrap.constants import INFO, SUCCESS
from Style import create_ui

logger = SetupLogger("[SendTest]", logging.DEBUG)
selected_file_path = None

def Send(sender_frame, output_text):
    global selected_file_path

    graph_holder = {}  # Use a dictionary to hold the graph label reference
    graph_holder['graph_label'] = create_graph(sender_frame)  # create graph --> maybe i will change the logic

    # open a file dialog --> select a file to send
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
            thread = threading.Thread(target=TransferFile, args=(selected_file_path,))
            thread.daemon = True
            thread.start()
            logger.info(f"[SendTest.py] File sent successfully: {selected_file_path}")

            # update the graph after the user start listening
            graph_holder['graph_label'].destroy()
            graph_holder['graph_label'] = change_graph(sender_frame)
        except Exception as e:
            logger.error(f"[SendTest.py] Error sending file: {e}")

    # use UI
    create_ui(
        sender_frame,
        first_button_action=open_file_dialog,
        second_button_action=send_file,
        first_butt_name="Select File to Send",
        second_butt_name="Send",
        slider_name1="Voulme",
        slider_name2="Frequency",
        slider_name3="Block Size"
    )