# TODO change the names of the modules
from AudioTransport.PhysicalLayer.RawReceiver import RecvFrameRaw   
from AudioTransport.PhysicalLayer.RawSender import SendFrameRaw
from AudioTransport.AudioConfig import Config  
import time
import logging
import LogSetup

logger = LogSetup.SetupLogger("[AudioTransport.py]", logging.DEBUG)
# We might want to add retries and timeouts to this layer


def RecvFrame(expectedFrameNum,config:Config) -> bytes:
    """Receive Frame and return it or None if invalid"""
    if expectedFrameNum != 0:
        logger.info(f"Receiving raw frame number {expectedFrameNum}")
    expectedFrameNum = expectedFrameNum%256
    while True:
        received,_ = RecvFrameRaw(config)
        logger.debug(int(received[0]))
        logger.debug(expectedFrameNum)
        if int(received[0]) == expectedFrameNum:
            break
        logger.warning(f"received frame {int(received[0])} twice")
        SendFrameRaw(b'1',config)
        
    logger.debug(f"Frame received successfully: {received}")
    # respond to sender to indicate that the frame was received
    SendFrameRaw(b'1',config)
    return received[1:]
    
def SendFrame(data: bytes,frameNumber: int,config: Config,retries = 3)-> bool:
    """Send Frame of up to 40 bytes and return True if successful False if not"""
    logger.debug(f"Sending frame: {data}")

    for _ in range(retries):
        SendFrameRaw((frameNumber%256).to_bytes(1)+data,config)
        
        # allow for 3 seconds for the receiver to respond
        try:
            received,_ = RecvFrameRaw(config = config,timeout = 3)
        except TimeoutError:
            logger.warning("\nTimeout receiving ACK from receiver\n")
            continue
        logger.info(f"Frame sent successfully {data}")
        return
    
    logger.debug("Frame sending failed")
    raise Exception(f"Frame sending failed after {retries} retries")



if __name__ == "__main__":
    # test the transport layer
    SendFrame(b'Hello World')

