import os
import socket

# send up to 40 bytes throws an error on failure
def SendFrame(bytes: bytes):

    assert len(bytes) <= 40, "trying to send too large a frame"
    s = socket.socket()         

    port = 1234              

    s.connect(('127.0.0.1', port)) 
 
 
    if len(bytes) != s.send(bytes):
        raise Exception("Error sending frame")
    s.close()   


def RecvFrame() -> bytes:
    # next create a socket object 
    s = socket.socket()        
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    port = 1234             
    s.bind(('', port))         
    s.listen(1)     
    c, addr = s.accept()
         
    ret = c.recv(40)
    
    c.close()
    s.close()
    return ret
    

