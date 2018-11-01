import numpy as np

from simulationtools import room_wrapper
from simulationtools.config import baseconfig as cfg
from utils import processing
from utils import plotting
from utils import log


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

all_feature_lists1 = room.receive_features(config.mic_location1, 10, 0.20, angle_from_first_pair, fr_limit=20)
all_feature_lists2 = room.receive_features(config.mic_location2, 10, 0.20, angle_from_second_pair, fr_limit=20)

log.INFO("shape of all features lists: ", np.shape(all_feature_lists1))
for frame_index in range(np.shape(all_feature_lists1)[0]):
    matched_indexes = processing.get_matched_angle_indexes(all_feature_lists1[frame_index], all_feature_lists2[frame_index],
                                                           config.decimation_factor, config.matching_method)
    result = processing.match_estimations_with_real_sources(angle_from_first_pair, angle_from_second_pair,
                                                            matched_indexes, config,
                                                            [1.02, 4.0], [4.0, 1.52], max_r=0.2)
    print(result)

# plotting.plot_histograms(all_feature_lists1, all_feature_lists2, config.decimation_factor)

