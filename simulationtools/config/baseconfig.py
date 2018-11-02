from utils import processing as pr
import numpy as np


class BaseConfig:
    def __init__(self):
        # room attributes
        self.room_dimension = [6., 8., 3.8]
        self.absorption = 0.95
        self.max_order = 0
        self.fs = 44100

        # DOA attributes
        self.nsamples = 2048
        self.frame_length = 50
        self.L = range(500, 1010, 10)
        # self.mic_location1 = np.c_[
        #     [1.00, 4.01, 1.5],  # mic1
        #     [1.00, 3.99, 1.5],  # mic2
        #     [1.02, 4.01, 1.5],  # mic3
        #     [1.02, 3.99, 1.5],  # mic4
        # ]
        # self.mic_location2 = np.c_[
        #     [4.01, 1.52, 1.5],  # mic1
        #     [4.01, 1.50, 1.5],  # mic2
        #     [3.99, 1.50, 1.5],  # mic3
        #     [3.99, 1.52, 1.5],  # mic4
        # ]

        # mics array
        self.source_center1 = [1.01, 4.0, 1.5]
        self.source_center2 = [4.0, 1.51, 1.5]
        self.mics_no = 4
        self.mics_phi = np.pi / 4
        self.r = 0.01414
        self.mic_location1 = pr.create_circular_mic_array(self.source_center1, self.mics_no, self.mics_phi, self.r)
        self.mic_location2 = pr.create_circular_mic_array(self.source_center2, self.mics_no, self.mics_phi, self.r)

        # sources
        self.source_location1 = [2.6, 5.7, 1.8]
        self.source_location2 = [2.0, 1.5, 1.8]
        self.src_signal1 = "src/female.wav"
        self.src_signal2 = "src/male_fr.wav"

        # other
        self.decimation_factor = 1
        self.matching_method = "PEARSON"

        # room plotting
        self.master_plot = 0
        self.plot_rir = 0
        self.plot_room = 0
        self.plot_doa_radar = 0
        self. plot_spectrogram1 = 0
        self. plot_spectrogram2 = 0
        self. write_mic_signal = 0

        # restult plotting
        self.plot_intersections = 0
        self.calculate_features = 1
        self.plot_histograms = 0


class UniversalConfig(BaseConfig):
    def __init__(self, data_from_xlsx):
        BaseConfig.__init__(self)
        self.absorption = data_from_xlsx[0]
        self.max_order = data_from_xlsx[1]
        self.source_center1 = data_from_xlsx[2]
        self.source_center2 = data_from_xlsx[3]
        self.mics_no = data_from_xlsx[4]
        self.mics_phi = data_from_xlsx[5]
        self.r = data_from_xlsx[6]
        self.source_location1 = data_from_xlsx[7]
        self.source_location2 = data_from_xlsx[8]
        self.matching_method = data_from_xlsx[9]

        # needs to be calculated once more (values have been updated)
        self.mic_location1 = pr.create_circular_mic_array(self.source_center1, self.mics_no, self.mics_phi, self.r)
        self.mic_location2 = pr.create_circular_mic_array(self.source_center2, self.mics_no, self.mics_phi, self.r)