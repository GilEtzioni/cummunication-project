#!/usr/bin/env python3
import AudioTransport.PhysicalLayer.conf as conf
import sys
import numpy as np
import sounddevice as sd
import queue
from AudioTransport.PhysicalLayer.RecvRaw import processChunk
q = queue.Queue()
samplesPerChunk = int(conf.RecvSampleRate*conf.RecvBlockSizeMs//1000)
chunkData = np.zeros(samplesPerChunk)
divider=30
diff=conf.SendDataBlocks
windowSize = int(divider*(diff+(conf.SendControlBlocks*2)))
numSamples=0
print (windowSize ," ",samplesPerChunk)
print (conf.RecvSampleRate ," ",conf.RecvBlockSizeMs)
window = np.full((windowSize) ,-1)
def audio_callback(indata, frames, timer, status):
    global chunkData
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(np.copy(indata[:,0]))

state = 'waiting'
data = b''
def startAudioListener():
    global data
    global state
    with sd.InputStream(channels=1,
        samplerate=conf.RecvSampleRate, callback=audio_callback,blocksize=int(samplesPerChunk)//divider):

        while True:
            if state == 'failed':
                return b''
            if state== 'finished':
                state = 'waiting'
                return data
            processAudioSample()

def processAudioSample():
        global chunkData
        global window
        global numSamples
        try:
            data = q.get_nowait()
        except queue.Empty:
            return
        shift = len(data)
        chunkData = np.roll(chunkData, -shift)
        chunkData[-shift:] = data
        val,mag = processChunk(chunkData)
        
        window = np.roll(window,-1)

        # print (val,mag)
        # ignore small magnitudes
        if mag>5:
            window[-1] = val
        else:
            window[-1] = -1
        used = window[-numSamples:]
        # print (window)
        match1 = np.count_nonzero(used[0:windowSize//6] == 257)
        match2 = np.count_nonzero(used[-windowSize//6:] == 257)
        # print (match1,match2)
        numSamples+=1
        # return
        # don't process unless we have a full window
        if numSamples<windowSize-10:
            return
        # print (window)
        # if we dont have a match for more than two windows rest the statemachine
        if numSamples>windowSize*2:
            stateMachine(-1)
            
        unique, counts = np.unique(window[window!=257], return_counts=True)       
        
        matches = False

        if match1 > windowSize//50 and match2 > windowSize//50:
            matches = True
            print ("matched")
        if matches and not np.max(counts)>len(window[window!=257])*0.6:
            print (window)
            # print ("before",matches ,unique[np.argmax(counts)],np.max(counts))
        if matches and np.max(counts)>len(window[window!=257])*0.1 and unique[np.argmax(counts)]!=-1 :
            print (unique[np.argmax(counts)])
            samplesLeft = np.count_nonzero(window[-windowSize//3:] == 257)
            # print (window)
            window[:-samplesLeft]= np.full(windowSize-samplesLeft,-1)
            
            # reset window
            numSamples=samplesLeft
            # return
            stateMachine(unique[np.argmax(counts)])
                
state = 'waiting'
controlCount=0
bytesLeft=0
receivedBytes = bytes([])
# TODO handle case where it stops receiving probably should be handled above better
def stateMachine(value):
    global state
    global data
    global controlCount
    global bytesLeft
    global receivedBytes
    if value != -1:
        print (value,state,controlCount)
    if state == 'waiting':
        if value == 258:
            controlCount+=1
            return 
        if controlCount>2 :
            print (f"receiving frame of length {value}")
            bytesLeft=value
            state = 'receiving'
            receivedBytes = bytes([])
            controlCount=0
        else:
            controlCount=0
    elif state == 'receiving':
        if value == -1:
            print ("timeout")

            state = 'failed'
            return
        receivedBytes+=bytes([value])
        print (f"Received: {receivedBytes} bytes left in frame:{bytesLeft}")
        if bytesLeft == 1:
            print (f"Received frame {receivedBytes[:-1]}")
            data = receivedBytes
            state = 'finished'
        
        bytesLeft-=1

if __name__ == "__main__":
    startAudioListener()