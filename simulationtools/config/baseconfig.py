import numpy as np

class BaseConfig:
    def __init__(self):
        self.room_dimension = [6., 8., 3.8]
        self.absorption = 0.85
        self.max_order = 5
        self.src_signal1 = "src/female.wav"
        self.src_signal2 = "src/male_fr.wav"
        self.fs = 44100
        self.nsamples = 2048
        self.frame_length = 50
        self.L = [500, 600, 750, 900, 1000]
        self.mic_location1 = np.c_[
            [1.00, 4.02, 1.5],  # mic1
            [1.00, 3.98, 1.5],  # mic2
            [1.04, 4.02, 1.5],  # mic3
            [1.04, 3.98, 1.5],  # mic4
        ]
        self.mic_location2 = np.c_[
            [4.02, 1.54, 1.5],  # mic1
            [4.02, 1.50, 1.5],  # mic2
            [3.98, 1.50, 1.5],  # mic3
            [3.98, 1.54, 1.5],  # mic4
        ]
        self.source_location1 = [2.6, 5.7, 1.8]
        self.source_location2 = [2.0, 1.5, 1.8]
