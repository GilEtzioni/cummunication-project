import AudioTransport.PhysicalLayer.conf as conf
import numpy as np

low, high = conf.StartFrequency,conf.MaxFrequency

fftsize= int(conf.RecvBlockSizeMs*(conf.RecvSampleRate / (1000)))
allFreqs = np.fft.rfftfreq(fftsize,1/conf.RecvSampleRate )
lowFreqIndex = np.searchsorted(allFreqs, low)
usedFreqs = allFreqs[lowFreqIndex: lowFreqIndex+conf.FrequencySteps]

def fftChunk(chunkData):
    return np.abs(np.fft.rfft(chunkData,n=fftsize))[lowFreqIndex: lowFreqIndex+conf.FrequencySteps]

def processChunk(chunkData):
    premag = fftChunk(chunkData)
    value = int(np.argmax(premag))
    # print(value)
    matchLevel = np.max(premag)
    return value,matchLevel


# RecvData. 