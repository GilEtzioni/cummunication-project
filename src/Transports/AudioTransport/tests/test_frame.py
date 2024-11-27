from AudioTransport.PhysicalLayer.RawReceiver import *
from AudioTransport.PhysicalLayer.RawSender import *
import os

def test_footer():
    data = b'0' + os.urandom(39)
    frame = addFooter(data)
    ret = tryGetValidFrame(frame)
    assert ret == data
    ret = tryGetValidFrame(b'1'+frame[1:])
    assert ret == None
    
    
def test_SendRecvWaveForm():
    # data = os.urandom(39)
    data = b"111111"
    frame = addFooter(data)
    waveForm = GenerateWaveform(frame+b'0',Config()) 
    receiver = AudioReceiver(Config())
    ret = None
    for i in range(0,len(waveForm),receiver.calcIntervalSamples):
        chunk = waveForm[i:i+receiver.calcIntervalSamples]
        ret = receiver.processAudioSample(chunk)
    assert receiver.received == data
    print(receiver.received, receiver.snr)
    
def test_processChunk():
    for i in b'1111111123123':
        encoder = AudioEncoder(Config())
        waveform = encoder.ByteToWaveformPhased(i)
        receiver = AudioReceiver(Config())
        value, matchLevel,noise = receiver.processChunk(waveform[:receiver.fftsize])
        assert value == i, "Value source and value returned should be the same"
        assert matchLevel >= 0, "Match level should be non-negative"
        print(value, matchLevel)
        print("Test passed")
    
if __name__ == "__main__":
    # test_footer()
    # test_processChunk()
    test_SendRecvWaveForm()
    print("All tests passed")