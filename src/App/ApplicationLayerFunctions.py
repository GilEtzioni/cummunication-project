from App.TransportLayerFunctions import SendFile, ReceiveFile
from AudioTransport.AudioConfig import Config  
import os
import LogSetup
import sys

# source venv/bin/activate
# python3 src/App/ApplicationLayerFunctions.py ReceiveAndSaveFile
# python3 src/App/ApplicationLayerFunctions.py TransferFile

logger = LogSetup.SetupLogger("ApplicationLayer")

# reads the file using the transport layer
def TransferFile(filepath: str,config:Config):
    logger.debug(f"Preparing to send file: {filepath}")

    if not os.path.exists(filepath):  # e.g. /Users/Desktop/FileOverSound/src/example.txt
        logger.error(f"File '{filepath}' does not exist.")
        return  # exit if there is no file

    try:
        filename = os.path.basename(filepath)  # e.g., example.txt
        filelen = os.path.getsize(filepath)    # e.g., 115
        logger.info(f"Starting SendFile from {filepath}\n")
        SendFile(filepath, filelen, filename,config)
        logger.info(f"\nFile '{filepath}' sent successfully.")

    except Exception as e:
        logger.error(f"Sending stopped because {e}")



# get a file and saves it to the specified directory
def ReceiveAndSaveFile(output_dir: str,config:Config) -> str:
    logger.info(f"Waiting to receive file...\n")
    try:
        filename = ReceiveFile(output_dir,config)            # get filename from the header
        filepath = os.path.join(output_dir, filename) # compute the full file path
        logger.info(f"\nFile received and saved as '{filepath}'.")
        return filepath
    except Exception as e:
        logger.error(f"Error during file reception: {e}. try again.")
        return None  # return None when it's error


if __name__ == "__main__":
    # if len(sys.argv) < 2:
    #     sys.exit(1)

    # function_to_call = sys.argv[1]

    # if function_to_call == "TransferFile":
    #     hardcoded_file_path = "/Users/giletzioni/Desktop/FileOverSound-gil/src/SendAndSaveFiles/SendFiles/example.txt"
    #     TransferFile(hardcoded_file_path,Config())

    # elif function_to_call == "ReceiveAndSaveFile":
    #     hardcoded_output_dir = "/Users/giletzioni/Desktop/FileOverSound-gil/src/SendAndSaveFiles/GetFiles"
    ReceiveAndSaveFile("./files",Config())

    # else:
    #     sys.exit(1)
