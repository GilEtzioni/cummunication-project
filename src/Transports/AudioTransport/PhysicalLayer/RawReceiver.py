#!/usr/bin/env python3
import AudioTransport.PhysicalLayer.conf as conf
import numpy as np
import sounddevice as sd
import numpy as np
import logging
import LogSetup

logger = LogSetup.SetupLogger("RawReceiver", logging.DEBUG)
# fftsize calcInterval maxFrameSize
maxFrameSize = 41+5
fftsize = int(conf.RecvSampleRate*conf.RecvBlockSizeMs//1000)
calcIntervalMs= 5
samplesPerByte = conf.SendDataBlocks*conf.RecvBlockSizeMs//calcIntervalMs
samplesToHold = maxFrameSize*samplesPerByte
calcIntervalSamples = int(conf.RecvSampleRate*calcIntervalMs//1000)

low, high = conf.StartFrequency,conf.MaxFrequency
allFreqs = np.fft.rfftfreq(fftsize,1/conf.RecvSampleRate )
lowFreqIndex = np.searchsorted(allFreqs, low)


def fftChunk(data): 
    

    # print (allFreqs)
    # exit(1)
    return np.abs(np.fft.rfft(data,n=len(data)))



def processChunk(chunkData):
    fft = fftChunk(chunkData)[lowFreqIndex: lowFreqIndex+conf.FrequencySteps]
    value = int(np.argmax(fft))
    # print(value)
    matchLevel = np.max(fft)
    noise = np.sum(fft)-matchLevel
    return value,matchLevel,noise



    
    

def calcChecksum(samples):
    chk =0
    for sample in samples:
        chk +=sample
    return chk

# check frames after we go to calc final snr
def tryGetValidFrame(srcData):
    if 65 != srcData[-2] or 65!=srcData[-1]:
        return None
    dataLen = srcData[-3]
    
    if(dataLen>len(srcData)-5) or dataLen<1:
        return None
  
    chksum = calcChecksum(srcData[-5-dataLen:-5])
    
    recvChkSum = int.from_bytes(srcData[-5:-3],"big")
    # if checksum matches then it is valid
    if chksum == recvChkSum: 
        return srcData[-5-dataLen:-5]

def findFrame(sampleVals,sampleSigs,sampleNoises): 
    # Get the relevant samples to check
    step = conf.SendDataBlocks*conf.RecvBlockSizeMs //calcIntervalMs
    if len(sampleVals)<5*step:
        return None,0
    relevantVals = (sampleVals[::-step])[::-1]
    relevantSigs = (sampleSigs[::-step])[::-1]
    relevantNoises = (sampleNoises[::-step])[::-1]
  
    validFrame =tryGetValidFrame(relevantVals)
    
    totalNoise = int(sum(relevantNoises))+0.1
    totalSignal =  int(sum(relevantSigs))
# # For printing out the samples for debug purposes
#     for sample in relevantVals:
#         # if sample.noise==0:
#         print(sample,end=" ")
#     print(f"snr: {totalSignal/totalNoise}")
  
    # print (f"chksum {chksum} last {relevantSamples[-1]}")
    # we can save processing time if we have a start sequence maybe a smaller checksum
    # Last 5 bytes are the checksum and the length of the data
    totalNoise = 0
    totalSignal = 0
    if validFrame:
        totalNoise = relevantNoises[-5-len(validFrame)]
        totalSignal =relevantSigs[-5-len(validFrame)]
        # int(sum(relevantSigs[-5-len(validFrame)]))
        if totalNoise == 0:
            snr= 1000000
        else:
            snr = totalSignal/totalNoise
            # don't return footer
        return bytes(validFrame),snr
    return None,0

        



ret= None
class AudioReceiver:
    # todo add configs here
    def __init__(self):
        self.received = None
        self.fullData= np.zeros(fftsize*maxFrameSize)
        self.sampleVals = []
        self.sampleSigs = []
        self.sampleNoises = []
        self.complete = False
        self.waitAtEnd = samplesToHold
        self.snr = 0
    # def audio_callback(self,indata, frames, timer, status):
    #     """This is called (from a separate thread) for each audio block."""
    #     assert len(indata) ==calcIntervalSamples
    #     if status:
    #         logger.error(status, file=sys.stderr)
    #     self.processAudioSample(indata[:,0])
    def processAudioSample(self,data):
        shift = len(data)
        self.fullData = np.roll(self.fullData, -shift)
        self.fullData[-shift:] = data
        val,sig,noise = processChunk(self.fullData[-fftsize:])
        self.sampleVals.append(val)
        self.sampleSigs.append(sig)
        self.sampleNoises.append(noise)
        if len(self.sampleVals)>samplesToHold:
            self.sampleVals.pop(0)
            self.sampleSigs.pop(0)
            self.sampleNoises.pop(0)

        received,snr = findFrame(self.sampleVals,self.sampleSigs,self.sampleNoises)
        # check more samples to get a good snr reading
        if not received and not self.received:
            return
        if  not self.received:
            self.waitAtEnd = samplesPerByte
            self.received = received
            self.snr = snr
            return
        if  self.waitAtEnd>0:
            self.waitAtEnd-=1
            self.snr = max(snr,self.snr)
            return
        
        self.complete = True
            
    def recvFrameBlocking(self,timeout=0):
        # TODO add error handling and confgurations
        self.received = None
        self.complete = False
        self.snr = 0
        self.sampleNoises = []
        self.sampleSigs = []
        self.sampleVals = []
        self.waitAtEnd = 100
        logger.debug("Receiving frame")
        blocksLeftToTimeout = timeout*1000/calcIntervalMs
        self.stream =  sd.InputStream(channels=1,samplerate=conf.RecvSampleRate,blocksize=int(calcIntervalSamples))
        self.stream.start()
        while not self.complete:
            if timeout !=0 and blocksLeftToTimeout<0:
                logger.warning("Timeout receiving audio")
                raise TimeoutError
            blocksLeftToTimeout-=1
            data,missedSamples = self.stream.read(calcIntervalSamples)
            if missedSamples:
                logger.debug(f"missed samples when receiving audio maybe try reducing processing time")
            self.processAudioSample(data[:,0])
        self.stream.stop()
        logger.info(f"received: {self.received} len{len(self.received)} snr: {self.snr}")
    
        return self.received, self.snr
    
def RecvFrameRaw(timeout = 0):
    global ret
    # TODO add configuration when creating AudioReceiver
    audio_receiver = AudioReceiver()    
    return audio_receiver.recvFrameBlocking(timeout)



if __name__ == "__main__":
    logger.info(RecvFrameRaw())