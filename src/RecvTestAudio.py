from AudioTransport.DataLayer.AudioTransport import RecvFrame
import time


# Example of how to receive a frame
def Recv():
    frame = RecvFrame()
    print("Frame received:", frame)
if __name__ == "__main__":
    Recv()