#!/usr/bin/env python3
# program for plotting sound and fft live for development purposes
import AudioTransport.PhysicalLayer.conf as conf
import queue
import sys
import time
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import matplotlib
# matplotlib.use('Agg') 
def fftChunk(chunkData):
    return np.abs(np.fft.rfft(chunkData,n=fftsize))[lowFreqIndex: lowFreqIndex+conf.FrequencySteps]



q = queue.Queue()
lastime=0

def audio_callback(indata, frames, timer, status):
    global lastime
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    # Fancy indexing with mapping creates a (necessary!) copy:
    # print(f"interval {timer.inputBufferAdcTime-lastime}")
    lastime = timer.inputBufferAdcTime
    
    q.put(np.copy(indata[:,0]))

last=0

counter=0
received = ""
state= 0 
start=0
maxTime = 0
maxCnt =0
maxMag=0
recvCnt = 0


def update_plot(frame):
    """This is called by matplotlib for each plot update.

    Typically, audio callbacks happen more frequently than plot updates,
    therefore the queue tends to contain multiple blocks of audio data.

    """
    global magnitude
    global freqs
    global plotData
    global fftPlotData
    while True:
        try:
            data = q.get_nowait()
        except queue.Empty:
            break
        shift = len(data)
        plotData = np.roll(plotData, -shift)
        plotData[-shift:] = data
        fftPlotData=np.roll(fftPlotData,-shift)
        fftPlotData[-shift:] = data
    line1.set_ydata(fftChunk(fftPlotData))
    line1.set_xdata(freqs)
    line2.set_ydata(plotData)

    # ax.set_ylim(0, max_magnitude + 1) 
    return line1,line2

low, high = conf.StartFrequency,conf.MaxFrequency

samplerate = conf.RecvSampleRate
blockSizeMs=conf.RecvBlockSizeMs

fftsize= int(blockSizeMs*(samplerate / (1000)))
length = int(blockSizeMs * samplerate / (1000))
plotData = np.zeros((length*20))
fftPlotData = np.zeros((length))
fullFreqs = np.fft.rfftfreq(fftsize,1/samplerate)
lowFreqIndex = np.searchsorted(fullFreqs, low)
freqs = fullFreqs[lowFreqIndex: lowFreqIndex+conf.FrequencySteps]

magnitude = np.abs(np.fft.rfft(np.zeros(fftsize),n=fftsize))[lowFreqIndex: lowFreqIndex+conf.FrequencySteps]
window = np.copy(magnitude)
fig, (ax,ax2) = plt.subplots(2, 1, figsize=(10, 10)) 
line1, = ax.plot(magnitude)
line2,= ax2.plot(plotData)
ax.axis((low-100, np.max(freqs)+100, 0, 200))
ax2.axis((0, len(plotData), -1, 1))


stream = sd.InputStream(channels=1,
    samplerate=samplerate, callback=audio_callback,blocksize=int(samplerate//100))
ani = FuncAnimation(fig, update_plot,interval=30, blit=True)
with stream:
    plt.show()
