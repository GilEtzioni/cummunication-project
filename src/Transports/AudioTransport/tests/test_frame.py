from AudioTransport.PhysicalLayer.Receiver import *
from AudioTransport.PhysicalLayer.Sender import *
import os

def test_footer():
    data = b'0'+ os.urandom(39)
    frame = addFooter(data)
    ret = tryGetValidFrame(frame)
    assert ret == data
    ret = tryGetValidFrame(b'1'+frame[1:])
    assert ret == None
    
    
def test_SendRecvWaveForm():
    # data = os.urandom(39)
    data = b"111111"
    frame = addFooter(data)
    waveForm = GenerateWaveform(frame)
    receiver = AudioReceiver()
    ret = None
    for i in range(0,len(waveForm),calcIntervalSamples):
        chunk = waveForm[i:i+calcIntervalSamples]
        ret = receiver.processAudioSample(chunk)
    assert receiver.received == data
    print(receiver.received, receiver.snr)
    
