from transport.socketTransport import SendFrame

# example of how to send a frame
def Send():

    frame = b'1234567890123456789012345678901234567890'  # 40 bytes
    try:    
        SendFrame(frame)
    except Exception as e:
        print("Error sending frame:", e)
        return
    print("Frame sent")
    
if __name__ == "__main__":
    Send()