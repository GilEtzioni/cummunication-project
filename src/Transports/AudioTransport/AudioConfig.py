class Config:
    def __init__(self, volume =0.5, freq = 1000, speedBPS = 5, parent_frame = None):
        self.volume = volume
        self.freq = 1000 #4 options 1000, 3000, 8000, 15000
        self.speedBPS= 5 # 4 options 2,5,20,50 
        self.sampleRate = 41200.0
        self.calcInterval = 5
        self.msPerFFT = 50
        self.parent_frame = None
        self.maxFrameSize= 40
        self.calcIntervalMs= 5



