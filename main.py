import numpy as np

from simulationtools import room_wrapper
from simulationtools.config import baseconfig as cfg
from utils import processing
from utils import plotting
from utils import log
import matplotlib.pyplot as plt


log = log.Log()
#==================================================#

config = cfg.BaseConfig()
room = room_wrapper.RoomWrapper(config)

angle_from_first_pair = room.receive_angles(config.mic_location1)
angle_from_second_pair = room.receive_angles(config.mic_location2)

found_crossings = processing.find_intersections(angle_from_first_pair, angle_from_second_pair, [1.02, 4.0], [4.0, 1.52])
log.INFO("crossing values: ", found_crossings)

# plotting.plot_crossings(found_crossings, [config.source_location1, config.source_location2],
#                         [6., 8., 3.8], [[1.02, 4.], [4., 1.52]],
#                         [angle_from_first_pair, angle_from_second_pair])

all_feature_lists1 = room.receive_features(config.mic_location1, 10, 0.20, angle_from_first_pair, fr_limit=120)
all_feature_lists2 = room.receive_features(config.mic_location2, 10, 0.20, angle_from_second_pair, fr_limit=120)

log.INFO("shape of all features lists: ", np.shape(all_feature_lists1))
plotting.plot_histograms(all_feature_lists1, all_feature_lists2, config.decimation_factor)

