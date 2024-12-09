# style
from Style import create_ui
from ttkbootstrap.constants import INFO, SUCCESS

# standart
import threading

# functions
from tkinter import filedialog
from App.ApplicationLayerFunctions import TransferFile
from LogSetup import SetupLogger
import logging
from AudioTransport.PhysicalLayer.tools.GraphSend import create_graph, change_graph
from AudioTransport.AudioConfig import Config  

logger = SetupLogger("[SendTest]", logging.DEBUG)
selected_file_path = None

def Send(sender_frame,config:Config,path_from_cli=None):
    global selected_file_path
    if path_from_cli:
        selected_file_path = path_from_cli
        logger.debug(f"File selected: {selected_file_path}")
    # graph_holder = {}  # Use a dictionary to hold the graph label reference
    # graph_holder['graph_label'] = create_graph(sender_frame)  # create graph --> maybe i will change the logic

    # open a file dialog --> select a file to send
    def open_file_dialog():
        global selected_file_path
        file_path = filedialog.askopenfilename(
            title="Select a File to Send",
            filetypes=(("All Files", "*.*"), ("Text Files", "*.txt"), ("PDF Files", "*.pdf")),
        )
        if file_path:
            selected_file_path = file_path
            logger.info(f"File selected: {file_path}")
        else:
            logger.info("[No file selected.")

    # send the selected file
    def send_file():
        if not selected_file_path:
            logger.info("No file selected.")
            return

        try:
            thread = threading.Thread(target=TransferFile, args=(selected_file_path,config))
            thread.daemon = True
            thread.start()
            logger.debug(f"File sent successfully: {selected_file_path}")

            # update the graph after the user start listening
            # graph_holder['graph_label'].destroy()
            # graph_holder['graph_label'] = change_graph(sender_frame)
        except Exception as e:
            logger.error(f"Error sending file: {e}")

    # UI
    create_ui(
        sender_frame,
        first_button_action=open_file_dialog,
        second_button_action=send_file,
        conf=config,
        first_butt_name="Select File to Send",
        second_butt_name="Send",
        has_volume=True,
    )