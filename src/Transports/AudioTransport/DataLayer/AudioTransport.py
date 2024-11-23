# TODO change the names of the modules
from PhysicalLayer.Receiver import RecvFrameRaw   
from AudioTransport.PhysicalLayer.Sender import SendFrameRaw
import time
import logging
import LogSetup

logger = LogSetup.SetupLogger("[AudioTransport.py]", logging.DEBUG)
# We might want to add retries and timeouts to this layer

def RecvFrame() -> bytes:
    """Receive Frame and return it or None if invalid"""
    logger.debug("Receiving raw frame:")
    received = RecvFrameRaw()
  
    time.sleep(1.5)
    
    if received == None:
        # failed receiving frame send '0' to sender so it can resend
        logger.error("\n\n ----------------------------------------------------------------------")
        logger.error("Error receiving frame")
        SendFrameRaw(b'0')
        return None
    
    logger.info(f"Frame received successfully: {received}")
    # send '1' to sender to indicate frame was received successfully
    SendFrameRaw(b'1')
    return received
    
def SendFrame(data: bytes,retries = 3)-> bool:
    """Send Frame of up to 40 bytes and return True if successful False if not"""
    # logger.info("Sending frame",data)
    logger.info(f"Sending frame: {data}")

    
    SendFrameRaw((data))
    
    # Todo when working with two computers we can remove this sleep
    time.sleep(0.5)
    received,_ = RecvFrameRaw()
    if received!=b'1':
        logger.error(f"Frame not sent successfully {received}")
        return
    
    logger.info("Frame sent successfully")


if __name__ == "__main__":
    # test the transport layer
    SendFrame(b'Hello World')

