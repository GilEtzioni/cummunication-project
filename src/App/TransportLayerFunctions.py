import os
from Transports.AudioTransport.DataLayer.AudioTransport import SendFrame, RecvFrame
# from Transports.SocketTransport.SocketTransport import SendFrame, RecvFrame

import time

# splits the file into chunks(40 bytes) ()
def SendFile(filepath: str):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"[Transport Layer] File '{filepath}' does not exist.")

    filename = os.path.basename(filepath)
    filelen = os.path.getsize(filepath)

    print(f"[Transport Layer] File details: Name='{filename}', Length={filelen} bytes")

    # ----- sender header -----
    # FileNamelen: int
    # FileName: string
    # FileLen: int
    header = {
        "FileNamelen": len(filename),
        "FileName": filename,
        "FileLen": filelen,
    }
    header_bytes = SerializeHeader(header)
    print(f"[Transport Layer] Sending header: {header}")
    SendFrame(header_bytes)

    # ----------------------------- without the delay .pdf will fail! -----------------------------
    time.sleep(0.02)

    # send file in 40-byte chunks
    print(f"[Transport Layer] Sending file content in chunks of 40 bytes...")
    with open(filepath, "rb") as f:
        chunk_number = 0
        while chunk := f.read(40):
            chunk_number += 1
            print(f"[Transport Layer] Sending chunk {chunk_number}: {chunk}")
            SendFrame(chunk)
            time.sleep(0.005)  # delay between chunks (LESS THAN 0.005 WILL PROBABLY FAIL!!!)
    print(f"[Transport Layer] File '{filename}' sent successfully.")

# get a file header and its content, then writes the file to the output directory 
def ReceiveFile(output_dir: str) -> str:
    # get the header
    header_bytes = RecvFrame()
    header = DeserializeHeader(header_bytes)
    print(f"[Transport Layer] Received header: {header}")

    # ----- receiver header -----
    # FileName: string
    # FileLen: int
    # filepath: string
    filename = header["FileName"]
    filelen = header["FileLen"]
    filepath = os.path.join(output_dir, filename)
    print(f"[Transport Layer] Preparing to receive file: {filename} ({filelen} bytes)")

    # get the file's content
    with open(filepath, "wb") as f:
        received_len = 0
        chunk_number = 0
        while received_len < filelen:
            chunk = RecvFrame()
            chunk_number += 1
            valid_chunk_size = min(filelen - received_len, len(chunk))  # Handle last chunk
            print(f"[Transport Layer] Received chunk {chunk_number}: {chunk[:valid_chunk_size]}")
            f.write(chunk[:valid_chunk_size])  # Write only valid bytes
            received_len += valid_chunk_size

    print(f"[Transport Layer] File received and saved as '{filepath}'.")
    return filename


# converts the header dictionary into a byte array
# ensures the header (filename length, filename, and file length) can be sent in 0/1 over the network
def SerializeHeader(header: dict) -> bytes:

    filename = header["FileName"].encode('utf-8')
    serialized = (
        header["FileNamelen"].to_bytes(4, 'big') +
        filename.ljust(32, b'\0') +  # ensuring the filename is exactly 32 bytes (makes the header fixed-length)
        header["FileLen"].to_bytes(4, 'big')
    )
    print(f"[Transport Layer] Serialized header: {serialized}")
    return serialized

# converts a byte array into a header dictionary
# allows the receiver to interpret metadata (like filename and file size) before processing the file content.
def DeserializeHeader(header_bytes: bytes) -> dict:
    file_name_len = int.from_bytes(header_bytes[:4], 'big')
    filename = header_bytes[4:36].rstrip(b'\0').decode('utf-8')
    file_len = int.from_bytes(header_bytes[36:], 'big')

    # ----- header -----
    # FileNamelen: int
    # FileName: string
    # FileLen: int 
    deserialized = {
        "FileNamelen": file_name_len,
        "FileName": filename,
        "FileLen": file_len,
    }
    print(f"[Transport Layer] Deserialized header: {deserialized}")
    return deserialized
