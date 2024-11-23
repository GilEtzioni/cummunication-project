from AudioTransport.PhysicalLayer.RawReceiver import *
from AudioTransport.PhysicalLayer.RawSender import *
import os

    
def test_SendRecvLoud():
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(RecvFrameRaw, timeout = 20)
        data = os.urandom(40)
        SendFrameRaw(data)

        value, snr = future.result()
        assert value == data
        assert snr > 0
