#!/usr/bin/env python3
import conf
import queue
import sys
import time
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd


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
    global max_magnitude
    global plotData
    global last
    global counter
    global fftsize
    global received
    global state
    global start
    global maxCnt
    global maxMag
    global maxArg
    global maxTime
    global recvCnt
    global window
    while True:
        try:
            data = q.get_nowait()
        except queue.Empty:
            break
        shift = len(data)
        plotData = np.roll(plotData, -shift)
        plotData[-shift:] = data
        premag = np.abs(np.fft.rfft(plotData,n=fftsize))[lowFreqIndex-2: lowFreqIndex+conf.FrequencySteps+2]
        indexToFind = 0

        for i in range(2,len(premag)-2):
            magnitude[i-2] = premag[i]/(np.sum(premag[i-2:i+2])+1)
        # magnitude = premag[2:-2]
        # inRange = find_mag/np.sum(magnitude[indexToFind-2:indexToFind+2])
        # if inRange > 0.95:
            # exit(0)
        # print("inRange",np.max(inRange),"argrange",np.argmax(inRange),"find_mag",find_mag)
        # if np.argmax(inRange)== 248 and np.max(inRange) > 0.8 :
        #     exit (0)
        windowSize = conf.SendBlockSizeMs/2
        countPer=(conf.SendBlockSizeMs+conf.RecvBlockSizeMs)
        find_mag = magnitude[indexToFind]
        # print (f"find_mag: {find_mag}")
        maxArgT = np.argmax(magnitude)
        if state == 0 and find_mag >0.4 and maxArgT == 0:
            state = 1
            counter = 0
            start = time.time()
            print(f"start: {time.time()}")
            # print (f"maxArg: {maxArgT} find_mag: {find_mag}")
        elif state == 1:
            counter+=1
            # print(f"counter: {counter} find_mag: {find_mag}")
            if find_mag > maxMag:
                maxArg = np.argmax(magnitude)
                maxMag = find_mag
                maxCnt = counter
                maxTime = time.time()
            if counter > countPer -windowSize:
                if maxMag > 0.7:
                    print(f"end: {maxTime-start} mag{maxMag} last{maxCnt}") 
                    state = 2
                    counter -= maxCnt
                    recvCnt = 289
                else:
                        state = 0
                
                maxMag = 0
        elif state == 2:
            

            counter+=1

            if counter < countPer-windowSize:
                continue
            if counter<countPer+windowSize:
                window+=magnitude
                # print(f"counter: {counter} find_mag: {np.max(magnitude )}num {np.argmax(magnitude)}")
                if np.max(magnitude ) > maxMag:
                    maxArg = np.argmax(magnitude)
                    maxMag = np.max(magnitude )
                    maxCnt = counter
                    maxTime = time.time()
                continue
            
            # if max_magnitude > 0:
            # print (f"max mag: {maxMag} freqs: {freqs[maxArg]} num {maxArg}")
            print (f"max wind: {np.max(window)} freqs: {freqs[np.argmax(window)]} num {np.argmax(window)}")
            maxArg =0
            maxCnt = 0
            maxMag = 0
            recvCnt-=1
            window = 0
            counter = windowSize
            # print(f"max mag: {max_magnitude}")
            if recvCnt == 0:
                state = 0
        # elif state == 2:

            
            
            
        # print (f"{counter} max_magnitude: {max_magnitude} freqs: {lastfreq}")
        # print (f"got number {np.where(freqs==lastfreq)[0][0]}")
        # received+=chr((np.where(freqs==lastfreq)[0][0]))
        # print (received)
        # counter = 0
        # continue
   
        # print (avg_magnitude)
            # print(f"max_magnitude: {max_magnitude} freqs: {freqs[np.argmax(magnitude)]}")

    line1.set_ydata(magnitude)
    line1.set_xdata(freqs)
    line2.set_ydata(plotData)

    # ax.set_ylim(0, max_magnitude + 1) 
    return line1,line2

low, high = conf.StartFrequency,conf.MaxFrequency

samplerate = conf.RecvSampleRate
blockSizeMs=conf.RecvBlockSizeMs

fftsize= int(blockSizeMs*(samplerate / (1000)))
length = int(200 * samplerate / (1000))
plotData = np.zeros((length))
fullFreqs = np.fft.rfftfreq(fftsize,1/samplerate)
lowFreqIndex = np.searchsorted(fullFreqs, low)
freqs = fullFreqs[lowFreqIndex: lowFreqIndex+conf.FrequencySteps]

magnitude = np.abs(np.fft.rfft(np.zeros(fftsize),n=fftsize))[lowFreqIndex: lowFreqIndex+conf.FrequencySteps]
window = np.copy(magnitude)
fig, (ax,ax2) = plt.subplots(2, 1, figsize=(10, 10)) 
line1, = ax.plot(magnitude)
line2,= ax2.plot(plotData)
# ax.set_ylim(0, 10) 
# if len(args.channels) > 1:
#     ax.legend([f'channel {c}' for c in args.channels],
#               loc='lower left', ncol=len(args.channels))
ax.axis((low-1000, np.max(freqs)+1000, 0, 1))
ax2.axis((0, len(plotData), -1, 1))
# ax2.set_yticks([0])
# ax2.yaxis.grid(True)
# ax2.tick_params(bottom=False, top=False, labelbottom=False,
#                 right=False, left=False, labelleft=False)
fig.tight_layout(pad=0)

stream = sd.InputStream(channels=1,
    samplerate=samplerate, callback=audio_callback,blocksize=int(samplerate//1000))
ani = FuncAnimation(fig, update_plot,interval=30, blit=True)
with stream:
    plt.show()
