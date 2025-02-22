from Transports.AudioTransport.DataLayer.AudioTransport import SendFrame,RecvFrame
from AudioTransport.AudioConfig import Config  
import time
import LogSetup

CHUNK = 40
MAX_HEADER = 40

logger = LogSetup.SetupLogger("TransportLayer")

# send the file
def SendFile(filepath, filelen, filename,config:Config):
    logger.debug(f"File details: Name='{filename}', Length={filelen} bytes, filepath={filepath}")

    # ----- sender header -----
    # e.g:  b'\x00\x00\x00\x0bexample.txt\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00x'
    #
    # FileNamelen: int     \x00\x00\x00\x0b
    # FileName: string      example.txt\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00
    # FileLen: int          \x00\x00\x00x
    frameNumber = 0
    try:
        # create the header
        header = {
            "FileNamelen": len(filename),
            "FileName": filename,
            "FileLen": filelen,
        }
        header_bytes = CreateHeader(header)          # convert header to bytes
        logger.debug(f"Sending header: {header}")

        SendFrame(header_bytes,frameNumber,config)  # send the header
        frameNumber += 1
        # ----------------------------- without the delay .pdf will fail! -----------------------------
        time.sleep(0.02)

        logger.debug(f"Sending file content in chunks of {CHUNK} bytes...")
        try:
            with open(filepath, "rb") as f:  # read
                chunk_number = 0
                while chunk := f.read(CHUNK):
                    chunk_number += 1
                    logger.debug(f"Sending chunk {chunk_number}: {chunk}")
                    SendFrame(chunk,frameNumber,config)
                    frameNumber += 1
                    time.sleep(0.005)  # delay between chunks (LESS THAN 0.005 WILL PROBABLY FAIL!!!)
        except Exception as e:
            logger.error(f"Error while sending file parts: {e}")
            raise

        logger.debug(f"File '{filename}' sent successfully.")
    except Exception as e:
        logger.debug(f"Error in SendFile: {e}")
        raise


# get a file header and its content, then writes the file to the output directory 
def ReceiveFile(output_dir: str,config: Config) -> str:
    logger.debug("in ReceiveFile")
    nextFrameNumber = 0
    try:
        header_bytes = RecvFrame(nextFrameNumber,config)
        nextFrameNumber += 1

        if len(header_bytes) != MAX_HEADER:
            logger.error("Invalid header size received.")
            raise ValueError("Invalid header size.")

        header = UnpackHeader(header_bytes)

        # extract filename and file length from the header
        filename = header["FileName"]
        filelen = header["FileLen"]

        filepath = f"{output_dir}/{filename}"
        # receive and save the file in chunks
        try:
            with open(filepath, "wb") as f:  # write
                received_len = 0

                while received_len < filelen:
                    chunk = RecvFrame(nextFrameNumber,config)
      
    
                    valid_chunk_size = min(filelen - received_len, len(chunk))
                    logger.debug(f"Received chunk {nextFrameNumber}: {chunk[:valid_chunk_size]}")
                    nextFrameNumber += 1
                    f.write(chunk[:valid_chunk_size])
                    received_len += valid_chunk_size
        except Exception as e:
            logger.error(f"Error while receiving file parts: {e}")
            raise

        logger.debug(f"File '{filename}' has been processed.")
        return filename

    except Exception as e:
        logger.error(f"Error in ReceiveFile: {e}")
        raise


# converts the header dictionary into a byte array
# ensures the header (filename length, filename, and file length) can be sent in 0/1 over the network
def CreateHeader(header: dict) -> bytes:
    logger.debug("in CreateHeader")

    try:
        filename = header["FileName"].encode('utf-8')  # convert the string to bytes
        header_bytes = (
            header["FileNamelen"].to_bytes(4, 'big') +
            filename.ljust(32, b'\0') +                # ensuring the filename is exactly 32 bytes (makes the header fixed-length)
            header["FileLen"].to_bytes(4, 'big')
        )

        # ensure the header = exactly 256 bytes (add zeros)
        header_bytes = header_bytes.ljust(CHUNK, b'\0')[:CHUNK]

        logger.debug(f"header bytes: {header_bytes}")
        return header_bytes

    except Exception as e:
        logger.error(f"Error in CreateHeader: {e}")
        raise


# unpacks the byte array back into a header dictionary for interpretation.
def UnpackHeader(header_bytes: bytes) -> dict:
    try:
        
        logger.debug("in UnpackHeader")
        file_name_len = int.from_bytes(header_bytes[:4], 'big')         # first 4 bytes from the header     -> int
        filename = header_bytes[4:36].rstrip(b'\0').decode('utf-8')     # next 32 bytes                     -> UTF-8 string
        file_len = int.from_bytes(header_bytes[36:], 'big')             # the remaining bytes (file length) -> int

        # ----- header -----
        # FileNamelen: int
        # FileName: string
        # FileLen: int 
        unpacked_header = {
            "FileNamelen": file_name_len,
            "FileName": filename,
            "FileLen": file_len,
        }
        logger.debug(f"unpacked header: {unpacked_header}")
        return unpacked_header

    except Exception as e:
        logger.error(f"Error in UnpackHeader: {e}")
        raise