##########################this needs to be cleaned up.##########################




#!/usr/bin/env python3
"""Play a sine signal."""
import AudioTransport.PhysicalLayer.conf as conf
import numpy as np
from scipy.io import wavfile

# import matplotlib.pyplot as plt
import time
import sounddevice as sd
rfftSize= int(conf.RecvBlockSizeMs*(conf.RecvSampleRate / (1000)))
# print(f"rfftSize {rfftSize}")
availableFreqs=np.fft.rfftfreq(rfftSize,1/conf.RecvSampleRate)
usedFreqs= availableFreqs[availableFreqs>=conf.StartFrequency][:conf.FrequencySteps]

# print (len(usedFreqs))
# for freq in usedFreqs:
#     print(f"Sending {freq}")    
# print (np.max(usedFreqs))
# print (usedFreqs)
# exit(1)
if(np.max(usedFreqs)>conf.MaxFrequency or len(usedFreqs)<conf.FrequencySteps):
    print("Error: not enough frequencies")

def ByteToWaveformPhased(byte, sampleRate=conf.SendSampleRate, start_phase=0,lengthMult=1):
    freq = usedFreqs[int(byte)]
    print(f"encoding {int(byte)} as {freq}")
    samplesToSend = int((conf.RecvBlockSizeMs* sampleRate*lengthMult) / 1000)

    
    t = np.arange(samplesToSend) / sampleRate
    phase_increment = 2 * np.pi * freq / sampleRate
    data = conf.SendAmplitude * np.sin(2 * np.pi * freq * t + start_phase)
    
    # Calculate the final phase
    final_phase = (start_phase + phase_increment * samplesToSend) % (2 * np.pi)
    ramp_length = int(samplesToSend * 0.2)  # 20% of the total samples for fade-in and fade-out
    ramp = np.linspace(0.5, 1, ramp_length)
    window = np.ones(samplesToSend)
    window[:ramp_length] = ramp  # Apply fade-in
    window[-ramp_length:] = ramp[::-1] 
    data*=window
    # samplesToZero = int(conf.SendBlockSizeMs*(sampleRate / (1000)))
    # zeroes= np.zeros(samplesToZero)
    # data = np.append(data,zeroes)
    return data, final_phase


def RawSend(data):
    FRAME_HEADER = list([258,258,258])
    data = FRAME_HEADER + list([len(data)])  + list(data)
    print(data)
    phase=0
    output =np.array([])
    append,phase = ByteToWaveformPhased(257,conf.SendSampleRate,phase)
    output = np.append(output,(append),axis=0)
    
    for i in data:

        append,phase = ByteToWaveformPhased(i,conf.SendSampleRate,phase,conf.SendDataBlocks)
        output = np.append(output,(append),axis=0)
        append,phase = ByteToWaveformPhased(257,conf.SendSampleRate,phase,conf.SendControlBlocks)
        output = np.append(output,(append),axis=0)
    wavfile.write("output.wav",int(conf.SendSampleRate),output)
    # np.append(output,np.zeros(20000))
    # print(len(ByteToWaveform(0))*len(data))
    # print(len(output))
    # plt.figure(figsize=(30, 10))
    # plt.plot(output)
    # plt.title("Output Waveform")
    # plt.xlabel("Sample Number")
    # plt.ylabel("Amplitude")
    # plt.show()
    sd.play(output,blocking=True,samplerate=conf.SendSampleRate)
if __name__ == "__main__":
    RawSend(b'ABAA'*10)