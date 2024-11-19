from .TransportLayerFunctions import SendFile, ReceiveFile

# reads the file using the transport layer
def TransferFile(filepath: str):
    print(f"[Application Layer] Preparing to send file: {filepath}")
    try:
        SendFile(filepath)
        print(f"[Application Layer] File '{filepath}' sent successfully.")
    except Exception as e:
        print(f"[Application Layer] Error during file transfer: {e}")


# get a file and saves it to the specified directory
def ReceiveAndSaveFile(output_dir: str):
    print(f"[Application Layer] Waiting to receive file...")
    try:
        filename = ReceiveFile(output_dir)
        print(f"[Application Layer] File received and saved as '{filename}'.")
        return filename
    except Exception as e:
        print(f"[Application Layer] Error during file reception: {e}")
        return None  # when it's error
