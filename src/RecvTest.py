from transport.socketTransport import RecvFrame


# Example of how to receive a frame
def Recv():
    frame = RecvFrame()
    print("Frame received:", frame)
if __name__ == "__main__":
    Recv()