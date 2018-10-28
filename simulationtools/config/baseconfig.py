import numpy as np


class BaseConfig:
    def __init__(self):
        self.room_dimension = [6., 8., 3.8]
        self.absorption = 0.95
        self.max_order = 0
        self.src_signal1 = "src/female.wav"
        self.src_signal2 = "src/male_fr.wav"
        self.fs = 44100
        self.nsamples = 2048
        self.frame_length = 50
        # self.L = [500, 525, 550, 575, 600, 625, 650, 675, 700, 725, 750, 775, 800, 850, 900, 950]
        self.L = range(500, 1010, 10)
        self.mic_location1 = np.c_[
            [1.00, 4.01, 1.5],  # mic1
            [1.00, 3.99, 1.5],  # mic2
            [1.02, 4.01, 1.5],  # mic3
            [1.02, 3.99, 1.5],  # mic4
        ]
        self.mic_location2 = np.c_[
            [4.01, 1.52, 1.5],  # mic1
            [4.01, 1.50, 1.5],  # mic2
            [3.99, 1.50, 1.5],  # mic3
            [3.99, 1.52, 1.5],  # mic4
        ]
        self.source_location1 = [2.6, 5.7, 1.8]
        self.source_location2 = [2.0, 1.5, 1.8]
        self.decimation_factor = 1


class ConfigI(BaseConfig):
    def __init__(self):
        super(ConfigI, self).__init__()
        self.source_location1 = [2.0, 4.7, 1.8]
        self.source_location2 = [2.3, 1.7, 1.8]
