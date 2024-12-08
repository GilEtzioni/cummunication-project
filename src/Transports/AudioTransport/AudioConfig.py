class Config:
    def __init__(self, volume =0.5, freq = 100, speedBPS = 5, parent_frame = None):
        self.volume = volume        # binary (1 or 0)
        self.freq = freq            #4 options 1000, 3000, 8000, 15000
        self.speedBPS= speedBPS     # 4 options 2,5,20,50 
        self.sampleRate = 41200.0
        self.msPerFFT = 75
        self.parent_frame = None
        self.maxFrameSize= 40
        self.calcIntervalMs= 5
        self.graphData =[]
    # volume
    def get_volume(self):
        return self.volume


    def set_volume(self, volume):
        self.volume = volume


    # frequency
    def get_frequency(self):
        return self.freq


    def set_frequency(self, freq):
        self.freq = freq


    # blockSize
    def get_bitrate(self):
        return self.speedBPS


    def set_bitrate(self, speedBPS):
        self.speedBPS = speedBPS
