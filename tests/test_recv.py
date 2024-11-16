import numpy as np
from recv import processChunk
from send import ByteToWaveformPhased
import conf

def test_processChunk():
    for i in range (conf.FrequencySteps):
        waveform,_ = ByteToWaveformPhased(i,conf.RecvSampleRate)
        value, matchLevel = processChunk(waveform)
        assert isinstance(value, int), "Value should be an integer"
        assert isinstance(matchLevel, float), "Match level should be a float"
        assert value == i, "Value source and value returned should be the same"
        assert matchLevel >= 0, "Match level should be non-negative"
        print(value, matchLevel)
        print("Test passed")



def test_WaitForHeader():
    # Placeholder test for WaitForHeader
    # Add actual test logic when the function is implemented
    pass