##########################this needs to be cleaned up.##########################




#!/usr/bin/env python3
"""Play a sine signal."""

import numpy as np
# import matplotlib.pyplot as plt
import sounddevice as sd
from AudioTransport.AudioConfig import Config  
import logging
import LogSetup
logger = LogSetup.SetupLogger("RawSender", logging.INFO)



class AudioEncoder:
    def __init__(self,conf:Config = Config()):
        self.phase = 0
        self.conf = conf
        rfftSize= int(conf.msPerFFT*(conf.sampleRate / (1000)))
        # print(f"rfftSize {rfftSize}")
        availableFreqs=np.fft.rfftfreq(rfftSize,1/conf.sampleRate)
        print(availableFreqs)
        self.usedFreqs= availableFreqs[availableFreqs>=conf.freq][:256]
        # if(np.max(self.usedFreqs)>conf.MaxFrequency or len(self.usedFreqs)<conf.freq):
        #     logger.error("Error: not enough frequencies")


        
    def encode(self,byte):
        data = self.ByteToWaveformPhased(byte)
        return data
    
    def ByteToWaveformPhased(self,byte ):

        freq = self.usedFreqs[int(byte)]
        logger.debug(f"encoding {int(byte)} as {freq}")
        samplesToSend = int((self.conf.sampleRate/self.conf.speedBPS) )

        t = np.arange(samplesToSend) / self.conf.sampleRate
        phase_increment = 2 * np.pi * freq / self.conf.sampleRate
        data =self.conf.volume * np.sin(2 * np.pi * freq * t + self.phase)
        
        # Keep track of the phase so we dont have a jump in the waveform
        self.phase= (self.phase + phase_increment * samplesToSend) % (2 * np.pi)
        return data

def plotWaveform(waveForm):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    ax.plot(waveForm)
    ax.grid()
    plt.show()
    
def addFooter(data):
    # 4 bytes is to much for regular chksum 40*256 can only go so high
    chksum = sum(data).to_bytes(2,byteorder='big')
    logger.debug(f"Checksum: {chksum}")
    return data +chksum + bytes([len(data)]) +b'AA'   

def GenerateWaveform(data,config: Config):
    encoder = AudioEncoder(config)
    waveForm = np.array([])
    for i in data:
        waveForm = np.append(waveForm,encoder.encode(i))
    return waveForm

def SendFrameRaw(data,config: Config = Config()):    
    
    data = addFooter(data)
    logger.debug(data)
    # TODO add configuration when creating encoder
    waveForm = GenerateWaveform(data,config)
    logger.debug("Playing waveform")
    sd.play(waveForm,blocking=True,samplerate=config.sampleRate)
    logger.debug("Waveform played")

if __name__ == "__main__":
    SendFrameRaw(b'1'*10)   
    # RawSend(b'1A'*10)
    import os
    # RawSend(os.urandom(5))