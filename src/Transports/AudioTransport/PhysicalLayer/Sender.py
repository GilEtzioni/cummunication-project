##########################this needs to be cleaned up.##########################




#!/usr/bin/env python3
"""Play a sine signal."""
import AudioTransport.PhysicalLayer.conf as conf
import numpy as np
# import matplotlib.pyplot as plt
import sounddevice as sd
import logging
import LogSetup
logger = LogSetup.SetupLogger("Sender", logging.DEBUG)



class AudioEncoder:
    def __init__(self):
        self.phase = 0
        rfftSize= int(conf.RecvBlockSizeMs*(conf.RecvSampleRate / (1000)))
        # print(f"rfftSize {rfftSize}")
        availableFreqs=np.fft.rfftfreq(rfftSize,1/conf.RecvSampleRate)
        print(availableFreqs)
        self.usedFreqs= availableFreqs[availableFreqs>=conf.StartFrequency][:conf.FrequencySteps]
        if(np.max(self.usedFreqs)>conf.MaxFrequency or len(self.usedFreqs)<conf.FrequencySteps):
            logger.error("Error: not enough frequencies")


        
    def encode(self,byte):
        data = self.ByteToWaveformPhased(byte,conf.SendSampleRate)
        return data
    
    def ByteToWaveformPhased(self,byte, sampleRate=conf.SendSampleRate, lengthMult=conf.SendDataBlocks):
        freq = self.usedFreqs[int(byte)]
        logger.debug(f"encoding {int(byte)} as {freq}")
        samplesToSend = int((conf.RecvBlockSizeMs* sampleRate*lengthMult) / 1000)

        t = np.arange(samplesToSend) / sampleRate
        phase_increment = 2 * np.pi * freq / sampleRate
        data = conf.SendAmplitude * np.sin(2 * np.pi * freq * t + self.phase)
        
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

def GenerateWaveform(data):
    encoder = AudioEncoder()
    waveForm = np.array([])
    for i in data:
        waveForm = np.append(waveForm,encoder.encode(i))
    return waveForm

def SendFrameRaw(data):
    
    data = addFooter(data)
    logger.debug(data)
    # TODO add configuration when creating encoder
    waveForm = GenerateWaveform(data)
    logger.info("Playing waveform")
    sd.play(waveForm,blocking=True,samplerate=conf.SendSampleRate)
    logger.debug("Waveform played")

if __name__ == "__main__":
    SendFrameRaw(b'1'*10)   
    # RawSend(b'1A'*10)
    import os
    # RawSend(os.urandom(5))