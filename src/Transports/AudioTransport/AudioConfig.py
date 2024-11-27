class Config:
    def __init__(self, volume =0.5, freq = 1000, speedBPS = 5, graph_holder = None):
        self.volume = volume
        self.freq = 1000 #4 options 1000, 3000, 8000, 15000
        self.speedBPS= 5 # 4 options 2,5,20,50 
        self.graph_holder = None