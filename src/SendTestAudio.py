from AudioTransport.DataLayer.AudioTransport import SendFrame,RecvFrame
import os
import time
# example of how to send a frame
def Send():

    data = b'hi from sender' # 40 bytes
    try:    
        SendFrame(data)
    except Exception as e:
        print("Error sending frame:", e)
        return

if __name__ == "__main__":
    Send()