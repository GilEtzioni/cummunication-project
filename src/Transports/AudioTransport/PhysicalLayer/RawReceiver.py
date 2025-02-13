#!/usr/bin/env python3
import AudioTransport.PhysicalLayer.conf as conf
import numpy as np
import sounddevice as sd
import numpy as np
import logging
import LogSetup
from AudioTransport.AudioConfig import Config   

logger = LogSetup.SetupLogger("RawReceiver", logging.DEBUG)

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
    validFrame =tryGetValidFrame(sampleVals)
# For printing out the samples for debug purposes

    # totalNoise = int(sum(sampleNoises))+0.1
    # totalSignal =  int(sum(sampleNoises))
    # for sample in sampleVals:
    #     # if sample.noise==0:
    #     print(sample,end=" ")
    # print(f"snr: {totalSignal/totalNoise}")
    totalNoise = 0
    totalSignal = 0
    if validFrame:
        totalNoise = sampleNoises[-5-len(validFrame)]
        totalSignal =sampleSigs[-5-len(validFrame)]
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
    def __init__(self,conf:Config):
        self.received = None

        self.sampleVals = []
        self.sampleSigs = []
        self.sampleNoises = []
        self.complete = False
        self.sampleRate = conf.sampleRate
        self.maxRawFrameSize = conf.maxFrameSize+6
        self.fftsize = int((conf.sampleRate*conf.msPerFFT)//1000)
        self.calcIntervalMs = conf.calcIntervalMs
        self.calcIntervalSamples = int(conf.sampleRate*conf.calcIntervalMs//1000)
        self.samplesPerByte =1000//(conf.speedBPS*self.calcIntervalMs)        
        self.fullData= np.zeros(self.fftsize)
        self.samplesToHold = self.maxRawFrameSize*self.samplesPerByte
        self.waitAtEnd = self.samplesToHold
        self.conf = conf
        self.snr = 0
        self.step =self.samplesPerByte
        allFreqs = np.fft.rfftfreq(self.fftsize,1/conf.sampleRate )
        self.lowFreqIndex = np.searchsorted(allFreqs, conf.freq)
        print(f"lowFreqIndex {self.lowFreqIndex} allFreqs {allFreqs[self.lowFreqIndex]}")
        # self.usedFreqs= availableFreqs[availableFreqs>=conf.StartFrequency][:conf.FrequencySteps]
        
    
    def fftChunk(self,data): 
        return np.abs(np.fft.rfft(data,n=len(data)))

    def processChunk(self,chunkData):
        fft = self.fftChunk(chunkData)[self.lowFreqIndex: self.lowFreqIndex+256]
        self.conf.graphData = fft
        value = int(np.argmax(fft))
        # print(value)
        matchLevel = np.max(fft)
        noise = np.sum(fft)-matchLevel
        return value,matchLevel,noise

    def processAudioSample(self,data):
        shift = len(data)
        self.fullData = np.roll(self.fullData, -shift)
        self.fullData[-shift:] = data
        val,sig,noise = self.processChunk(self.fullData[-self.fftsize:])

        self.sampleVals.append(val)        
        self.sampleSigs.append(sig)
        self.sampleNoises.append(noise)
        if len(self.sampleVals)>self.samplesToHold:
            self.sampleVals.pop(0)
            self.sampleSigs.pop(0)
            self.sampleNoises.pop(0)


        if len(self.sampleVals)<5*self.step:
            return None,0
        
        received,snr = findFrame((self.sampleVals[::-self.step])[::-1],(self.sampleSigs[::-self.step])[::-1],(self.sampleNoises[::-self.step])[::-1])
        # check more samples to get a good snr reading
        if not received and not self.received:
            return
        if  not self.received:
            self.waitAtEnd = self.samplesPerByte
            self.received = received
            self.snr = snr
            return
        if  self.waitAtEnd>0:
            self.waitAtEnd-=1
            self.snr = max(snr,self.snr)
            return
        
        self.complete = True
            
    def recvFrameBlocking(self,timeout:int):
        # TODO add error handling and confgurations
        self.received = None
        self.complete = False
        self.snr = 0
        self.sampleNoises = []
        self.sampleSigs = []
        self.sampleVals = []
        self.waitAtEnd = 100
        self.fullData = np.zeros(self.fftsize)
        logger.debug("Receiving frame")
        blocksLeftToTimeout = timeout*1000/self.calcIntervalMs
        self.stream =  sd.InputStream(channels=1,samplerate=self.sampleRate,blocksize=int(self.calcIntervalSamples))
        self.stream.start()
        while not self.complete:
            if timeout !=0 and blocksLeftToTimeout<0:
                logger.debug("Timeout receiving audio")
                raise TimeoutError
            blocksLeftToTimeout-=1
            data,missedSamples = self.stream.read(self.calcIntervalSamples)
            if missedSamples:
                logger.debug(f"missed samples when receiving audio maybe try reducing processing time")
            self.processAudioSample(data[:,0])
        self.stream.stop()
        logger.debug(f"received: {self.received} len{len(self.received)} snr: {self.snr}")
    
        return self.received, self.snr
    
def RecvFrameRaw(config = Config(),timeout = 0):
    logger.debug(f"volume (%): {config.get_volume()}")
    logger.debug(f"frequency start (HZ): {config.get_frequency()}")
    logger.debug(f"bitrate (bps): {config.get_bitrate()}")
    global ret
    
    # TODO add configuration when creating AudioReceiver
    audio_receiver = AudioReceiver(config)    
    return audio_receiver.recvFrameBlocking(timeout)



if __name__ == "__main__":
    logger.info(RecvFrameRaw())