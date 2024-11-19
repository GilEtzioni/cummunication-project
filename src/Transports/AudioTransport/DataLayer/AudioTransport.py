from PhysicalLayer.recvSound import startAudioListener   
from PhysicalLayer.SendRaw import RawSend
import time
import logging
import LogSetup

logger = LogSetup.SetupLogger("AudioTransport", logging.DEBUG)
# We might want to add retries and timeouts to this layer

def RecvFrame() -> bytes:
    """Receive Frame and return it or None if invalid"""
    logger.debug("Received raw frame:")
    receivedRaw = startAudioListener()
    received = _DecodeAudioFrame(receivedRaw)
  
    time.sleep(1.5)
    
    if received == None:
        # failed receiving frame send '0' to sender so it can resend
        logger.error("Error receiving frame")
        RawSend(_EncodeAudioFrame(b'0'))
        return None
    
    logger.info(f"Frame received successfully: {received}")
    # send '1' to sender to indicate frame was received successfully
    RawSend(_EncodeAudioFrame(b'1'))
    return received
    
def SendFrame(data: bytes)-> bool:
    """Send Frame of up to 40 bytes and return True if successful False if not"""
    logger.info("Sending frame",data)
    
    RawSend(_EncodeAudioFrame(data))
    
    # Todo when working with two computers we can remove this sleep
    time.sleep(0.5)
    if startAudioListener()!=b'1':
        logger.error("Frame not sent successfully")
        return
    
    logger.info("Frame sent successfully")



def _calculateChecksum(bytes):
    return sum(bytes)%256


def _EncodeAudioFrame(data) -> None:
    """currently adds checksum to data"""
    assert len(data) <= 40,"trying to send too large a frame"
    logger.debug(f"sum: {_calculateChecksum(data)}")
    rawFrame =   list(data) + list([_calculateChecksum(data)])
    logger.debug(f"rawFrame {rawFrame}")
    return rawFrame

def _DecodeAudioFrame(data) -> bytes:
    """Verify checksum and return data if valid return None if invalid"""
    logger.debug(f"decoding data: {data}")
    logger.debug(f"comparing checksum with received  {int(_calculateChecksum(data[0:-1]))}, {int(data[-1])}")
    
    if _calculateChecksum(data[0:-1]) == data[-1]:
        return data[0:-1]
    return None


